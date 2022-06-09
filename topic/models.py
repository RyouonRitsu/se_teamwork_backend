from django.db import models

# Create your models here.

# create a new class called Topic



class Topic(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic_name = models.CharField(max_length=200, null=False)
    topic_heat = models.IntegerField(default=0)
    topic_num_members = models.IntegerField(default=0)
    topic_create_date = models.DateTimeField(auto_now_add=True)
    topic_description = models.TextField()

    def __str__(self):
        return self.topic_name

    def to_dict(self):
        return {
            'id': self.id,
            'topic_name': self.topic_name,
            'topic_heat': self.topic_heat,
            'topic_num_members': self.topic_num_members,
            'topic_create_date': self.topic_create_date,
            'topic_description': self.topic_description
        }


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

    def to_dict(self):
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'title': self.diary_title,
            'content': self.diary_content,
            'create_time': self.diary_create_time,
            'heat': self.diary_heat,
            'author': self.diary_authorId,
            'likes': self.likes,
            'dislikes': self.dislikes,
            'num_comments': self.diary_num_comments
        }


class Topic_Members(models.Model):
    topic_id = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField(default=0)
    member_since = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
