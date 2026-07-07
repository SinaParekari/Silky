from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from cart.models import Cart
from django.db.models import Sum, Value,Q,Count,Avg
from django.db.models.functions import Coalesce
from product.models import Product
from category.models import Category
from order.models import Order,OrderItem
from django.db import models
from django.db.models import Exists, OuterRef
from settings.models import settings
# Create your views here.

def home_page(request):

    best_products = (
        Product.objects.filter(is_active=True)
        .annotate(avg_rating=Avg('reviews__rating'),review_count=Count('reviews'),total_sales=Coalesce(Sum("orderitem__quantity",filter=models.Q(orderitem__order__status=Order.Status.PAID)),Value(0)))
        .order_by("-total_sales")[:10]
    )

    most_visited_products = (
    Product.objects
    .filter(is_active=True)
    .select_related("category")
    .prefetch_related(
        "images",
        "variants",
        "attribute_values__attribute",
        "reviews",
    )
    .annotate(
        avg_rating=Avg("reviews__rating"),
        review_count=Count("reviews"),
    )
    .order_by("-visits")[:10]
    )

    leaf_categories = (
        Category.objects.annotate(has_children=Exists(Category.objects.filter(parent=OuterRef("pk")))).
        filter(has_children=False)
    )

    categories = []

    for category in leaf_categories:
        categories.append({
            "name": category.name,
            "slug": category.slug,
            "icon": category.icon,
            "count": "",
        })

    products = []

    for product in best_products:
        variant = product.default_variant

        products.append({
            "id": product.id,
            "name": product.name,
            "brand": "",
            "cat": product.category.name,
            "slug": product.slug,

            "price": variant.price if variant else 0,
            "oldPrice": None,
            "discount": 0,

            "rating": product.avg_rating or 0,
            "rCount": product.review_count,

            "stock": variant.stock if variant else 0,

            "isNew": False,
            "isBest": True,

            "img": product.main_image.image.url if product.main_image else "",

            "desc": product.description,

            "specs": [
                {
                    "k": attr.attribute.name,
                    "v": attr.value,
                }
                for attr in product.attribute_values.all()
            ],
        })

    most_visited = []

    for product in most_visited_products:
        variant = product.default_variant

        most_visited.append({
            "id": product.id,
            "name": product.name,
            "brand": "",
            "cat": product.category.name,
            "slug": product.slug,

            "price": variant.price if variant else None,
            "oldPrice": None,
            "discount": 0,

            "rating": product.avg_rating or 0,
            "rCount": product.review_count,

            "stock": variant.stock if variant else 0,

            "isNew": False,
            "isBest": False,

            "img": product.main_image.image.url if product.main_image else "",

            "desc": product.description,

            "specs": [
                {
                    "k": attr.attribute.name,
                    "v": attr.value,
                }
                for attr in product.attribute_values.select_related("attribute")
            ],
        })

    setting = settings.objects.filter(is_default=True).first()
        
    heroStats =  [
                    { "value": f'+{setting.number_of_products}', "label": 'محصول متنوع' },
                    { "value": f'+{setting.sattisfied_customer}K', "label": 'مشتری راضی' },
                    { "value": f'+{setting.brand_count}', "label": 'برند معتبر' },
                    { "value": f'{setting.sattisfy_percent}٪', "label": 'رضایت خریداران' }
                ]

    
    context = {
            "products" : products,
            "most_visited": most_visited,
            "categories" : categories,
            "heroStats" : heroStats,

        }
    
    return render(request, 'home_page.html',context)

def contact_view(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد!')
            return redirect('contact')

    context = {
        'form': form,
    }
    return render(request, 'contact-us.html', context)

def about_us_view(request):
    return render(request, 'about-us.html')

def rules_view(request):
    return render(request,'rules.html')


