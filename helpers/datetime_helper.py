import datetime

import pytz


class DateTimeHelper:
    __ukraine_tz = pytz.timezone("Etc/GMT-2")

    @staticmethod
    def get_current_time_str_hour_minute() -> str:
        now = datetime.datetime.now(DateTimeHelper.__ukraine_tz)
        return now.strftime("%H:%M")

    @staticmethod
    def get_current_time_usual_look():
        now = datetime.datetime.now(DateTimeHelper.__ukraine_tz)
        return now.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def normalize_datetime(time: str) -> str:
        time_normalized = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        time_formatted = time_normalized.strftime("%H:%M")
        return time_formatted
