import logging
from django.db import models
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class Event(models.Model):
    """
    구글 캘린더 이벤트를 나타내는 모델.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=255, unique=True)
    summary = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        logger.debug(f"Event {self.summary} saved/updated for user {self.user}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.summary

class LearningStatus(models.Model):
    """
    학습현황 정보를 나타내는 모델.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    progress = models.CharField(max_length=100)
    last_accessed = models.DateTimeField()

    def __str__(self):
        return self.course_name

class AcademicSchedule(models.Model):
    """
    방송통신대학교 학사일정을 나타내는 모델.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
