# admin.py
from django.contrib import admin
from .models import UserAgentIP,Tag,Post,Author,Categories,UserOtp

admin.site.register(UserAgentIP)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Categories)
admin.site.register(UserOtp)
