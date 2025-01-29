from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Offer, Order, Profiles (evtl auch in user_auth), Review



class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Untitled Offer")  
    image = models.FileField(upload_to='offers/', null=True, blank=True)    
    description = models.TextField(max_length=255, default="No description provided")  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Details(models.Model):
    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Untitled Detail")  
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(null=True, blank=True, default=1)  
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50, null=True, blank=True, default="basic")  


# class Offer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     image = models.FileField(upload_to='offers/', null=True, blank=True)    
#     description = models.TextField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     min_price = models.DecimalField(max_digits=10, decimal_places=2)
#     min_delivery_time = models.IntegerField()


# class Details(models.Model):
#     offer = models.ForeignKey('Offer', related_name='details', on_delete=models.CASCADE)
#     url = models.URLField()

