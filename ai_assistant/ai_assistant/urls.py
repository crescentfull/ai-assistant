from django.contrib import admin
from django.urls import path, include
from schedule import views as schedule_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('schedule/', include('schedule.urls')),
    path('', schedule_views.home, name='home'),
]
