**staff_info.json**

`{
  "<STAFF_1_EMAIL>": 
  {
    "name": "<STAFF_1_NAME>",
    "slack_id": "<STAFF_1_SLACK_ID>"
  },
  "<STAFF_2_EMAIL>": 
  {
    "name": "<STAFF_2_NAME>",
    "slack_id": "<STAFF_2_SLACK_ID>"
  },
  ...
}`

STAFF_EMAIL = `<STRING>` ("test1@gmail.com")

STAFF_NAME = `<STRING>` ("John")

STAFF_SLACK_ID = `<STRING>` ("F04K187DFCJ")

**ENVIRONMENT VARIABLES**

SLACK_BOT_TOKEN - token of your Slack app

CHANNEL_ID - id of Slack channel where u want bot to drop msgs

CALENDAR_ID - id of Google Calendar that u want to use

TIME_CHECK_INTERVAL - how often (seconds) bot will check schedule (DEFAULT=60)

WORK_TIME_START - bot starts working at this time (DEFAULT="10:00")

WORK_TIME_FINISH - bot finishes work at this time (DEFAULT="22:00")
