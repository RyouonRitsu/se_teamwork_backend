# Generated by Django 4.0.5 on 2022-06-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_book_heat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='cover',
            new_name='book_cover',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='name',
            new_name='book_name',
        ),
        migrations.AddField(
            model_name='book',
            name='book_num_comments',
            field=models.IntegerField(default=0),
        ),
    ]