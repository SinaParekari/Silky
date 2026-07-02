from rest_framework import serializers
from .models import CartItem, Cart

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source="product.name")
    variant = serializers.CharField(source="variant.color")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product','variant','quantity','total_price']

    def get_total_price(self,obj):
        return obj.get_total_price()
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_item = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id','items','total_item','total_price']

    def get_total_price(self, obj):
        return obj.get_total()
    
    def get_total_item(self, obj):
        return len(obj)
    
class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

class DiscountSerializer(serializers.Serializer):
    code = serializers.CharField()
