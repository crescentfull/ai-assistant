import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/calendar']

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def get_credentials_from_session(session):
    if 'credentials' in session:
        return Credentials(**session['credentials'])
    return None

def save_credentials_to_session(session, credentials):
    session['credentials'] = credentials_to_dict(credentials)

def initiate_google_calendar_auth(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return authorization_url

def handle_google_calendar_callback(request):
    state = request.session.get('state')
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    save_credentials_to_session(request.session, credentials)

def create_google_calendar_event(request, title, description, start_time, end_time):
    credentials = get_credentials_from_session(request.session)
    if not credentials:
        return None, "Credentials not found"

    try:
        service = build('calendar', 'v3', credentials=credentials)

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Asia/Seoul',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Asia/Seoul',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return event.get('htmlLink'), None

    except Exception as e:
        return None, str(e)
