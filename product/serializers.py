from rest_framework import serializers
from .models import Product, ProductVariant, ProductImage, ProductAttributeValue, Review, Tag

class productSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(read_only=True,source='main_image.image')
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','name','slug','main_image','price']

    def get_price(self,obj):
        variant : ProductVariant = obj.default_variant
        return variant.price if variant else None

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image','is_main','order']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id','color','color_code','price','stock','is_default']

class ProductAttrValueSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(source='attribute.name')

    class Meta:
        model = ProductAttributeValue
        fields = ['attribute','value']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Review
        fields = ['user','rating','comment','created_at']

class TagSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    class Meta:
        model = Tag
        fields = ['name']

class ProductDetailSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True)
    variants = ProductVariantSerializer(many=True)
    attributes = ProductAttrValueSerializer(source="attribute_values",many=True)
    reviews = ReviewSerializer(many=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = ["id","name","slug","description","visits","images","variants","attributes","reviews","tags"]