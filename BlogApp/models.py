from django.db import models
import os
from django.core.validators import MinLengthValidator
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


class UserAgentIP(models.Model):
    browser=models.CharField(max_length=500)
    device=models.CharField(max_length=500,blank=True,default=None)
    deviceOs=models.CharField(max_length=500,blank=True,default=None)
    ip=models.CharField(max_length=50)
    crawlers=models.BooleanField(default=False)
    movie=models.BooleanField(default=False)
    adult=models.BooleanField(default=False)
    blacklist=models.BooleanField(default=False)
    count=models.IntegerField()
    time=models.DateTimeField(auto_now_add=True, blank=True)
    

    def __str__(self):
        return self.ip


    



class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)  # Tag name with a maximum length of 30 characters

    def __str__(self):
        return self.name
class Author(models.Model):
    url=models.CharField(max_length=40,blank=True,default=None)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    name = models.CharField(max_length=40)
    bio=models.CharField(max_length=150,blank=False,default="Not Given")
    facebook=models.CharField(max_length=150,blank=True)
    twitter=models.CharField(max_length=150,blank=True)
    instagram=models.CharField(max_length=150,blank=True)
    other=models.CharField(max_length=150,blank=True)
    image = models.ImageField(upload_to='author_images/')
    can_publish=models.BooleanField(default=False)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.startswith(self.url):
            # Get the file extension
            extension = os.path.splitext(self.image.name)[1]
            # Rename the file
            self.image.name = f"{self.url}{extension}"
            #check the name is exit or not if exit remove the old one
        super().save(*args, **kwargs)
class Categories(models.Model):
    name = models.CharField(max_length=40, unique=True)
    def __str__(self):
        return self.name
class Post(models.Model):
    url=models.CharField(max_length=30,unique=True)
    titel = models.CharField(max_length=60, validators=[MinLengthValidator(10)])  # Title with a max length of 60 and min length of 50
    meta_description = models.CharField(max_length=160, validators=[MinLengthValidator(120)])  # Meta description with a max length of 155 and min length of 120
    description = RichTextUploadingField()  # Full description of the post
    categories=models.ForeignKey(Categories,on_delete=models.CASCADE,blank=True)
    tags = models.ManyToManyField(Tag)  # Many-to-many relationship with the Tag model, with limit choices
    last_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    viewed=models.PositiveIntegerField()
    def __str__(self):
        return self.titel
    def increment_view_count(self):
        self.viewed += 1
        self.save(update_fields=['viewed'])

    def save(self, *args, **kwargs):
        if not self.pk:
            # If the post is being created, set the initial last_updated timestamp
            self.last_updated = models.DateTimeField(auto_now=True)
        super(Post, self).save(*args, **kwargs)


class UserOtp(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.IntegerField()

    def __str__(self):
        return self.user.email
    



