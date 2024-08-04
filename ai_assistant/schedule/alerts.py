import logging
import smtplib
from email.mime.text import MIMEText
import openai
from .google_calendar import get_events

logger = logging.getLogger('schedule')

def send_email_alert(subject, body, to_email):
    from_email = 'your-email@example.com'
    from_password = 'your-email-password'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        logger.debug(f'Sending email to {to_email} with subject {subject}')
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        logger.debug('Email sent successfully')
    except Exception as e:
        logger.error(f'Error sending email: {e}')

def get_gpt_response(prompt):
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    try:
        logger.debug(f'Fetching GPT-3 response for prompt: {prompt}')
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=150
        )
        gpt_response = response.choices[0].text.strip()
        logger.debug(f'GPT-3 response: {gpt_response}')
        return gpt_response
    except Exception as e:
        logger.error(f'Error fetching GPT-3 response: {e}')
        return "Sorry, I couldn't fetch a response from GPT-3."

def send_schedule_alerts():
    events = get_events()
    for event in events:
        # 현재 시간을 기준으로 일정이 다가왔는지 확인하는 코드 필요
        # 일정 예시
        try:
            logger.debug(f'Sending alert for event: {event["summary"]}')
            send_email_alert('Upcoming Event: ' + event['summary'], 'Event details: ' + event['description'], 'recipient@example.com')
            prompt = f"How should I prepare for the event: {event['summary']}?"
            response = get_gpt_response(prompt)
            send_email_alert('Preparation Tips for ' + event['summary'], response, 'recipient@example.com')
            logger.debug('Alert and preparation tips sent successfully')
        except Exception as e:
            logger.error(f'Error sending alert for event {event["summary"]}: {e}')
