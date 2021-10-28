from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # username, password, email, is_active, is_staff are already present in AbstractUser
    first_name = models.CharField(_('first name'), max_length=255, blank=True) #overwrite due to different max_length
    last_name = models.CharField(_('last name'), max_length=255, blank=True) #overwrite due to different max_length
    phone = models.CharField(max_length=13, blank = True)
    birthday = models.DateField(null=True)
    age = models.FloatField(null=True)
    language = models.CharField(max_length=2, default='EN')
    USER_STATUS_CHOICES = [
        ('RENTER', 'RENTER'),
        ('OWNER', 'OWNER')
    ]
    status = models.CharField(max_length=20, blank=True, choices=USER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()


class Build(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Flat(models.Model):
    build = models.ForeignKey(Build, on_delete=models.RESTRICT)
    room_count = models.IntegerField()
    type = models.CharField(max_length=20)
    price = models.FloatField()
    owner = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FlatRoom(models.Model):
    type = models.CharField(max_length=255)
    flat = models.ForeignKey(Flat, on_delete=models.RESTRICT, related_name='flat_rooms')
    description = models.TextField(blank=True)


class FlatAttribute(models.Model):
    name = models.CharField(max_length=256)


class FlatAttributesValue(models.Model):
    attribute = models.ForeignKey(FlatAttribute, on_delete=models.RESTRICT)
    flat_room = models.ForeignKey(FlatRoom, on_delete=models.CASCADE, related_name='flat_attributes')
    count = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class  RentOrder(models.Model):
    renter = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    flat = models.ForeignKey(Flat, on_delete=models.RESTRICT)
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.FloatField()

