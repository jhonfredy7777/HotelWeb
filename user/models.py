from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=50, null=True)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
