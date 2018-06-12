import urllib.request as urllib2
from bs4 import BeautifulSoup
from ioeWebScrapper import to_json
from utils import ioeBot
from pymessenger import Bot
import time

PAGE_TOKEN = open('token.txt','r').readline()

bot = Bot(PAGE_TOKEN)

main_site = "http://exam.ioe.edu.np"

site = "http://exam.ioe.edu.np/?page="

# sleep_time = 20

ioe_bot = ioeBot()    
# def detectChange(sleep_time = 20):
prev_top_notice,_ =  to_json(site,1)
prev_top_notice = prev_top_notice[0]
try:
    while True:
        now_top_notice,_ = to_json(site,1)
        subscribers_list=ioe_bot.get_subscribers()
        print(subscribers_list)
        for x in subscribers_list:
            # ioe_bot = ioeBot(x)
            elements = [{'title':'Notice',
                        'subtitle':now_top_notice[0]['title'],
                        'default_action':{
                            'type': 'web_url',
                            'url': now_top_notice[0]['file'],
                            "messenger_extensions": "false",
                            'webview_height_ratio': 'tall',
                        },
                        'buttons':[{                                                                
                            'type':'web_url',
                            'url':'https://exam.ioe.edu.np',
                            'title':'View website'
                             }],
                        'image_url' : 'https://cdn.pixabay.com/photo/2017/02/10/17/11/table-2055700_960_720.jpg'
                                                             }]
            result = bot.send_generic_message(x,elements)
            print(result)
            # ioe_bot.send_quick_replies('notice',['1','2'])
            # print(ioebot.get_sender())
            # print(x)
            # result = bot.send_text_message(x,'notice')
        if prev_top_notice['title'] != now_top_notice[0]['title']:
            #messenger sends message to all


            print("change")
            pass
        print(prev_top_notice['title'])
        print("equal")
        # time.sleep(sleep_time)
except Exception as e:
    print('Exception:'+str(e))
    
print(prev_top_notice)


