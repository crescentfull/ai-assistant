from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from schedule.views import CustomLoginView

urlpatterns = [
    path('', include('schedule.urls')),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), # REST framework 인증 URL
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')), # Django Allauth URL
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]