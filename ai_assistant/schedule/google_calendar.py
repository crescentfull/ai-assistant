import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

logger = logging.getLogger(__name__)

def create_event(summary, location, description, start_time, end_time):
    """
    구글 캘린더에 새로운 이벤트를 생성합니다.
    """
    try:
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Seoul',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Seoul',
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        logger.debug(f"Event created: {event}")
        return event
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        raise

def list_events():
    """
    구글 캘린더에서 다가오는 이벤트를 리스트합니다.
    """
    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        logger.debug(f"Events listed: {events}")
        return events
    except Exception as e:
        logger.error(f"Error listing events: {e}")
        raise
