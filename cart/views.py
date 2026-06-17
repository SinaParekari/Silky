from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from product.models import Product, ProductVariant
from .models import Cart, CartItem




def add_to_cart(request, slug):

    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "login_required": True,
            "login_url": reverse("login")
        })

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request"
        })

    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))

    if not variant_id:
        return JsonResponse({
            "success": False,
            "message": "Variant not selected"
        })

    product = get_object_or_404(
        Product,
        slug=slug
    )

    variant = get_object_or_404(
        ProductVariant,
        id=variant_id,
        product=product
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={
            'product': product,
            'quantity': quantity
        }
    )

    if not created:

        new_quantity = cart_item.quantity + quantity

        if new_quantity > variant.stock:
            return JsonResponse({
                "success": False,
                "message": "موجودی کافی نیست"
            })

        cart_item.quantity = new_quantity
        cart_item.save()

    else:

        if quantity > variant.stock:
            return JsonResponse({
                "success": False,
                "message": "موجودی کافی نیست"
            })

    return JsonResponse({
        "success": True,
        "cart_count": len(cart),
        "message": "محصول به سبد خرید اضافه شد"
    })


@login_required
def remove_cart_item(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))