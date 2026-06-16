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
    
    def get_totoal_price(self):
        return self.variant.color * self.quantity
    
class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    max_uses = models.PositiveIntegerField(default=0)

    allowed_users = models.ManyToManyField(User, blank=True , related_name='allowed_discounts')
    class Meta:
        pass

    def __str__(self):
        return self.code

    def is_valid(self, user=None):
        # چک فعال بودن
        if not self.is_active:
            return False, 'کد تخفیف غیرفعال است'

        # چک تاریخ انقضا
        if self.expires_at and self.expires_at < timezone.now():
            return False, 'کد تخفیف منقضی شده است'

        # چک حداکثر استفاده کل
        if self.max_uses > 0 and self.get_used_count() >= self.max_uses:
            return False, 'کد تخفیف به حداکثر استفاده رسیده است'

        if user and user.is_authenticated:
            # چک کاربر مجاز
            if self.allowed_users.exists() and not self.allowed_users.filter(id=user.id).exists():
                return False, 'شما مجاز به استفاده از این کد نیستید'

            # چک استفاده قبلی این کاربر
            if self.usages.filter(user=user).exists():
                return False, 'شما قبلاً از این کد تخفیف استفاده کرده‌اید'
        else:
            return False, 'برای استفاده از کد تخفیف باید وارد شوید'

        return True, 'کد تخفیف معتبر است'

    def get_used_count(self):
        return self.usages.count()
    
class DiscountUsage(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discount_usages')
    used_at = models.DateTimeField(auto_now_add=True)

    # وقتی سفارش ثبت شد اینجا ذخیره میشه
    order_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'استفاده از تخفیف'
        verbose_name_plural = 'استفاده‌های تخفیف'
        unique_together = ['discount', 'user']  # هر کاربر فقط یکبار

    def __str__(self):
        return f'{self.user.username} - {self.discount.code}'

