# Generated by Django 3.2.5 on 2022-06-07 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('num_likes', models.IntegerField(default=0)),
                ('num_dislikes', models.IntegerField(default=0)),
                ('authorId', models.BigIntegerField(default=0)),
                ('type', models.IntegerField(default=0)),
                ('body_id', models.BigIntegerField(default=0)),
            ],
        ),
    ]
