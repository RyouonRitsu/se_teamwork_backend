from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    introduction = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user_id}: {self.username}'
