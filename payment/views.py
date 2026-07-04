from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction
from django.db.models import F

from cart.models import Cart, Discount, DiscountUsage
from order.services.order_service import OrderService
from payment.models import Payment
from payment.zibal import ZibalGateway
from django.shortcuts import get_object_or_404
from django.utils import timezone
from order.models import Order
# Create your views here.

PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def to_persian_digits(value: str) -> str:
    return value.translate(PERSIAN_DIGITS)


def build_payment_context(payment) -> dict:
    """Data injected into the success page via {{ payment_context|json_script }}."""
    amount = f"{payment.order.final_price:,.0f}"
    paid_at = payment.paid_at or timezone.now()

    return {
        "track_id": payment.track_id,
        "order_number": f"#{payment.order.id}",
        "amount": to_persian_digits(amount),
        "payment_date": to_persian_digits(paid_at.strftime("%Y/%m/%d - %H:%M")),
        "payment_method": payment.get_gateway_display() if hasattr(payment, "get_gateway_display") else "کارت بانکی",
    }

@login_required
def payment_request(request):

    cart = Cart.objects.filter(
        user=request.user
    ).first()

    if not cart:
        return HttpResponse("Cart not found.")

    if not cart.items.exists():
        return HttpResponse("Cart is empty.")

    discount = None

    discount_id = request.session.get("discount_id")

    if discount_id:
        discount = Discount.objects.filter(
            id=discount_id
        ).first()

    

    order = OrderService.create_from_cart(
        cart=cart,
        discount=discount ,
    )

    payment = Payment.objects.create(
        order=order,
        amount=order.final_price,
    )

    result = ZibalGateway.request_payment(
        amount=payment.amount,
        order_id=order.id,
    )

    if not result["success"]:
        payment.status = Payment.Status.FAILED
        payment.save()

        return HttpResponse(
            result["message"]
        )

    payment.track_id = result["track_id"]
    payment.save()

    return redirect(
        result["payment_url"]
    )


@transaction.atomic
def payment_verify(request):

    track_id = request.GET.get("trackId")

    if not track_id:
        return HttpResponse("TrackId not found.")

    payment = get_object_or_404(
        Payment,
        track_id=track_id,
    )

    if payment.status == Payment.Status.SUCCESS:
        return render(
            request,
            "payment_success.html",
            {"order": payment.order, "payment_context": build_payment_context(payment)},
        )

    result = ZibalGateway.verify_payment(track_id)

    if not result["success"]:

        payment.status = Payment.Status.FAILED
        payment.save(update_fields=["status"])

        payment.order.status = Order.Status.FAILED
        payment.order.save(update_fields=["status"])

        return HttpResponse("Payment failed.")

    payment.status = Payment.Status.SUCCESS
    payment.paid_at = timezone.now()
    payment.save(update_fields=["status", "paid_at"])

    payment.order.status = Order.Status.PAID
    payment.order.save(update_fields=["status"])

    for item in payment.order.items.select_related("variant"):

        variant = (
            item.variant.__class__.objects
            .select_for_update()
            .get(pk=item.variant.pk)
        )

        if variant.stock < item.quantity:
            return HttpResponse(
                f"Not enough stock for {variant.product.name}"
            )

        variant.stock = F("stock") - item.quantity
        variant.save(update_fields=["stock"])

    # ثبت استفاده از کد تخفیف
    if payment.order.discount:
        DiscountUsage.objects.get_or_create(
            discount=payment.order.discount,
            user=payment.order.user,
            defaults={
                "order_id": payment.order.id,
            }
        )

    cart = Cart.objects.filter(
        user=payment.order.user
    ).first()

    if cart:
        cart.items.all().delete()

    request.session.pop("discount_id", None)
    request.session.pop("discount_amount", None)
    request.session.pop("discount_code", None)

    return render(
        request,
        "payment_success.html",
        {"payment" : payment,"order": payment.order, "payment_context": build_payment_context(payment)},
    )