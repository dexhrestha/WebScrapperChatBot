import urllib.request as urllib2
from bs4 import BeautifulSoup
from ioeWebScrapper import to_json
from utils import ioeBot
from pymessenger import Bot
import time
import redis
from apscheduler.schedulers.blocking import BlockingScheduler

PAGE_TOKEN = open('token.txt','r').readline()

bot = Bot(PAGE_TOKEN)

ioe_bot = ioeBot()    

main_site = "http://exam.ioe.edu.np"

site = "http://exam.ioe.edu.np/?page="

sched = BlockingScheduler()

sleep_time = ioe_bot.get_sleep_time()
new_notice_title = ""
new_notice_file = ""
subscribers_list = []

def send_notice():
    print('send NOTICEEEEEEEEEE')
    for x in subscribers_list:
            # ioe_bot = ioeBot(x)
            elements = [{'title':'Notice',
                        'subtitle':new_notice_title,
                        'default_action':{
                            'type': 'web_url',
                            'url': new_notice_file,
                            "messenger_extensions": "false",
                            'webview_height_ratio': 'tall',
                        },
                        'buttons':[{                                                                
                            'type':'web_url',
                            'url':'https://exam.ioe.edu.np',
                            'title':'View website'
                             }],
                        'image_url' : 'https://cdn.pixabay.com/photo/2017/02/10/17/11/table-2055700_960_720.jpg'}]

            result = bot.send_generic_message(x,elements)
            print(result)

def detectChange():
    try:
        
        prev_top_notice = ioe_bot.get_prev_notice()
        print(prev_top_notice['-LF1sU538Jg9JyVQ_Nfs']['title'])
        now_top_notice,_ = to_json(site,1)
        print(now_top_notice[0]['title'])
        new_notice_title = now_top_notice[0]['title']
        new_notice_file = now_top_notice[0]['file']
        subscribers_list=ioe_bot.get_subscribers()
        print(subscribers_list)
            # ioe_bot.send_quick_replies('notice',['1','2'])
            # print(ioebot.get_sender())
            # print(x)
            # result = bot.send_text_message(x,'notice')
        if prev_top_notice['-LF1sU538Jg9JyVQ_Nfs']['title'] != now_top_notice[0]['title']:
            #messenger sends message to all
            print("change")
            send_notice()
            ioe_bot.save_new_notice(now_top_notice[0])
            # print(now_top_notice[0])
            pass
        # print(prev_top_notice['title'])
        else:
            print("equal")
       
        # time.sleep(20)
    except Exception as e:
        print('Exception:'+str(e))

@sched.scheduled_job('interval',minutes=sleep_time)
def time_job():
    print('Run every'+str(sleep_time)+'minutes')
    detectChange()

sched.start()