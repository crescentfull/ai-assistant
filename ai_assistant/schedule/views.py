from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomLoginForm, ScheduleForm
from .models import Schedule
from .google_calendar import initiate_google_calendar_auth, handle_google_calendar_callback, create_google_calendar_event
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView

class CustomLoginView(LoginView):
    form_class = CustomLoginForm

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
def google_calendar_auth(request):
    authorization_url = initiate_google_calendar_auth(request)
    return redirect(authorization_url)

@login_required
def oauth2callback(request):
    handle_google_calendar_callback(request)
    return redirect('create_schedule')

@login_required
def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.created_by = request.user
            schedule.save()

            # 시간 형식 변환 (예: UTC 형식으로 변환)
            start_time = schedule.start_time.isoformat() + 'Z'
            end_time = schedule.end_time.isoformat() + 'Z'

            # 이벤트 생성
            if 'credentials' not in request.session:
                return redirect('google_calendar_auth')

            try:
                event_link, error = create_google_calendar_event(request, schedule.title, schedule.description, start_time, end_time)
                if error:
                    print(f"An error occurred: {error}")
                else:
                    schedule.event_link = event_link
                    schedule.save()
            except Exception as e:
                print(f"An error occurred: {e}")
            return redirect('schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'list/create_schedule.html', {'form': form})

@login_required
def schedule_list(request):
    schedules = Schedule.objects.filter(created_by=request.user)
    return render(request, 'list/schedule_list.html', {'schedules': schedules})
