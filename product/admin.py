from django.contrib import admin
from .models import Product, ProductImage, ProductVariant, ProductAttributeValue, Review, Tag


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'is_main', 'order']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 2
    fields = ['color', 'color_code', 'price', 'stock']


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 0
    fields = ['attribute', 'value']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'attribute':
            # فقط attributeهای دسته محصول رو نشون بده
            if hasattr(request, '_current_product') and request._current_product:
                attrs = request._current_product.category.get_all_attributes()
                from category.models import CategoryAttribute
                kwargs['queryset'] = CategoryAttribute.objects.filter(id__in=[a.id for a in attrs])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ['user', 'rating', 'comment', 'is_approved']
    readonly_fields = ['user', 'rating', 'comment']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_at']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline, ProductAttributeValueInline, ReviewInline]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        request._current_product = self.get_object(request, object_id)
        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # attributeهای دسته رو خودکار بساز
        if obj.category:
            for attr in obj.category.get_all_attributes():
                ProductAttributeValue.objects.get_or_create(
                    product=obj,
                    attribute=attr
                )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['__str__','is_active']
    search_fields = ['name']