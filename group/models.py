from django.db import models

# Create your models here.
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_name = models.CharField(max_length=200, null=False)
    group_description = models.TextField(max_length=1000)
    group_created_date = models.DateTimeField(auto_now_add=True)
    group_heat = models.IntegerField(default=0)
    group_num_members = models.IntegerField(default=0)
    group_rules = models.TextField()
    num_of_posts = models.IntegerField(default=0)
    group_picture_url = models.CharField(max_length=200, null=True)
    group_cover = models.ImageField(upload_to='book_cover', blank=True, null=True)

    def __str__(self):
        return self.group_name

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


# create a class called Group_Member that inherits from the models.Model class
class Group_Members(models.Model):
    group_id = models.BigIntegerField(null=False, default=0)
    user_id = models.BigIntegerField(null=False, default=0)
    member_since = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.BigIntegerField(null=False, default=0)
    post_title = models.CharField(max_length=200, null=False)
    post_content = models.TextField(null=False)
    post_create_time = models.DateTimeField(auto_now_add=True)
    post_heat = models.IntegerField(default=0)
    post_num_comments = models.IntegerField(default=0)
    post_authorId = models.BigIntegerField(null=False, default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.post_title

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
