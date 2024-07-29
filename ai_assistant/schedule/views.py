from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import Schedule
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('home')
            except Exception as e:
                form.add_error(None, f"에러발생: {e}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required
def create_schedule(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        schedule = Schedule.objects.create(
            title       =   title,
            description =   description,
            start_time  =   start_time,
            end_time    =   end_time,
            created_by  = request.user
        )
        return redirect('home')
    return render(request, 'create_schedule.html')
