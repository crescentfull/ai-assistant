from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomLoginForm, ScheduleForm
from .models import Schedule
from .google_calendar import create_event
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView


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

class CustomLoginView(LoginView):
    form_class = CustomLoginForm

@login_required
def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.created_by = request.user
            schedule.save()
            form.save_m2m()
            # Google Calendar에 이벤트 생성
            event_link = create_event(schedule.title, schedule.description, schedule.start_time, schedule.end_time)
            return redirect('home')
    else:
        form = ScheduleForm()
    return render(request, 'create_schedule.html', {'form': form})

@login_required
def schedule_list(request):
    schedules = Schedule.objects.filter(created_by=request.user)
    return render(request, 'schedule_list.html', {'schedules': schedules})