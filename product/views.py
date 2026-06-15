from django.shortcuts import render
from django.views.generic import ListView
from .models import Product
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


def product_detial_view(request):
    return render(request,'product_detial.html')
