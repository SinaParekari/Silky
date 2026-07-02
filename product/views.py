from django.shortcuts import render,redirect
from django.http import Http404
from django.views.generic import ListView
from .models import Product, ProductImage, Review, ProductVariant
from category.models import Category
from django.db.models import Avg, Count, Q
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Min, F, Case, When, OuterRef, Subquery, DecimalField
#rest framework
from .serializers import productSerializer, ProductDetailSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
# Create your views here.

#region ------------------------------- main views -------------------------------------------------------------
class ProductListView(ListView):
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):

        Variant = ProductVariant 

        default_price = Variant.objects.filter(
            product=OuterRef('pk'),
            is_default=True
        ).values('price')[:1]

        first_price = Variant.objects.filter(
            product=OuterRef('pk')
        ).order_by('id').values('price')[:1]

        queryset = (
            Product.objects
            .get_active_products()
            .annotate(
                avg_rating=Avg('reviews__rating'),
                review_count=Count('reviews'),

                price_default=Subquery(default_price, output_field=DecimalField()),

                price_first=Subquery(first_price, output_field=DecimalField()),
            )
            .annotate(
                sort_price=Case(
                    When(price_default__isnull=False, then=F('price_default')),
                    default=F('price_first'),
                    output_field=DecimalField()
                )
            )
            .select_related('category')
            .prefetch_related('images', 'variants', 'attribute_values')
        )

        sort = self.request.GET.get('sort', 'default')

        if sort == 'price-asc':
            queryset = queryset.order_by('sort_price')

        elif sort == 'price-desc':
            queryset = queryset.order_by('-sort_price')

        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')

        elif sort == 'rating':
            queryset = queryset.order_by('-avg_rating')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        return context


def product_detail_view(request, *args, **kwargs):
    slug = kwargs['slug']
    product = Product.objects.get_product_by_slug(slug)
    tags = product.tags.all()
    print(tags)

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

    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
    brand = product.attribute_values.filter(attribute__name='brand').first()


    context = {
        'product': product,
        'images': images,
        'variants': variants,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_count': reviews.count(),
        'selected_variant': selected_variant,
        'related_products': related_products,
        'review_form': ReviewForm(instance=user_review),
        'user_review': user_review,
        'brand' : brand.value if brand else None, 
        'tags' : tags
    }
    return render(request, 'product_detial.html', context)

@login_required(login_url='login')
def add_review_view(request, slug):
    product = Product.objects.get_product_by_slug(slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # چک کن قبلاً نظر داده یا نه
            if not Review.objects.filter(product=product, user=request.user).exists():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
            else:
                # اگه قبلاً نظر داده، آپدیت کن
                Review.objects.filter(product=product, user=request.user).update(
                    rating=form.cleaned_data['rating'],
                    comment=form.cleaned_data['comment'],
                )
    
    return redirect('product_detail', slug=slug)

def search_product(request):
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'default')

    Variant = ProductVariant

    products = Product.objects.none()

    if query:
        products = (
            Product.objects
            .get_active_products()
            .filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            )
            .distinct()
            .annotate(
                avg_rating=Avg('reviews__rating'),
                review_count=Count('reviews'),

                # default variant price
                price_default=Subquery(
                    Variant.objects.filter(
                        product=OuterRef('pk'),
                        is_default=True
                    ).values('price')[:1],
                    output_field=DecimalField()
                ),

                # first variant price
                price_first=Subquery(
                    Variant.objects.filter(
                        product=OuterRef('pk')
                    ).order_by('id').values('price')[:1],
                    output_field=DecimalField()
                ),
            )
            .annotate(
                sort_price=Case(
                    When(price_default__isnull=False, then=F('price_default')),
                    default=F('price_first'),
                    output_field=DecimalField()
                )
            )
            .select_related('category')
            .prefetch_related('tags', 'images', 'variants')
        )

        # ---------- SORT LOGIC ----------
        if sort == 'price-asc':
            products = products.order_by('sort_price')

        elif sort == 'price-desc':
            products = products.order_by('-sort_price')

        elif sort == 'newest':
            products = products.order_by('-created_at')

        elif sort == 'rating':
            products = products.order_by('-avg_rating')

    # ---------- PAGINATION ----------
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'categories': Category.objects.all()
    }

    return render(request, 'shop.html', context)

def search_product_by_category(request, slug):
    category = Category.objects.get(slug=slug)

    products = Product.objects.get_products_by_category(category)

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj' : page_obj,
        'is_paginated' : page_obj.has_other_pages(),
        'categories' : category.children.all()
    }

    return render(request, 'shop.html', context)
#endregion -----------------------------------------------------------------------------------------------------

#region ------------------------------- API views --------------------------------------------------------------
class ProductGenericAPIViewPagination(PageNumberPagination):
    page_size = 3

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.get_active_products()
    serializer_class = productSerializer
    pagination_class = ProductGenericAPIViewPagination

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.get_active_products()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"


#endregion -----------------------------------------------------------------------------------------------------
