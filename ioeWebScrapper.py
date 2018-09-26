import urllib.request as urllib2
from bs4 import BeautifulSoup
import pandas as pd
import sys
import json

main_site = "http://exam.ioe.edu.np"

site = "http://exam.ioe.edu.np/?page="

def get_notices(site,page_no):
    notices_text=[]
    notices_links=[]
    p=1
    while p<=page_no:
        dsite=site+str(p)
        # dsite = main_site
        print('main_site '+dsite)
        try:
            page = urllib2.urlopen(dsite)

            soup = BeautifulSoup(page,"html.parser")
            tables = soup.find_all('table')[0]
            for notice in tables.find_all('tr')[1:]:            
                notice = notice.find_all('td')[1].contents
                notices_links.append(notice[0]['href'])
                notices_text.append(notice[0].contents[0])
            
    ##            df_notices = pd.DataFrame(notices_td,columns=["Notices"])

    ##            for notice in df_notices['Notices']:
    ##                notices_text.append(notice.contents[0])
            p=p+1
            
        except:
            print("Unexpected error:", sys.exc_info()[0])

    return notices_text,notices_links    

def to_json(site,page_no):
    notices_text,notices_links = get_notices(site,page_no)
    py_json = []
    for x , y in list(zip(notices_text,notices_links)):
        dic = {'title':'','file':''}
        dic['title'] = x
        dic['file'] = main_site+y
        py_json.append(dic)    
    json_py = json.dumps(py_json)

    return py_json,json_py

def get_json(site,page_no):
    text ,links = get_notices(site,page_no)
    py_json = to_json(text,links)
##    print(py_json,type(py_json))
    return py_json

# print(to_json(site,1))



# print(get_notices(site,1))




