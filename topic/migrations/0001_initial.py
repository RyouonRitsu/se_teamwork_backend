# Generated by Django 3.2.5 on 2022-06-07 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('topic_id', models.BigIntegerField(default=0)),
                ('diary_title', models.CharField(max_length=200)),
                ('diary_content', models.TextField()),
                ('diary_create_time', models.DateTimeField(auto_now_add=True)),
                ('diary_heat', models.IntegerField(default=0)),
                ('diary_authorId', models.BigIntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('diary_num_comments', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('topic_name', models.CharField(max_length=200)),
                ('topic_heat', models.IntegerField(default=0)),
                ('topic_num_members', models.IntegerField(default=0)),
                ('topic_create_date', models.DateTimeField(auto_now_add=True)),
                ('topic_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Topic_Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_id', models.BigIntegerField(default=0)),
                ('user_id', models.BigIntegerField(default=0)),
                ('member_since', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
    ]