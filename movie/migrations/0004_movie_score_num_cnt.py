# Generated by Django 4.0.5 on 2022-06-10 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_alter_movie_movie_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='score_num_cnt',
            field=models.IntegerField(default=0),
        ),
    ]