from __future__ import print_function

import datetime
from pathlib import Path
from typing import Union

import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from slack_bot.settings import SCOPES, CALENDAR_ID, STAFF_INFO, BASE_DIR


class GoogleCalendarParser:
    """
    Parses event from Google calendar by now
    """
    __ukraine_tz = pytz.timezone("Etc/GMT-2")
    __creds = None
    __token_path: Path = BASE_DIR.joinpath("token.json")
    __creds_path: Path = BASE_DIR.joinpath("credentials.json")

    def __init__(self):
        self.__login_into_calendar()
        self.__build_service()

    def __build_service(self) -> None:
        try:
            self.__service = build('calendar', 'v3', credentials=self.__creds)
        except HttpError as error:
            print(f'An error occurred: {error}')

    def __login_into_calendar(self) -> None:
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self.__token_path.exists():
            self.__creds = Credentials.from_authorized_user_file(
                str(self.__token_path),
                SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.__creds_path),
                    SCOPES
                )
                self.__creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.__token_path, 'w') as token:
                token.write(self.__creds.to_json())

    def __get_events_from_google_calendar(self) -> Union[dict, None]:
        try:
            now = datetime.datetime.now(self.__ukraine_tz)
            now_iso = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print(f'Getting upcoming event at {now.strftime("%Y-%m-%d %H:%M")}')
            # Call the Calendar API
            event_result = self.__service.events().list(
                calendarId=CALENDAR_ID,
                timeMin=now_iso,
                maxResults=5,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            event_items = event_result.get('items')

            if event_items is None:
                print('No upcoming events found.')
                return
            return event_items
        except HttpError as error:
            print('An error occurred: %s' % error)

    def get_events(self) -> Union[list, None]:
        events_list = list()
        events = self.__get_events_from_google_calendar()
        current_time = self.__get_current_time_str()
        for event in events:
            staff_email = event.get("creator").get("email")
            start_time = self.__normalize_datetime(event.get('start').get('dateTime'))
            if start_time != current_time:
                continue
            if staff_email not in STAFF_INFO:
                print(f"{staff_email} is not staff email")
                continue
            end_time = self.__normalize_datetime(event.get('end').get('dateTime'))
            staff_name = STAFF_INFO.get(staff_email).get("name")
            staff_slack_id = STAFF_INFO.get(staff_email).get("slack_id")
            event_summary = event.get("summary")
            event_item = {
                "name": staff_name,
                "email": staff_email,
                "slack_id": staff_slack_id,
                "start_time": start_time,
                "end_time": end_time,
                "summary": event_summary
            }
            events_list.append(event_item)
        if not events_list:
            print(f"No events at {current_time}")
            return
        return events_list

    def __get_current_time_str(self) -> str:
        time_now = datetime.datetime.now(self.__ukraine_tz)
        return time_now.strftime("%H:%M")

    @staticmethod
    def __normalize_datetime(time: str) -> str:
        time_normalized = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        time_formatted = time_normalized.strftime("%H:%M")
        return time_formatted
