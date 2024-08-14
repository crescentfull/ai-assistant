from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', chat, name='chat'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/google/login', CustomOAuth2LoginView.as_view(), name='google_login'),
    path('accounts/google/login/callback/', CustomOAuth2CallbackView.as_view(), name='google_callback'),
]