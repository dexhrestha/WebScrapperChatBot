
import urllib.request as urllib2
from bs4 import BeautifulSoup
from ioeWebScrapper import to_json
from utils import ioeBot
from pymessenger import Bot
import time
import requests

PAGE_TOKEN = open('token.txt','r').readline()
MAIN_URL = "https://api.chatfuel.com/bots/5bbd658876ccbc2d050ff23a/users/{0}/send?chatfuel_token=3TYBQLSKuIbKbLEDKroYmTbpCoCtO0XIM04RAx4R0VOpekvwfNgAKdlXu0DxXwH4&chatfuel_block_name=Notice"
#"&noticeTitle={1}&noticeUrl={2}"
bot = Bot(PAGE_TOKEN)

ioe_bot = ioeBot()

main_site = "http://exam.ioe.edu.np"

site = "http://exam.ioe.edu.np/?page="

def send_notice(now_top_notice):
    # print('send NOTICEEEEEEEEEE')
    subscribers_list=ioe_bot.get_subscribers()
    new_notice_title = now_top_notice['title']
    new_notice_file = now_top_notice['file']
    print('New notice:',new_notice_file)
    print('New title',new_notice_title)
    ## broadcast to subsribers
    for x in subscribers_list:
        # ioe_bot = ioeBot(x)
        content={
            "noticeTitle":new_notice_title,
            "noticeUrl":new_notice_file
        }
        #result = requests.post(MAIN_URL.format(x),json=content)
        print(content)
        break

def detectChange():

    try:
        now_top_notice,_ = to_json(site,1)
        subscribers_list=ioe_bot.get_subscribers()
        prev_title = ioe_bot.get_prev_notice()['-LF1sU538Jg9JyVQ_Nfs']['title']
        no_of_new_notices = find_prev_notice_pos(prev_title,now_top_notice)
        for x in range(no_of_new_notices):
        	send_notice(now_top_notice[x]) 
        if prev_title != now_top_notice[0]['title']:
            #messenger sends message to all subscribers
            print("change")
            no_of_new_notices = find_prev_notice_pos(prev_title,now_top_notice)
            for x in range(no_of_new_notices):
            	send_notice(now_top_notice[x])
            ioe_bot.save_new_notice(now_top_notice[0])
            # print(now_top_notice[0])
            pass
        # print(prev_top_notice['title'])
        else:
            print("equal")

    except Exception as e:
        print('Exception:'+str(e))
def find_prev_notice_pos(prev_title,now_notice):
	for i,x in enumerate(now_notice):
		if x['title'] == prev_title:
			return i	
	
while(True):
    detectChange()
    time.sleep(int(ioe_bot.get_sleep_time()))
