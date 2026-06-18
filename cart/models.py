from django.db import models
from user.models import User
from product.models import ProductVariant, Product
from django.utils import timezone

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        pass

    def __str__(self):
        return f"سید خرید {self.user.username}"
    
    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_price(self, discount_amount=0):
        return sum(0, self.get_total() - discount_amount)
    
    def __len__(self):
        return sum(item.quantity for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'variant']

    def __str__(self):
        return f"{self.product.name} - {self.variant.color}"
    
    def get_total_price(self):
        return self.variant.price * self.quantity
    
class Discount(models.Model):

    PERCENT = 'percent'
    FIXED = 'fixed'

    DISCOUNT_TYPES = [
        (PERCENT, 'Percentage'),
        (FIXED, 'Fixed Amount'),
    ]

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPES,
        default=PERCENT
    )

    value = models.PositiveIntegerField()

    is_active = models.BooleanField(
        default=False
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    max_uses = models.PositiveIntegerField(
        default=0
    )

    allowed_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='allowed_discounts'
    )

    def __str__(self):
        return self.code

    def get_used_count(self):
        return self.usages.count()

    def is_valid(self, user=None):

        if not self.is_active:
            return False, 'کد تخفیف غیرفعال است'

        if self.expires_at and self.expires_at < timezone.now():
            return False, 'کد تخفیف منقضی شده است'

        if self.max_uses > 0 and self.get_used_count() >= self.max_uses:
            return False, 'کد تخفیف به حداکثر استفاده رسیده است'

        # if not user or not user.is_authenticated:
        #     return False, 'ابتدا وارد حساب کاربری شوید'

        if (
            self.allowed_users.exists()
            and not self.allowed_users.filter(id=user.id).exists()
        ):
            return False, 'شما مجاز به استفاده از این کد نیستید'

        if self.usages.filter(user=user).exists():
            return False, 'قبلاً از این کد استفاده کرده‌اید'

        return True, 'کد تخفیف معتبر است'

    def calculate_discount(self, total_price):

        if self.discount_type == self.PERCENT:
            return (total_price * self.value) / 100

        if self.discount_type == self.FIXED:
            return min(self.value, total_price)

        return 0
    
    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.lower().strip()
        super().save(*args, **kwargs)


class DiscountUsage(models.Model):

    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name='usages'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='discount_usages'
    )

    used_at = models.DateTimeField(
        auto_now_add=True
    )

    order_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ['discount', 'user']

    def __str__(self):
        return f'{self.user.username} - {self.discount.code}'
