from django.db import models



# Create your models here.
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

    def __str__(self):
        return self.group_name

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            'group_description': self.group_description,
            'group_created_date': self.group_created_date,
            'group_heat': self.group_heat,
            'group_num_members': self.group_num_members,
            'group_rules': self.group_rules,
            'num_of_posts': self.num_of_posts,
            'group_picture_url': self.group_picture_url
        }


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

    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'title': self.post_title,
            'content': self.post_content,
            'create_time': self.post_create_time,
            'heat': self.post_heat,
            'authorId': self.post_authorId,
            'likes': self.likes,
            'dislikes': self.dislikes,
            'num_comments': self.post_num_comments
        }
