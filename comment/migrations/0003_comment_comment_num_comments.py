# Generated by Django 3.2.5 on 2022-06-09 00:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('comment', '0002_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_num_comments',
            field=models.IntegerField(default=0),
        ),
    ]
