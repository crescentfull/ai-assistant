from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True, verbose_name="학번")
    is_bt_student = models.BooleanField(default=False, verbose_name="방송통신대학교 학생 여부")
    
    def __str__(self):
        return self.username