from django.db import models
from django.db.models.signals import post_save
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
	members = models.ManyToManyField(User, related_name='circles')
	created_at = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=100, blank=True)  # Making name field optional

	def __str__(self):
		return self.name or f"Circle {self.id}"

	def save(self, *args, **kwargs):
		if not self.name and self.members.exists():
			# Create the default name based on member usernames
			user_list = ", ".join([user.username for user in self.members.all()])
			self.name = f"{user_list}'s Circle"
		super().save(*args, **kwargs)

class ChatRoom(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255, blank=True, null=True)
	users = models.ManyToManyField(User, related_name='rooms')
	

	def save(self, *args, **kwargs):
		if not self.name:
			# Create the default name as a comma-separated list of user usernames
			user_list = ", ".join([user.username for user in self.users.all()])
			self.name = user_list
		super(ChatRoom, self).save(*args, **kwargs)

	def __str__(self):
		return self.name or f"Chat Room {self.id}"
		
class Message(models.Model):
	room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.sender.username} - {self.timestamp}"


class Profile(models.Model):
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

post_save.connect(create_profile, sender=User)

