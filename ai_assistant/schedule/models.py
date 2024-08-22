from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)  # 사용자의 소개
    location = models.CharField(max_length=30, blank=True, null=True)  # 사용자의 위치
    birth_date = models.DateField(null=True, blank=True)  # 생년월일

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자와 연결
    title = models.CharField(max_length=200)  # 일정 제목
    description = models.TextField(blank=True, null=True)  # 일정 설명
    start_time = models.DateTimeField()  # 시작 시간
    end_time = models.DateTimeField()  # 종료 시간

    def __str__(self):
        return f"{self.title} ({self.user.username})"
