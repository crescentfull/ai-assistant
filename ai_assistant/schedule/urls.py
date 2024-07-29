from django.urls import path
from .views import signup, home, create_schedule, profile

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('signup/', signup, name='signup'),
    path('create_schedule/', create_schedule, name='create_schedule'),
]
