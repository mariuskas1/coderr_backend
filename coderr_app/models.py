from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Offer, Order, Profiles (evtl auch in user_auth), Review


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', null=True, blank=True)    
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_delivery_time = models.IntegerField()


class Details(models.Model):
    offer = models.ForeignKey('Offer', related_name='details', on_delete=models.CASCADE)
    url = models.URLField()

