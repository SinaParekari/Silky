from django.db import transaction

from order.models import Order, OrderItem


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_from_cart(cart, discount=None):

        if not cart.items.exists():
            raise ValueError("Cart is empty.")

        total_price = cart.get_total()

        discount_amount = 0

        if discount:
            discount_amount = discount.calculate_discount(total_price)

        final_price = total_price - discount_amount

        order = Order.objects.create(
            user=cart.user,
            total_price=total_price,
            discount=discount,
            discount_amount=discount_amount,
            final_price=final_price,
        )

        order_items = []

        for item in cart.items.select_related(
            "product",
            "variant",
        ):

            order_items.append(
                OrderItem(
                    order=order,
                    product=item.product,
                    variant=item.variant,
                    product_name=item.product.name,
                    variant_name=item.variant.color,
                    unit_price=item.variant.price,
                    quantity=item.quantity,
                    total_price=item.variant.price * item.quantity,
                )
            )

        OrderItem.objects.bulk_create(order_items)

        return order