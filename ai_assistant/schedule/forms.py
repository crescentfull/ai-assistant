from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Schedule
from allauth.account.forms import LoginForm

class CustomUserCreationForm(UserCreationForm):
    student_id = forms.CharField(max_length=20, required=True, help_text='학번을 입력하세요')
    is_bt_student = forms.BooleanField(required=True, help_text='방통대학생이라면 체크하세요')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'student_id', 'is_bt_student', 'email', 'password1', 'password2')

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['remember'].widget.attrs.update({'class': 'form-check-input'})