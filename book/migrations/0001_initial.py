# Generated by Django 4.0.5 on 2022-06-06 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('ISBN', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('cover', models.CharField(max_length=500)),
                ('introduction', models.TextField(blank=True)),
                ('type', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('author_country', models.CharField(max_length=50)),
                ('press', models.CharField(max_length=50)),
                ('published_date', models.DateField()),
                ('page_number', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('score', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('heat', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]