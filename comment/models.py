from django.db import models

# Create your models here.
from django.db.models import ManyToManyField, DateTimeField


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    num_likes = models.IntegerField(default=0)
    num_dislikes = models.IntegerField(default=0)
    authorId = models.BigIntegerField(default=0, null=False)
    type = models.IntegerField(default=0, null=False)
    body_id = models.BigIntegerField(default=0, null=False)
    comment_num_comments = models.IntegerField(default=0)

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


class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    reason = models.TextField(null=False)
    title = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    reporter_id = models.BigIntegerField(default=0, null=False)
    comment_id = models.BigIntegerField(default=0, null=False)
