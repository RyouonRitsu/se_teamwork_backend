# Generated by Django 3.2.5 on 2022-06-09 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_comment_comment_num_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='title',
            field=models.TextField(default=''),
        ),
    ]
