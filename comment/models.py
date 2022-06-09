from django.db import models

# Create your models here.



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


class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    reason = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    reporter_id = models.BigIntegerField(default=0, null=False)
    comment_id = models.BigIntegerField(default=0, null=False)
