from django.db import models
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    introduction = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user_id}: {self.username}'

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                value = [i.id for i in value] if self.pk else None
            if isinstance(f, DateTimeField):
                value = value.strftime('%Y/%m/%d %H:%M:%S') if value else None
            data[f.name] = value
        return data
