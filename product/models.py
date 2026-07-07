import os, uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from category.models import Category, CategoryAttribute
from user.models import User


def upload_product_image(instance, filename):
    base, ext = os.path.splitext(filename)
    return f'products/{instance.product.slug}-{uuid.uuid4().hex}{ext}'

class ProductManager(models.Manager):
    def get_active_products(self):
        return self.get_queryset().filter(is_active=True)
    
    def get_product_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug, is_active=True)
        if qs.count() == 1:
            return qs.first()
        
    def get_products_by_category(self, category):
        return (self.get_active_products().filter(category_id__in=category.get_descendants_ids()))
    
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visits = models.IntegerField(default=0)

    objects = ProductManager()

    class Meta:
        pass

    def __str__(self):
        return self.name

    @property
    def main_image(self):
        image = self.images.filter(is_main=True).first()
        return image or self.images.first()

    @property
    def default_variant(self):
        return (
            self.variants.filter(is_default=True).first()
            or self.variants.first()
        )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_product_image)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.product.name} - عکس {self.order}'

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50)
    color_code = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                r'^#[0-9A-Fa-f]{6}$',
                'Enter a valid HEX color.'
            )
        ]
    )
    price = models.DecimalField(max_digits=12, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'variant'
        verbose_name_plural = 'variant ها'

    def __str__(self):
        return f'{self.product.name} - {self.color}'

    @property
    def is_available(self):
        return self.stock > 0


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    class Meta:
        unique_together = ['product', 'attribute'] 

    def __str__(self):
        return f'{self.product.name} - {self.attribute.name}: {self.value}'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'user'] 

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.rating}'
    
class Tag(models.Model):
    name = models.CharField(max_length=20)
    product = models.ManyToManyField(Product, blank=True, related_name='tags')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    