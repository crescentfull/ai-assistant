from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), # REST framework 인증 URL
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')), # Django Allauth URL
    path('signup/', include('schedule.urls')), # 회원 가입 URL 포함
]