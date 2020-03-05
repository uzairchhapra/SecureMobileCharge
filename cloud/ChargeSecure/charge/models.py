from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.
class UserOfApp(AbstractUser):
    uaddr= models.CharField(max_length=100)
    zip= models.CharField(max_length=6)
    state= models.CharField(max_length=100)
    city= models.CharField(max_length=100)
    phone= models.CharField(max_length=10)

class ChargeStation(models.Model):
    latitude = models.CharField(max_length=300)
    longitude = models.CharField(max_length=300)
    description = models.CharField(max_length=300,default="-")
    name = models.CharField(max_length=200, default='abc')
    # number_of_slots= models.IntegerField(default=0)
    # number_of_busy_slots= models.IntegerField(default=0)
    # number_of_broken_slots= models.IntegerField(default=0)

class Slot(models.Model):
    slot_number = models.IntegerField(default=0)
    cid = models.ForeignKey(ChargeStation, on_delete= models.CASCADE, db_column='cid')
    status = models.CharField(max_length=50, default='unused')

class Book(models.Model):
    uid = models.ForeignKey(UserOfApp, on_delete=models.CASCADE, db_column='uid')
    sid = models.ForeignKey(Slot, on_delete= models.CASCADE, db_column='sid')
    # book_start_time = models.DateTimeField(auto_now=True)
    # book_end_time = models.DateTimeField(null=False)
    phone_status = models.CharField(max_length=50, default='inside')
    action = models.CharField(max_length=50, default='close')
    action_time = models.DateTimeField(auto_now=True)
