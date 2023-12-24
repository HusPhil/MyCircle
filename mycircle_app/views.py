from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
import json
from django.core.serializers.json import DjangoJSONEncoder

from .forms import CreateUserForm, CreatePostForm, CreateCircleForm, FriendRequestForm, UploadProfilePic
from .models import Profile, Post, Message, ChatRoom, Circle, FriendRequest
from django.contrib import messages

# Create your views here.
def home(request):
	if request.user.is_authenticated:
		form = CreatePostForm(request.POST, request.FILES)
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
		profile_pic_form = UploadProfilePic(request.POST or None, request.FILES or None)

		if profile_pic_form.is_valid():
			profile_pic_form.save()
			return JsonResponse({'message': 'works'})
		
		profile = Profile.objects.get(id=pk)
		user_friends = Profile.objects.get(user=request.user)

		context = {
			'profile_pic_form': profile_pic_form,
			'profile': profile,
			'user_friends': user_friends,
			'result': None,
		}

		return render(request, 'profile.html', context)
	messages.error(request,'Please log in before you access this page')
	return redirect('sign_in')

def friends(request):
	if request.user.is_authenticated:
		fr_form = FriendRequestForm()
		circle_form = CreateCircleForm(request.user)
		current_user_profile = request.user.profile 
		friends = current_user_profile.friend.exclude(user=request.user)
		sent_fr_list = FriendRequest.objects.filter(sender=request.user)
		received_fr_list = FriendRequest.objects.filter(receiver=request.user)
		# print(friend_requests)
		context = {
			'sent_fr_list': sent_fr_list,
			'received_fr_list': received_fr_list,
			'friends': friends,
			'profile': profile,
			'circle_form': circle_form,
			'fr_form': fr_form,
		}
		return render(request, 'friends.html', context)
	messages.error(request,'Please log in before you access this page')
	return redirect('sign_in')
	
def view_messages(request):
	if request.user.is_authenticated:
	    user = request.user
	    circles = Circle.objects.filter(members=user)

	    chat_rooms = []
	    for circle in circles:
	        circle_chat_rooms = circle.chat_room
	        chat_rooms.append(circle_chat_rooms)

	    context = {
	       
	        'chatrooms': chat_rooms,
	       
	    }

	    return render(request, 'messages.html', context)
	return redirect('sign_in')


# Create your action functions here

def view_convo(request, room_id):
	if request.user.is_authenticated:
	    user = request.user
	    circles = Circle.objects.filter(members=user)


	    chat_rooms = []
	    for circle in circles:
	        circle_chat_rooms = circle.chat_room
	        chat_rooms.append(circle_chat_rooms)
	    
	    messages = Message.objects.filter(room_id=room_id)
	    m_room = ChatRoom.objects.get(id=room_id)

	    context = {
	        'chatrooms': chat_rooms,
	        'messages': messages,
	        'room': m_room,
	    }
	    return render(request, 'messages.html', context)
	return redirect('sign_in')

def create_circle(request):
	if request.user.is_authenticated:
	    if request.method == 'POST':
	        form = CreateCircleForm(request.user, request.POST)
	        if form.is_valid():
	            circle = form.save(commit=False)
	            circle.save()
	            circle.members.add(request.user)
	            profiles = form.cleaned_data['members']
	            for profile in profiles:
	                circle.members.add(profile.user)
	            circle.save()  # Save the Circle instance after adding members
	            
	            if not circle.name:
	                circle.name = ", ".join([user.username for user in circle.members.all()])
	                circle.save()
	            
	            return redirect('friends')
	    else:
	        form = CreateCircleForm(request.user)
	    
	    return render(request, 'friends.html', {'form': form})
	return redirect('sign_in')

def send_message(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			room_id = request.POST.get('room_id')
			m_content = request.POST.get('message')
			m_room = ChatRoom.objects.get(id=room_id)
			
			# print(m_room.circle.name)
			new_message = Message.objects.create(
				room=m_room,
				sender=request.user,
				content=m_content
			)
			new_message.save()

			message = "hi"

			return JsonResponse({'message': message})
		return JsonResponse({'message': 'Error: Invalid request method'})
	return redirect('sign_in')

def get_messages(request, room_id):
	if request.user.is_authenticated:
		m_room = ChatRoom.objects.get(id=room_id)
		messages = Message.objects.filter(room=m_room)


		serialized_messages = []
		for message_obj in messages:
			serialized_message = {
				'room': message_obj.room_id,
				'sender': message_obj.sender.username if message_obj.sender else None,
				'content': message_obj.content,
				'timestamp': message_obj.timestamp
			}
			serialized_messages.append(serialized_message)

		serialized_messages = json.dumps(serialized_messages, cls=DjangoJSONEncoder)

		return JsonResponse({'messages': serialized_messages})
	return redirect('sign_in')

def send_friend_request(request):
	if request.user.is_authenticated:
		if request.method == 'POST':

			# print(request.POST['receiver_user_id'])


			fr_form = FriendRequestForm(request.POST)
			if fr_form.is_valid():
				receiver_user_id = fr_form.cleaned_data['user_id']
			else:
				receiver_user_id = request.POST['receiver_user_id']

			receiver_user_profile = Profile.objects.get(id=receiver_user_id)
			receiver_user = receiver_user_profile.user

			if request.user == receiver_user:
				messages.info(request, 'You cannot send a friend request to yourself!')
				return redirect('friends')

			if Profile.objects.filter(friend=receiver_user.profile, user=request.user).exists():
				messages.info(request, 'You are already friends with ' + receiver_user.username)
				return redirect('friends')

			if FriendRequest.objects.filter(sender=receiver_user, receiver=request.user).exists():
				messages.info(request, 'You already have a friend request from ' + receiver_user.username)
				return redirect('friends')

			if FriendRequest.objects.filter(sender=request.user, receiver=receiver_user).exists():
				messages.info(request, 'You already sent a friend request to ' + receiver_user.username)
				return redirect('friends')


			friend_request_obj = FriendRequest.objects.create(
					sender=request.user,
					receiver=receiver_user,
				)
			friend_request_obj.save()
			return redirect('friends')

	return redirect('sign_in')

def accept_friend_request(request, fr_id):
	if request.user.is_authenticated:
		friend_request_obj = FriendRequest.objects.get(id=fr_id)
		sender = Profile.objects.get(user=friend_request_obj.sender)
		receiver = Profile.objects.get(user=friend_request_obj.receiver)

		sender.friend.add(receiver)
		friend_request_obj.delete()

		return redirect('friends')
	return redirect('sign_in')

def delete_friend_request(request, fr_id):
	if request.user.is_authenticated:
		friend_request_obj = FriendRequest.objects.get(id=fr_id)
		friend_request_obj.delete()

		return redirect('friends')
	return redirect('sign_in')

def unfriend(request, user_id):
	if request.user.is_authenticated:
		print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n"*10)
		sender = Profile.objects.get(user=request.user)
		receiver = Profile.objects.get(id=user_id)

		sender.friend.remove(receiver)

		return redirect('friends')
	return redirect('sign_in')
	pass