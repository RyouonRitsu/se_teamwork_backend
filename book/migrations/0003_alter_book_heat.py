# Generated by Django 4.0.5 on 2022-06-06 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_rename_type_book_book_type_alter_book_author_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='heat',
            field=models.IntegerField(default=0),
        ),
    ]
