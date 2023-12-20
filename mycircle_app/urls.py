from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('sign_up', views.sign_up, name='sign_up'),
	path('sign_in', views.sign_in, name='sign_in'),
	path('sign_out', views.sign_out, name='sign_out'),

	path('profile/<uuid:pk>', views.profile, name='profile'),
	path('friends', views.friends, name='friends'),
	path('messages', views.view_messages, name='messages'),
	path('m/<uuid:room_id>', views.view_convo, name='view_convo'),
	path('m/send_message', views.send_message, name='send_message'),
	path('create_circle', views.create_circle, name='create_circle'),
	path('m/get_messages/<uuid:room_id>', views.get_messages, name='get_messages'),
	path('send_friend_request', views.send_friend_request, name='send_friend_request'),
	path('acpt_fr/<int:fr_id>', views.accept_friend_request, name='accept_friend_request'),
	path('del_fr/<int:fr_id>', views.delete_friend_request, name='delete_friend_request'),
	path('un_fr/<uuid:user_id>', views.unfriend, name='unfriend'),

]