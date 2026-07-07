from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class settings(models.Model):
    support_phone_number = models.CharField(max_length=30)
    number_of_products = models.IntegerField(default=500)
    brand_count = models.IntegerField(default=100)
    sattisfied_customer = models.IntegerField(default=4)
    sattisfy_percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    support_email = models.EmailField(default="support@example.com")
    telegram_id = models.CharField(max_length=20)

    instagram_link = models.CharField(max_length=100)
    telegram_link = models.CharField(max_length=100)
    youtube_link = models.CharField(max_length=100)
    twitter_link = models.CharField(max_length=100)

    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            settings.objects.exclude(pk=self.pk).filter(is_default=True).update(is_default=False)

        super().save(*args, **kwargs)