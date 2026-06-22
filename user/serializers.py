from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address


User = get_user_model()

class UserProfielSerialization(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','phone_number','avatar','national_code','birth_date']

        read_only_fields = ['id','email']

class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

        read_only_fields = ['id','user','created_at']
    
    def validate(self, attrs):

        request = self.context['request']
        user = request.user

        if Address.objects.filter(user=user).count() >= 3:
            raise serializers.ValidationError(
                "you reached maximum addresses"
            )

        return attrs
    

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("this username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("this email already exists.")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({
                'confirm_password': 'passwords do not match'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user

#for login
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            raise Exception("Invalid email or password")

        data = super().validate(attrs)
        return data
    
#logout
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        RefreshToken(self.validated_data['refresh']).blacklist()