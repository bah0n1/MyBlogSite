# Generated by Django 5.0.6 on 2024-08-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.CharField(blank=True, default=None, max_length=40),
        ),
    ]
