import logging
import requests
from .google_calendar import create_event

logger = logging.getLogger('schedule')

def get_ku_academic_calendar():
    url = 'https://calendar.google.com/calendar/ical/fnolq3vso0c6i3ci5l8o3b2hjc%40group.calendar.google.com/public/basic.ics'
    try:
        logger.debug(f'Fetching academic calendar from {url}')
        response = requests.get(url)
        # HTML을 파싱하여 학사일정을 추출하는 코드가 필요
        # 일정 예시
        events = [
            {
                'summary': '학기 시작',
                'start': {'dateTime': '2024-03-01T09:00:00', 'timeZone': 'Asia/Seoul'},
                'end': {'dateTime': '2024-03-01T17:00:00', 'timeZone': 'Asia/Seoul'}
            },
            # ...
        ]
        logger.debug(f'Academic calendar fetched: {events}')
        return events
    except Exception as e:
        logger.error(f'Error fetching academic calendar: {e}')
        return []

def add_ku_academic_calendar_to_google():
    events = get_ku_academic_calendar()
    for event in events:
        try:
            logger.debug(f'Adding event to Google Calendar: {event}')
            create_event(event)
            logger.debug('Event added to Google Calendar')
        except Exception as e:
            logger.error(f'Error adding event to Google Calendar: {e}')
