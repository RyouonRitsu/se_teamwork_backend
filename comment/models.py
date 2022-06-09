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

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'date': self.date,
            'num_likes': self.num_likes,
            'num_dislikes': self.num_dislikes,
            'authorId': self.authorId,
            'type': self.type,
            'body_id': self.body_id,
            'comment_num_comments': self.comment_num_comments
        }


class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    reason = models.TextField(null=False)
    title = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    reporter_id = models.BigIntegerField(default=0, null=False)
    comment_id = models.BigIntegerField(default=0, null=False)
