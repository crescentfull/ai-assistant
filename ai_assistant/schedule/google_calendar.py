import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar API의 범위 설정
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """
    Google Calendar 서비스 객체 생성
    사용자 인증 처리, 토큰을 갱신
    """
    creds = None
    # token.json 파일은 사용자의 액세스 및 리프레시 토큰을 저장합니다.
    # 인증 흐름이 처음 완료될 때 자동으로 생성됩니다.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # 유효한 자격 증명이 없는 경우 사용자를 로그인시킵니다.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 토큰이 만료되었지만 리프레시 토큰이 있는 경우 토큰을 갱신합니다.
            creds.refresh(Request())
        else:
            # 리프레시 토큰이 없거나 유효하지 않은 경우 사용자 로그인을 시작합니다.
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # 다음 실행을 위해 자격 증명을 저장합니다.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # Google Calendar API 서비스 객체를 빌드합니다.
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(summary, description, start_time, end_time):
    """
    Google Calendar에 새로운 이벤트를 생성합니다.

    Args:
        summary (str): 이벤트 제목
        description (str): 이벤트 설명
        start_time (datetime): 이벤트 시작 시간 (datetime 객체)
        end_time (datetime): 이벤트 종료 시간 (datetime 객체)

    Returns:
        str: 생성된 이벤트의 링크 (URL)
    """
    # Google Calendar 서비스 객체를 가져옵니다.
    service = get_calendar_service()
    
    # 이벤트 데이터를 정의합니다.
    event = {
        'summary': summary,  # 이벤트 제목
        'description': description,  # 이벤트 설명
        'start': {
            'dateTime': start_time.isoformat(),  # 이벤트 시작 시간 (ISO 형식)
            'timeZone': 'UTC',  # 시간대 설정
        },
        'end': {
            'dateTime': end_time.isoformat(),  # 이벤트 종료 시간 (ISO 형식)
            'timeZone': 'UTC',  # 시간대 설정
        },
        'reminders': {
            'useDefault': False,  # 기본 리마인더 설정을 사용하지 않음
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # 이메일 리마인더 (24시간 전)
                {'method': 'popup', 'minutes': 10},  # 팝업 리마인더 (10분 전)
            ],
        },
    }
    
    # 이벤트를 Google Calendar에 삽입합니다.
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")  # 생성된 이벤트 링크를 출력합니다.
    return event.get('htmlLink')  # 생성된 이벤트의 링크를 반환합니다.