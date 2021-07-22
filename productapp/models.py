from django.db import models

# Create your models here.
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Product(models.Model):
    name = models.CharField(max_length=12)
    weight = models.CharField(max_length=45)
    price = models.CharField(max_length=34)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name