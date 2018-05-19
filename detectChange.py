import urllib.request as urllib2
from bs4 import BeautifulSoup
from ioeWebScrapper import to_json
import time

main_site = "http://exam.ioe.edu.np"

site = "http://exam.ioe.edu.np/?page="

sleep_time = 20

prev_top_notice,_ =  to_json(site,1)
prev_top_notice = prev_top_notice[0]
try:
    while True:
        now_top_notice,_ = to_json(site,1)
        if prev_top_notice['title'] != now_top_notice[0]['title']:
            #messenger sends message to all
            
            print("change")
            pass
        print(prev_top_notice['title'])
        print("equal")
        time.sleep(sleep_time)
except Exception as e:
    print(e)
    
print(prev_top_notice)
