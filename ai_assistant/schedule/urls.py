from django.urls import path
from .views import signup, home, create_schedule, profile, schedule_list

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('signup/', signup, name='signup'),
    path('create_schedule/', create_schedule, name='create_schedule'),
    path('schedules/', schedule_list, name='schedule_list'),
]
