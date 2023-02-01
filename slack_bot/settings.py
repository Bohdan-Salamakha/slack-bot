import datetime
import json
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

# load environment variables
load_dotenv()
# main settings
BASE_DIR = Path(__file__).parent.parent
# slack settings
SLACK_BOT_TOKEN = getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = getenv("CHANNEL_ID")
TIME_CHECK_INTERVAL = int(getenv("TIME_CHECK_INTERVAL", 60))  # seconds
# Google Calendar settings
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = getenv("CALENDAR_ID")
# General work settings
with open(BASE_DIR.joinpath("staff_info.json")) as staff_info_read_stream:
    STAFF_INFO = json.load(staff_info_read_stream)
ADMIN_EMAIL = getenv("ADMIN_EMAIL")
# Work time settings
WORK_TIME_START = getenv("WORK_TIME_START", "10:00")
# we need to subtract one minute because scheduler skips first run
one_minute = datetime.timedelta(minutes=1)
formatted_start_time = datetime.datetime.strptime(WORK_TIME_START, "%H:%M") - one_minute
WORK_TIME_START = formatted_start_time.strftime("%H:%M")
WORK_TIME_FINISH = getenv("WORK_TIME_FINISH", "22:00")
