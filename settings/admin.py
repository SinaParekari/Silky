from django.contrib import admin
from .models import settings
# Register your models here.

@admin.register(settings)
class settingsAdmin(admin.ModelAdmin):
    list_display = ['support_phone_number','is_default','sattisfied_customer','sattisfy_percent','number_of_products']
    list_filter = ['sattisfied_customer','sattisfy_percent','number_of_products']
