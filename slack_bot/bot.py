from slack import WebClient

from google_services.google_calendar import GoogleCalendarParser
from slack_bot.settings import SLACK_BOT_TOKEN, CHANNEL_ID, STAFF_INFO, ADMIN_EMAIL


class SlackBot:
    """
    @UserName = <@MEMBER_ID>
    @here = <!here>
    """

    def __init__(self):
        self.__client = WebClient(SLACK_BOT_TOKEN)
        self.__calendar = GoogleCalendarParser()

    def check_schedule(self):
        events = self.__calendar.get_events()
        if events is None:
            return
        for event in events:
            self.__send_message(event)

    def __get_message(self, event):
        slack_id = event.get('slack_id')
        start_time = event.get('start_time')
        end_time = event.get('end_time')
        name = event.get('name')
        email = event.get('email')
        summary = event.get('summary')
        mention = self.__get_mention(slack_id)
        if self.__is_qa_tech_check(email):
            summary = self.__try_format_summary(summary)
            print("Sent message about QA/TechCheck")
            return (
                f"<!here>\n"
                f"{summary} will be from {start_time} to {end_time}"
            )
        print("Sent message about mentor")
        return (
            f"{name} is <!here> from {start_time} to {end_time}\n"
            f"Mentor {mention} will answer your questions and check your homeworks"
        )

    def __send_message(self, event):
        message = self.__get_message(event)
        self.__client.chat_postMessage(
            channel=CHANNEL_ID,
            text=message
        )

    @staticmethod
    def __is_qa_tech_check(email: str) -> bool:
        return email == ADMIN_EMAIL

    @staticmethod
    def __try_format_summary(summary: str) -> str:
        staff_members = (staff_member for staff_member in STAFF_INFO.values())
        for staff_member in staff_members:
            name = staff_member.get("name")
            slack_id = staff_member.get("slack_id")
            if name in summary:
                return summary.replace(name, SlackBot.__get_mention(slack_id))
        return summary

    @staticmethod
    def __get_mention(slack_id: str) -> str:
        return f"<@{slack_id}>"
