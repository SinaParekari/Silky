from category.models import Category
from cart.models import Cart

def header_data(request):

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart = None

    return {
        'header_categories': Category.objects.filter(parent=None,is_active=True)[:8],
        'cart': cart
    }