# Generated by Django 4.0.5 on 2022-06-09 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_cover',
            field=models.ImageField(blank=True, null=True, upload_to='../se_teamwork/src/assets/movie_cover'),
        ),
    ]