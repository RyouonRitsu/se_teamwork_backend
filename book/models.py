from django.db import models
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField


# Create your models here.
class Book(models.Model):
    ISBN = models.CharField(max_length=20, primary_key=True)
    book_name = models.CharField(max_length=100)
    book_cover = models.ImageField(upload_to='book_cover', blank=True, null=True)
    introduction = models.TextField(blank=True)
    book_type = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    author_country = models.CharField(max_length=50, blank=True)
    press = models.CharField(max_length=50)
    published_date = models.DateField()
    page_number = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    score = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    heat = models.IntegerField(default=0)
    book_num_comments = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.ISBN}: {self.book_name}'

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
            if isinstance(f, models.ImageField):
                value = value.name if value else None
            data[f.name] = value
        return data
