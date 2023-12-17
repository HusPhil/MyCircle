from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
from django.contrib.auth.models import AbstractUser

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

class CustomUser(AbstractUser):
    # Define a field for the UUID as the primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user',
    )

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	friend = models.ManyToManyField(
			'self',
			related_name='friend_of',
			# symmetrical=True,
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