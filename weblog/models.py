from django.db import models
from user.models import User
import os, uuid
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from product.models import Product

# Create your models here.


def upload_weblog_image(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"weblogs/{instance.slug}-{uuid.uuid4().hex}{ext}"

class WeblogManager(models.Manager):
    def get_active_weblogs(self):
        return self.get_queryset().filter(is_active=True)

    def get_weblog_by_slug(self, slug):
        return self.get(slug=slug, is_active=True)

    def get_weblog_by_category(self, category):
        return self.filter(category__title=category,is_active=True)
    

class WeblogCategory(models.Model):
    title = models.CharField( max_length=20)

    def __str__(self):
        return self.title
    
class Weblog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weblogs")
    title = models.CharField( max_length=50)
    excerpt = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, allow_unicode=True)
    is_active = models.BooleanField(default=False)
    category = models.ForeignKey(WeblogCategory,on_delete=models.CASCADE, related_name="weblogs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    readTime = models.PositiveIntegerField(default=5)
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=upload_weblog_image)
    summary = models.CharField(max_length=100)

    objects = WeblogManager()

    def __str__(self):
        return self.title

class WeblogText(models.Model):
    class Choices(models.TextChoices):
        simple = "simple"
        simple_ul = "simple_ul"
        purple = "purple"
        blue = "blue"
        yellow = "yellow"
        green = "green"

    weblog = models.ForeignKey(Weblog, on_delete=models.CASCADE, related_name="texts")
    template = models.CharField(max_length=20,choices=Choices.choices,default=Choices.simple)
    header = models.TextField(max_length=40, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.weblog.title} - {self.order}"
    
class WeblogReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weblog = models.ForeignKey(Weblog, on_delete=models.CASCADE,related_name="reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ['user', 'weblog']  

    def __str__(self):
        return f"{self.weblog.title} - {self.user.first_name} {self.user.last_name}"  
    
class WeblogLike(models.Model):
    weblog = models.ForeignKey(Weblog,on_delete=models.CASCADE,related_name="likes")

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("weblog", "user")
    
class WeblogTag(models.Model):
    title = models.CharField(max_length=20)
    weblog = models.ManyToManyField(Weblog, related_name='tags')

    def __str__(self):
        return self.title
    
class WeblogRelatedProduct(models.Model):
    weblog = models.ForeignKey(
        Weblog,
        on_delete=models.CASCADE,
        related_name="related_products",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="related_weblogs",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ("weblog", "product")

    def __str__(self):
        return f"{self.weblog.title} -> {self.product.name}"

