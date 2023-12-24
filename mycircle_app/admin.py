from django.contrib import admin
from . models import Profile, Post, Message, ChatRoom, Circle, FriendRequest, ProfilePicture

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(Circle)
admin.site.register(FriendRequest)
admin.site.register(ProfilePicture)