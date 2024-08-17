from django.contrib import admin
from django.urls import path, include
from schedule import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Django Allauth URL 설정
    path('', views.home, name='home'),  # 홈 페이지 URL 설정
]
