from django.db import models
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField


# Create your models here.
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=100)
    movie_cover = models.ImageField(upload_to='movie_cover', blank=True, null=True)
    introduction = models.TextField(blank=True)
    movie_form = models.CharField(max_length=100, blank=True)
    movie_type = models.CharField(max_length=50)
    area = models.CharField(max_length=100)
    release_date = models.DateField()
    director = models.CharField(max_length=100)
    screenwriter = models.CharField(max_length=100)
    starring = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    duration = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.movie_id}: {self.movie_name}'

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
                value = value.path if value else None
            data[f.name] = value
        return data
