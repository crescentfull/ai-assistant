from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True, verbose_name="학번")
    is_bt_student = models.BooleanField(default=False, verbose_name="방송통신대학교 학생 여부")
    
    def __str__(self):
        return self.username
    
# 스케줄에 태그 붙이는 기능
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
# 스케줄
class Schedule(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return self.title