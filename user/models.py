import os, random
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

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

class User(AbstractUser):
    email = models.EmailField(unique=True) 
    phone_number = PhoneNumberField(unique=True, region="IR")
    avatar = models.ImageField(upload_to=upload_image, blank=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    province = models.CharField(max_length=50) #TODO : this field needs to be choice box
    city = models.CharField(max_length=50) #TODO : this field needs to be choice box
    address = models.CharField(max_length=100)
    building_number = models.CharField(max_length=10)
    unit = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    #TODO: wallet

    #this method stops two or more addresses is_default value in True for one user
    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Address'

    def __str__(self):
        return f'{self.user.username} - {self.postal_code}'