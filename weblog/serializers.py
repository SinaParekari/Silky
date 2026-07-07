from rest_framework import serializers
from .models import WeblogCategory, WeblogText, WeblogReview, WeblogTag, Weblog
from user.serializers import UserProfielSerialization
from product.serializers import productSerializer
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = WeblogCategory
        fields = ["id", "title"]

class WeblogTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeblogText
        fields = ["id","template","header","text","order"]

class WeblogReviewSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = WeblogReview
        fields = ['full_name','comment','rating','created_at']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
class WeblogTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeblogTag
        fields = ['title']

class WeblogSerializer(serializers.ModelSerializer):
    user = UserProfielSerialization(read_only=True)
    category = CategorySerializer(read_only=True)
    texts = WeblogTextSerializer(many=True,read_only=True)
    likes = serializers.IntegerField(source="likes_count",read_only=True)
    products = productSerializer(many=True,read_only=True)
    reviews = WeblogReviewSerializer(
        many=True,
        read_only=True,
    )

    tags = WeblogTagSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Weblog
        fields = ['id','user','title','excerpt','slug','category','created_at','updated_at','readTime','views','image','summary','texts','tags','reviews','likes','products']