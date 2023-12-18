from django.contrib import admin
from . models import Profile, Post, Message, ChatRoom

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(ChatRoom)
admin.site.register(Message)