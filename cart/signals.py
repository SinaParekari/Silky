from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart as CartDB, CartItem
from product.models import Product, ProductVariant


@receiver(user_logged_in)
def merge_session_cart_to_db(sender, request, user, **kwargs):
    session_cart = request.session.get('cart', {})
    
    if not session_cart:
        return

    db_cart, _ = CartDB.objects.get_or_create(user=user)

    for key, item in session_cart.items():
        try:
            product = Product.objects.get(id=item['product_id'])
            variant = ProductVariant.objects.get(product=product, color=item['color'])
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=db_cart,
                variant=variant,
                defaults={'product': product, 'quantity': 0}
            )
            cart_item.quantity += item['quantity']
            
            # چک موجودی
            if cart_item.quantity > variant.stock:
                cart_item.quantity = variant.stock
            
            cart_item.save()
        except Exception as e:
            print(f'Error merging cart: {e}')
            continue

    # سشن رو پاک کن
    del request.session['cart']
    request.session.modified = True