import threading
from time import sleep

from schedule import run_pending, every, ScheduleValueError

from slack_bot.bot import SlackBot
from slack_bot.settings import WORK_TIME_START, WORK_TIME_FINISH, TIME_CHECK_INTERVAL


class Scheduler:
    @staticmethod
    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()

    @staticmethod
    def run():
        bot = SlackBot()
        while True:
            try:
                start_work = (every().minute.until(WORK_TIME_FINISH).
                              do(Scheduler.run_threaded, bot.check_schedule))
            except ScheduleValueError:
                print(f'Can not set WORK_TIME_FINISH={WORK_TIME_FINISH}. '
                      f'Wait for tomorrow please.')
                sleep(TIME_CHECK_INTERVAL * 60)
            else:
                break
        every().day.at(WORK_TIME_START).do(Scheduler.run_threaded, start_work)
        while True:
            run_pending()
            sleep(TIME_CHECK_INTERVAL)
