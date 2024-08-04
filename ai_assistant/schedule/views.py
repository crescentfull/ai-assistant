from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomLoginForm, ScheduleForm, ProfileForm
from .models import Schedule
from .google_calendar import *
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView
import logging

# 로그 설정
logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    form_class = CustomLoginForm

def home(request):
    logger.debug("Home view accessed")
    return render(request, 'home.html')

@login_required
def profile(request):
    logger.debug("Profile view accessed")
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            logger.debug(f"Profile updated for user: {request.user.username}")
            return redirect('profile')
        else:
            logger.debug("Profile form is not valid")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'account/profile.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                logger.debug(f"User signed up: {user.username}")
                return redirect('home')
            except Exception as e:
                logger.error(f"Error during signup: {e}")
                form.add_error(None, f"에러발생: {e}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required
def google_calendar_auth(request):
    try:
        authorization_url, state = initiate_google_calendar_auth(request)
        request.session['oauth_state'] = state
        logger.debug(f"Google Calendar auth initiated: {authorization_url}, state saved: {state}")
        return redirect(authorization_url)
    except ValueError as e:
        logger.error(f"Error initiating Google Calendar auth: {e}")
        return render(request, 'error.html', {'message': f'Error initiating Google Calendar auth: {e}'})
    except Exception as e:
        logger.error(f"Unexpected error initiating Google Calendar auth: {e}")
        return render(request, 'error.html', {'message': 'Unexpected error initiating Google Calendar auth'})

@login_required
def oauth2callback(request):
    try:
        logger.debug("OAuth2 callback accessed")
        handle_google_calendar_callback(request)
        logger.debug("Google Calendar OAuth2 callback handled successfully")
        return render(request, 'list/oauth2callback_success.html', {'message': 'Google Calendar authentication successful!'})
    except Exception as e:
        logger.error(f"Error handling OAuth2 callback: {e}")
        return render(request, 'error.html', {'message': 'Error handling OAuth2 callback'})

@login_required
def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.created_by = request.user
            schedule.save()

            start_time = schedule.start_time.isoformat() + 'Z'
            end_time = schedule.end_time.isoformat() + 'Z'

            if 'credentials' not in request.session:
                return redirect('google_calendar_auth')

            try:
                event_link, error = create_google_calendar_event(request, schedule.title, schedule.description, start_time, end_time)
                if error:
                    logger.error(f"Error creating Google Calendar event: {error}")
                else:
                    schedule.event_link = event_link
                    schedule.save()
            except Exception as e:
                logger.error(f"Exception while creating Google Calendar event: {e}")
            return redirect('schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'list/create_schedule.html', {'form': form})

def update_schedule(request, event_id):
    if request.method == 'POST':
        updated_event = {
            'summary': request.POST['summary'],
            'location': request.POST['location'],
            'description': request.POST['description'],
            'start': {
                'dateTime': request.POST['start'],
                'timeZone': 'Asia/Seoul',
            },
            'end': {
                'dateTime': request.POST['end'],
                'timeZone': 'Asia/Seoul',
            },
        }
        logger.debug(f'Updating event {event_id} with data: {updated_event}')
        try:
            update_event(event_id, updated_event)
            logger.debug('Event updated successfully')
        except Exception as e:
            logger.error(f'Error updating event {event_id}: {e}')
        return redirect('schedule_list')
    return render(request, 'list/update_schedule.html')


def delete_schedule(request, event_id):
    logger.debug(f'Deleting event {event_id}')
    try:
        delete_event(event_id)
        logger.debug('Event deleted successfully')
    except Exception as e:
        logger.error(f'Error deleting event {event_id}: {e}')
    return redirect('schedule_list')

@login_required
def schedule_list(request):
    schedules = Schedule.objects.filter(created_by=request.user)
    logger.debug(f"Schedule list accessed by user: {request.user.username}")
    return render(request, 'list/schedule_list.html', {'schedules': schedules})