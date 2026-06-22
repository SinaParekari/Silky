import os, random
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

# Create your models here.

def get_file_extension(file):
    base_name = os.path.basename(file)
    name ,ext = os.path.splitext(base_name)
    return name , ext

def upload_image(instance : AbstractUser, filename):
    rand_name = random.randint(1,10000)
    name ,ext = get_file_extension(filename)
    final_name = f'{instance.id}-{instance.username}-{rand_name}{ext}'
    return f'avatars/{final_name}'

class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True) 
    phone_number = PhoneNumberField(unique=True, region="IR",blank=True,null=True)
    avatar = models.ImageField(upload_to=upload_image, blank=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        pass

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    address = models.CharField(max_length=255)
    building_number = models.CharField(max_length=10)
    unit = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=10,
        validators=[
        RegexValidator(
            r'^\d{10}$',
            'Postal code must be 10 digits'
        )
    ]
    )

    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city} - {self.address}"