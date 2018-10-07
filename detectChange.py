import urllib.request as urllib2
from bs4 import BeautifulSoup
from ioeWebScrapper import to_json
from utils import ioeBot
from pymessenger import Bot
import time
import requests

PAGE_TOKEN = open('token.txt','r').readline()

bot = Bot(PAGE_TOKEN)

ioe_bot = ioeBot()

main_site = "http://exam.ioe.edu.np"

site = "http://exam.ioe.edu.np/?page="

def send_notice():
    # print('send NOTICEEEEEEEEEE')
    subscribers_list=ioe_bot.get_subscribers()
    now_top_notice,_ = to_json(site,1)
    new_notice_title = now_top_notice[0]['title']
    new_notice_file = now_top_notice[0]['file']
    print('Subscribers:',subscribers_list)
    print('New notice:',new_notice_file)
    print('New title',new_notice_title)

    for x in subscribers_list:
            # ioe_bot = ioeBot(x)
            result = requests.post(MAIN_URL.format(x,new_notice_title,new_notice_file))
            print(result)

def detectChange():

    try:
        prev_top_notice = ioe_bot.get_prev_notice()
        now_top_notice,_ = to_json(site,1)
        subscribers_list=ioe_bot.get_subscribers()
        if prev_top_notice['-LF1sU538Jg9JyVQ_Nfs']['title'] != now_top_notice[0]['title']:
            #messenger sends message to all subscribers
            print("change")
            send_notice()
            ioe_bot.save_new_notice(now_top_notice[0])
            # print(now_top_notice[0])
            pass
        # print(prev_top_notice['title'])
        else:
            print("equal")

    except Exception as e:
        print('Exception:'+str(e))

while(True):
    detectChange()
    time.sleep(int(ioe_bot.get_sleep_time()))
