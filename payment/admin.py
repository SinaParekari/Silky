from django.contrib import admin
from .models import Payment
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["__str__",'amount','status','paid_at']
    search_fields = ['status','track_id','amount']
    list_filter = ['status']
