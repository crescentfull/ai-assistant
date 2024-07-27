from django.urls import path
from .views import signup, home, create_schedule

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('create_schedule/', create_schedule, name='create_schedule'),
]
