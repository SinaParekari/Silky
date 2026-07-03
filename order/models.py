from django.db import models
from user.models import User
from cart.models import Discount
from product.models import Product, ProductVariant
# Create your models here.

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING) 

    total_price = models.PositiveBigIntegerField()

    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)

    discount_amount = models.PositiveBigIntegerField(default=0)

    final_price = models.PositiveBigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=50)

    variant_name = models.CharField(max_length=50)

    variant_price = models.PositiveBigIntegerField()

    quantity = models.IntegerField()

    total_price = models.PositiveBigIntegerField()

    def __str__(self):
        return self.product.name