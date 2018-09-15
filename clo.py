from apscheduler.schedulers.blocking import BlockingScheduler
from utils import ioeBot

ioe_bot = ioeBot()

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=ioe_bot.get_sleep_time())
def timed_job():
    print('This job is run every three minutes.')
