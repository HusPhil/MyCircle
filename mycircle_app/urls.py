from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('sign_up', views.sign_up, name='sign_up'),
	path('sign_in', views.sign_in, name='sign_in'),
	path('sign_out', views.sign_out, name='sign_out'),

	path('profile/<int:pk>', views.profile, name='profile'),
	path('friends', views.friends, name='friends'),
]