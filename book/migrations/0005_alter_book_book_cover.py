# Generated by Django 4.0.5 on 2022-06-08 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_rename_cover_book_book_cover_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_cover',
            field=models.ImageField(blank=True, null=True, upload_to='book_cover'),
        ),
    ]