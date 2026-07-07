from category.models import Category
from cart.models import Cart
from settings.models import settings
def header_data(request):

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart = None

    setting = settings.objects.filter(is_default=True).first()

    return {
        'header_categories': Category.objects.filter(parent=None,is_active=True)[:8],
        'cart': cart,
        'setting' : setting
    }