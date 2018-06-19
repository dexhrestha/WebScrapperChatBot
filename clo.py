from apscheduler.schedulers.blocking import BlockingScheduler

sleep_time = 1
sched = BlockingScheduler()

@sched.scheduled_job('interval',minutes=int(open('time.txt','r').read()))
def time_job():
	
	# bot.send_text_message('1928179273867668','Sleep time:'+str(sleep_time))
	print('Run every'+str(minutes)+'minutes')
	# detectChange()
	sleep_time = 3

sched.start()


