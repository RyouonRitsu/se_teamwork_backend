from django.db import models

# Create your models here.

# create a new class called Topic
from django.db.models import ManyToManyField, DateTimeField


class Topic(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic_name = models.CharField(max_length=200, null=False)
    topic_heat = models.IntegerField(default=0)
    topic_num_members = models.IntegerField(default=0)
    topic_create_date = models.DateTimeField(auto_now_add=True)
    topic_description = models.TextField()

    def __str__(self):
        return self.topic_name

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

class Diary(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic_id = models.BigIntegerField(default=0)
    diary_title = models.CharField(max_length=200, null=False)
    diary_content = models.TextField(null=False)
    diary_create_time = models.DateTimeField(auto_now_add=True)
    diary_heat = models.IntegerField(default=0)
    diary_authorId = models.BigIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    diary_num_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.diary_title

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


class Topic_Members(models.Model):
    topic_id = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField(default=0)
    member_since = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
