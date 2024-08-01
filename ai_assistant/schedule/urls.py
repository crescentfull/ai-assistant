from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('create_schedule/', views.create_schedule, name='create_schedule'),
    path('schedule_list/', views.schedule_list, name='schedule_list'),
    path('google_calendar_auth/', views.google_calendar_auth, name='google_calendar_auth'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('create_event/', views.create_google_calendar_event, name='create_event'),
]
