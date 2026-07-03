from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_name','variant_name','quantity','total_price']

class OrderSerializer(serializers.ModelSerializer):
    item = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id','user','status','discount_amount','final_price']