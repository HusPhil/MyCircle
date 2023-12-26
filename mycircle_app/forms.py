from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Circle, Profile, ProfilePicture, BackgroundPicture



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

class CreateCircleForm(forms.ModelForm):
    class Meta:
        model = Circle
        fields = ['name', 'members']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_user_profile = Profile.objects.get(user=user)
        self.fields['members'].queryset = current_user_profile.friend.exclude(user=user)

class CreateUserForm(UserCreationForm):
	class Meta():
		model = User 
		fields = [
			'username',
			'email',
			'password1',
			'password2',
		]

class FriendRequestForm(forms.Form):
	user_id = forms.CharField(widget=forms.TextInput, required=True, label="Enter User ID")
	# message = forms.CharField(widget=forms.TextInput, required=False)

class UploadProfilePic(forms.ModelForm):
	class Meta:
		model = ProfilePicture
		fields = ('img',)

class UploadBackgroundPic(forms.ModelForm):
	class Meta:
		model = BackgroundPicture
		fields = ('img',)