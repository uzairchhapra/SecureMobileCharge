from django.db import models

# Create your models here.
class ChargeStation(models.Model):
    latitude = models.CharField(max_length=300)
    longitude = models.CharField(max_length=300)
