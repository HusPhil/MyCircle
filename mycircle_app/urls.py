from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('sign_up', views.sign_up, name='sign_up'),
	path('sign_in', views.sign_in, name='sign_in'),
	path('sign_out', views.sign_out, name='sign_out'),

	path('profile/<int:pk>', views.profile, name='profile'),
	path('friends', views.friends, name='friends'),
	path('messages', views.messages, name='messages'),
	path('view_convo/<uuid:room_id>', views.view_convo, name='view_convo'),
	path('create_circle', views.create_circle, name='create_circle'),
]