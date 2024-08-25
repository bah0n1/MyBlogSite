# Generated by Django 5.0.6 on 2024-08-15 10:55

import ckeditor_uploader.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAgentIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browser', models.CharField(max_length=500)),
                ('device', models.CharField(blank=True, default=None, max_length=500)),
                ('deviceOs', models.CharField(blank=True, default=None, max_length=500)),
                ('ip', models.CharField(max_length=50)),
                ('crawlers', models.BooleanField(default=False)),
                ('movie', models.BooleanField(default=False)),
                ('adult', models.BooleanField(default=False)),
                ('blacklist', models.BooleanField(default=False)),
                ('count', models.IntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=40)),
                ('bio', models.CharField(default='Not Given', max_length=150)),
                ('facebook', models.CharField(blank=True, max_length=150)),
                ('twitter', models.CharField(blank=True, max_length=150)),
                ('instagram', models.CharField(blank=True, max_length=150)),
                ('other', models.CharField(blank=True, max_length=150)),
                ('image', models.ImageField(upload_to='author_images/')),
                ('can_publish', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=30, unique=True)),
                ('titel', models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(10)])),
                ('meta_description', models.CharField(max_length=160, validators=[django.core.validators.MinLengthValidator(120)])),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images/')),
                ('viewed', models.PositiveIntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogApp.author')),
                ('categories', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='BlogApp.categories')),
                ('tags', models.ManyToManyField(to='BlogApp.tag')),
            ],
        ),
        migrations.CreateModel(
            name='UserOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
