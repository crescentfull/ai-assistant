from django.contrib import admin
from .models import Event, LearningStatus, AcademicSchedule

admin.site.register(Event)
admin.site.register(LearningStatus)
admin.site.register(AcademicSchedule)