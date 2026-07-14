from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from datetime import datetime, timedelta
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service

def create_event(service, event_data):
    start = datetime.fromisoformat(f"{event_data['date']}T{event_data['time']}:00")
    end = start + timedelta(hours=1)

    event = {
        "summary": event_data["title"],
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "Asia/Kolkata"
        }
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event
