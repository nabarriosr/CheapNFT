from django.db import models

# Create your models here.

class Bid(models.Model):
    seller_address = models.CharField(max_length=42)
    seller_sign = models.TextField()
    buyer_address = models.CharField(max_length=42)
    buyer_sign = models.TextField()
    nft_id= models.BigIntegerField()
    price = models.BigIntegerField()
    timestamp_publish = models.BigIntegerField()
    timestamp_close = models.BigIntegerField()
    status = models.CharField(max_length=42)
    ready= models.BooleanField()