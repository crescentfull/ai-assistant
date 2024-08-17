# ai_assistant/schedule/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 홈 페이지 URL 설정
]
