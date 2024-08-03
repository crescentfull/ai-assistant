
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings

# 설정 로그
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        # OAuth 2.0 Flow 객체 생성
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        logger.debug("Flow object created successfully")

        # authorization_url과 state 값을 생성
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        logger.debug(f"Authorization URL: {authorization_url}")
        logger.debug(f"State: {state}")

        return authorization_url, state
    except Exception as e:
        logger.error(f"Error generating authorization URL: {e}")
        raise

def handle_google_calendar_callback(request):
    try:
        state = request.session.get('state')
        logger.debug(f"State from session: {state}")
        if not state:
            logger.error("State not found in session")
            raise ValueError("State not found in session")

        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/calendar'],
            state=state,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        authorization_response = request.build_absolute_uri()
        logger.debug(f"Authorization response: {authorization_response}")

        flow.fetch_token(authorization_response=authorization_response)
        logger.debug("Token fetched successfully")

        credentials = flow.credentials
        logger.debug(f"Credentials: {credentials}")

        save_credentials_to_session(request.session, credentials)
        logger.debug("Credentials saved to session")
    except Exception as e:
        logger.error(f"Error in handle_google_calendar_callback: {e}")
        raise

def save_credentials_to_session(session, credentials):
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    logger.debug("Session credentials updated")

def create_google_calendar_event(request, title, description, start_time, end_time):
    credentials = get_credentials_from_session(request.session)
    if not credentials:
        logger.error('Credentials not found in session')
        return None, "Credentials not found"

    try:
        service = build('calendar', 'v3', credentials=credentials)
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            }
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        logger.info('Event created: %s', event.get('htmlLink'))
        return event.get('htmlLink'), None
    except Exception as e:
        logger.error('An error occurred: %s', e)
        return None, str(e)
