from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
import json
from django.core.serializers.json import DjangoJSONEncoder

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
		profile = Profile.objects.get(id=pk)
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

    chat_rooms = []
    for circle in circles:
        circle_chat_rooms = circle.chat_room
        chat_rooms.append(circle_chat_rooms)

    

    context = {
       
        'chatrooms': chat_rooms,
       
    }
    return render(request, 'messages.html', context)



# Create your action functions here

def view_convo(request, room_id):
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

def send_message(request):
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

def get_messages(request, room_id):
	m_room = ChatRoom.objects.get(id=room_id)
	message_contents = Message.objects.filter(room=m_room).values('content')
	message_senders = Message.objects.filter(room=m_room).values('sender')

	print(type(message_senders[0].get('sender')),"::", str(message_senders[0]))

	context = {
		'messages': list(message_contents)
	}

	return JsonResponse(context)

def get_messages(request, room_id):
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

	print(type(serialized_messages))

	serialized_messages = json.dumps(serialized_messages, cls=DjangoJSONEncoder)



	return JsonResponse({'messages': serialized_messages})

    

 # m_room = ChatRoom.objects.get(id=room_id)
 #    messages = Message.objects.filter(room=m_room)

 #    # Serialize messages to JSON
 #    serialized_messages = serialize('json', messages)

 #    return JsonResponse({'messages': serialized_messages})