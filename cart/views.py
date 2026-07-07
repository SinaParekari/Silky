from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from product.models import Product, ProductVariant
from .models import Cart, CartItem, Discount
from user.models import Address
#rest framework
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer, DiscountSerializer

#region---------------------------------- web views -----------------------------------------------------
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

@login_required
def cart_view(request):
    # ← از مدل دیتابیس بگیر نه Cart(request)
    cart = Cart.objects.filter(user=request.user).first()
    
    discount_amount = request.session.get('discount_amount', 0)
    discount_code = request.session.get('discount_code', '')

    cart_items_json = []
    
    if cart:
        for item in cart.items.all():  # ← items رو از دیتابیس بگیر
            cart_items_json.append({
                'key': str(item.id),
                'name': item.product.name,
                'color': item.variant.color,
                'color_code': item.variant.color_code,
                'price': float(item.variant.price),
                'qty': item.quantity,
                'stock': item.variant.stock,
                'image': item.product.main_image.image.url if item.product.main_image else '',
                'total_price': float(item.get_total_price()),
            })

    addresses = []
    if request.user.is_authenticated:
        addresses = request.user.addresses.all()

    related_products = Product.objects.filter(is_active=True)[:8]

    context = {
        'cart': cart,
        'cart_items_json': cart_items_json,
        'discount_amount': discount_amount,
        'discount_code': discount_code,
        'addresses': addresses,
        'related_products': related_products,
    }
    return render(request, 'cart.html', context)
@login_required
def clear_cart(request):

    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        cart.items.all().delete()

    return redirect('cart')

@login_required
def set_main_address(request, address_id):

    if request.method != "POST":
        return JsonResponse({"success": False})

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    Address.objects.filter(
        user=request.user
    ).update(is_default=False)

    address.is_default = True
    address.save()

    return JsonResponse({"success": True})


def apply_coupon(request):

    code = request.POST.get('code')

    try:
        discount = Discount.objects.get(
            code=code,
            is_active=True
        )

    except Discount.DoesNotExist:

        return JsonResponse({
            'success': False,
            'message': 'کد تخفیف معتبر نیست'
        })

    valid, message = discount.is_valid(request.user)

    if not valid:
        return JsonResponse({
            'success': False,
            'message': message
        })

    if discount.discount_type == 'percent':
        label = f'{discount.value}% تخفیف'
    else:
        label = f'{discount.value:,} تومان تخفیف'

    return JsonResponse({
        'success': True,
        'code': discount.code,
        'label': label,
        'value': discount.value,
        'type': discount.discount_type
    })

def apply_discount(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().lower() 
        print(code)
        try:
            discount = Discount.objects.get(code=code)
            is_valid, message = discount.is_valid(user=request.user)  # ← user
            print(is_valid)
            if is_valid:
                request.session['discount_amount'] = int(discount.value)
                request.session['discount_code'] = code
                request.session['discount_id'] = discount.id
                return JsonResponse({
                    'success': True,
                    'code': code,
                    'label': f'{int(discount.value):,} تومان تخفیف',
                    'amount': int(discount.value),
                    'message': message
                })
            else:
                return JsonResponse({'success': False, 'message': message})
        except Discount.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'کد تخفیف معتبر نیست'})
    return JsonResponse({'success': False})
#endregion -----------------------------------------------------------------------------------
#region --------------------------------- API View -----------------------------------------------------
@extend_schema(
summary="Cart",
description="Returns Cart and CartItems(need authentication)."
)
class CartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request : Request):
        cart , created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
@extend_schema(
summary="Adding to Cart",
description="Get's products and add it to User cart."
)
class AddCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request : Request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart , created1 = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=serializer.validated_data['product_id'])
        variant = ProductVariant.objects.get(id=serializer.validated_data['variant_id'])
        cart_item ,created= CartItem.objects.get_or_create(cart=cart,product=product,variant=variant,quantity=serializer.validated_data['quantity'])    

        if not created:
            cart_item.quantity = serializer.validated_data["quantity"]
            cart_item.save()
        
        return Response(None, status=status.HTTP_200_OK)
    
@extend_schema(
summary="Update Cart",
description="Editing Cart, mean increase or decrease the product in Cart."
)
class UpdateCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self , request : Request, pk):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = CartItem.objects.get(id=pk,cart__user=request.user)
        item.quantity = serializer.validated_data['quantity']
        item.save()
        return Response(None, status=status.HTTP_200_OK)
    
@extend_schema(
summary="delete Cart Item",
description="Delete the Cart Item."
)
class DeleteCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request : Request , pk):
        item = CartItem.objects.get(id=pk,cart__user=request.user)

        item.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
@extend_schema(
summary="Checking Discount to apply to the Cart",
description="takes the code , and check if it's appliable or not."
)
class CheckDiscountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request : Request):
        serializer = DiscountSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        discount = Discount.objects.get(code=serializer.validated_data['code'].lower())

        if not discount:
            return Response(None,status=status.HTTP_404_NOT_FOUND)
        
        valid , message = discount.is_valid(request.user)

        if not valid:
            return Response({"valid" : False, "message" : message})
        
        cart = Cart.objects.get(user=request.user)

        total = cart.get_total()

        discount_amount = discount.calculate_discount(total)

        return Response({"valid" : True,"discount" : discount_amount, "final_price" : total - discount_amount})
    

#endregion ---------------------------------------------------------------------------------------------
