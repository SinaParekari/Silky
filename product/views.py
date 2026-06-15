from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView
from .models import Product, ProductImage
from category.models import Category
from django.db.models import Avg, Count

# Create your views here.

class ProductListView(ListView):
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return (
            Product.objects
            .get_active_products()
            .annotate(
                avg_rating=Avg('reviews__rating'),
                review_count=Count('reviews')
            )
            .select_related('category')
            .prefetch_related(
                'images',
                'variants',
                'attribute_values'
            )
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.filter(parent=None)

        return context


from django.db.models import Avg
from django.http import Http404
from django.shortcuts import render
from .models import Product, ProductImage

def product_detail_view(request, *args, **kwargs):
    slug = kwargs['slug']
    product = Product.objects.get_product_by_slug(slug)

    if product is None:
        raise Http404("product not found")

    product.visits += 1
    product.save()

    images = ProductImage.objects.filter(product=product)
    variants = product.variants.all()
    reviews = product.reviews.filter(is_approved=True)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    selected_variant = variants.first()
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:10]

    context = {
        'product': product,
        'images': images,
        'variants': variants,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_count': reviews.count(),
        'selected_variant': selected_variant,
        'related_products': related_products,
    }
    return render(request, 'product_detial.html', context)