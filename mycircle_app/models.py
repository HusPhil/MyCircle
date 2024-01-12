from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid

# Create your models here.
class Post(models.Model):
	user = models.ForeignKey(User, related_name="post", on_delete=models.DO_NOTHING)
	body = models.TextField(blank=True)
	img = models.ImageField(blank=True, null=True, upload_to='uploaded_images/')
	created_at = models.DateTimeField(auto_now_add=True)

	def clean(self):
		if not (self.body or self.img):
			raise ValidationError("You cannot leave img and body blank!")

	def __str__(self):
		return f"{self.user} ({self.created_at:%Y-%m-%d %H:%M}): {self.body}.."

#CHAT SYSTEM

class Circle(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	members = models.ManyToManyField(User, related_name='circles')
	img = models.ImageField(default='circle_default.png', upload_to='uploaded_circle_img/')
	created_at = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=100, blank=True)
	type = models.TextField(default="standard", blank=True)

	def __str__(self):
		return f"{(self.type.upper())}:__:{self.name}" or f"Circle {self.pk}"

class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    circle = models.OneToOneField('Circle', on_delete=models.CASCADE, related_name='chat_room', null=True)

    def save(self, *args, **kwargs):
        if not self.name and self.circle:
            user_list = ", ".join([user.username for user in self.circle.members.all()])
            self.name = user_list
        super(ChatRoom, self).save(*args, **kwargs)

    def __str__(self):
        return self.name or f"(ChRm) {self.circle.name}"

def create_chatroom(sender, instance, created, **kwargs):
	if created:
		chat_room = ChatRoom.objects.create(circle=instance)
		chat_room.name = f"Chat Room for {instance}" 
post_save.connect(create_chatroom, sender=Circle)

class Message(models.Model):
	room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.sender.username} - {self.timestamp}"

class Profile(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	friend = models.ManyToManyField(
			'self',
			blank=True,
		)

	def __str__(self):
		return self.user.username

	

def create_profile(sender, instance, created, **kwargs): 
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

		user_profile.friend.set([instance.profile.id])
		user_profile.save()

		new_profile_pic = ProfilePicture.objects.create(user_profile=user_profile, img='blank_img.png')
		new_profile_pic.save()

		new_background_pic = BackgroundPicture.objects.create(user_profile=user_profile)
		new_background_pic.save()


post_save.connect(create_profile, sender=User)

class FriendRequest(models.Model):
	sender = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('sender', 'receiver')

class ProfilePicture(models.Model):
	user_profile = models.OneToOneField('Profile', on_delete=models.CASCADE, related_name='profile_picture', null=True)
	img = models.ImageField(default='blank_img.png', upload_to='uploaded_profile_pics/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(f"PF: {self.user_profile.user.username}")

def change_profile_imgfile(sender, instance, **kwargs):
	instance.img = sender.img
pre_delete.connect(change_profile_imgfile, sender=ProfilePicture)

class BackgroundPicture(models.Model):
	user_profile = models.OneToOneField('Profile', on_delete=models.CASCADE, related_name='background_picture', null=True)
	img = models.ImageField(default='blank_img.png', upload_to='uploaded_background_pics/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(f"BG: {self.user_profile.user.username}")

def change_background_imgfile(sender, instance, **kwargs):
    instance.img = sender.img
pre_delete.connect(change_background_imgfile, sender=BackgroundPicture)

