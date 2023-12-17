from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, CreatePostForm
from .models import Profile, Post

# Create your views here.
def home(request):
	form = CreatePostForm(request.POST, request.FILES)
	if request.user.is_authenticated:
		current_user_profile = request.user.profile 
		friends = current_user_profile.friend.all()
		posts = Post.objects.all()

		if request.method == 'POST':

			if form.is_valid():
				post = form.save(commit=False)
				post.user = request.user
				post.save()
				return redirect('home')

		context = {
			'user': request.user,
			'friends': friends,
			'form': form,
			'posts': posts
		}
		return render(request, 'home.html', context)
	messages.error(request,'Please log in before you access this page')
	return redirect('sign_in')

def sign_up(request):
	form = CreateUserForm()
	
	if request.method == 'POST':
		form = CreateUserForm(request.POST)

		if form.is_valid():
			form.save()
			messages.success(request,'SUCCESSFUL')
			return redirect('sign_in')
		messages.error(request,'NOT SUCCESSFUL')
	context = {
		'form': form
	}
	
	return render(request, 'sign_up.html', context)

def sign_in(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)

		if user:
			login(request, user)
			return redirect('/')
		messages.error(request, 'Wrong username or password')

	return render(request, 'sign_in.html')
	

def sign_out(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('sign_in')
	messages.error(request,'Please log in before you access this page')
	return redirect('sign_in')


def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		context = {'profile': profile}

		return render(request, 'profile.html', context)
	messages.error(request,'Please log in before you access this page')
	return redirect('sign_in')

	


def friends(request):
	if request.user.is_authenticated:
		current_user_profile = request.user.profile 
		friends = current_user_profile.friend.exclude(user=request.user)
		context = {
			'user': request.user,
			'friends': friends
		}
		return render(request, 'friends.html', context)
	messages.error(request,'Please log in before you access this page')
	return redirect('sign_in')
	

def messages(request):
	return render(request, 'messages.html')