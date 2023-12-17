from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class CreatePostForm(forms.ModelForm):

	class Meta(object):
		model = Post
		fields = ['body', 'img',]
		labels = {
			'body': "Enter caption",
			'img': "Upload image",
		}
		widget = {
			'body': forms.widgets.TextInput(attrs={"placeholder": "Enter your caption"}),
		}
		exclude = ('user',)

			




	# user = models.ForeignKey(User, related_name="post", on_delete=models.DO_NOTHING)
	# body = models.TextField(blank=True)
	
	# created_at = models.DateTimeField(auto_now_add=True)


class CreateUserForm(UserCreationForm):
	class Meta():
		model = User 
		fields = [
			'username',
			'email',
			'password1',
			'password2',
		]
			

