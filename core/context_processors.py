from category.models import Category

def header_data(request):

    return {
        'header_categories': Category.objects.filter(parent=None,is_active=True)[:8]
    }

def cart_context(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart = None

    return {
        'cart': cart
    }