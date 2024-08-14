from django.urls import path
from . import views
from allauth.socialaccount.providers.google.views import oauth2_login, oauth2_callback

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/google/login', views.CustomOAuth2LoginView.as_view(), name='google_login'),
    path('accounts/google/login/callbacak', views.CustomOAuth2CallbackView, name='google_callback')
]