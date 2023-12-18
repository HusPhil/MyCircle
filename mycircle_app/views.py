from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, CreatePostForm, CreateCircleForm
from .models import Profile, Post, Message, ChatRoom, Circle

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
	# messages.error(request,'Please log in before you access this page')
	return redirect('sign_in')

def sign_up(request):
	form = CreateUserForm()
	
	if request.method == 'POST':
		form = CreateUserForm(request.POST)

		if form.is_valid():
			form.save()
			# messages.success(request,'SUCCESSFUL')
			return redirect('sign_in')
		# messages.error(request,'NOT SUCCESSFUL')
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
		form = CreateCircleForm(request.user)
		current_user_profile = request.user.profile 
		friends = current_user_profile.friend.exclude(user=request.user)
		context = {
			'user': request.user,
			'friends': friends,
			'profile': profile,
			'form': form,
		}
		return render(request, 'friends.html', context)
	messages.error(request,'Please log in before you access this page')
	return redirect('sign_in')
	

def messages(request):
    user = request.user
    circles = Circle.objects.filter(members=user)
    print(circles)

    chat_rooms = []
    for circle in circles:
        circle_chat_rooms = circle.chat_room
        chat_rooms.append(circle_chat_rooms)


    context = {
        # 'messages': messages,
        'chatrooms': chat_rooms,
    }
    return render(request, 'messages.html', context)



def view_convo(request, room_id):
    user = request.user
    circles = Circle.objects.filter(members=user)
    print(circles)

    chat_rooms = []
    for circle in circles:
        circle_chat_rooms = circle.chat_room
        chat_rooms.append(circle_chat_rooms)
    
    messages = Message.objects.filter(room_id=room_id)
    print(room_id)

    p_room_id = room_id

    context = {
        'chatrooms': chat_rooms,
        'messages': messages,
        'p_room_id': p_room_id,
    }
    return render(request, 'messages.html', context)


def create_circle(request):
    if request.method == 'POST':
        form = CreateCircleForm(request.user, request.POST)
        if form.is_valid():
            circle = form.save(commit=False)
            circle.save()
            profiles = form.cleaned_data['members']
            for profile in profiles:
                circle.members.add(profile.user)
            circle.members.add(request.user)
            circle.save()  # Save the Circle instance after adding members
            
            if not circle.name:
                circle.name = ", ".join([user.username for user in circle.members.all()])
                circle.save()
            
            return redirect('friends')
    else:
        form = CreateCircleForm(request.user)
    
    return render(request, 'friends.html', {'form': form})