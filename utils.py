from wit import Wit
from firebase import firebase
from pymessenger import Element, Button
import requests
PAGE_ACCESS_TOKEN = open('token.txt','r').readline()
ACCESS_TOKEN = "WD7F5SXIT5E5YJ2J3EAWAPWZT6F57AYA"
MY_DB = "https://website-scrapper-bot.firebaseio.com/"

#create Wit object
class ioeBot:
    def __init__(self,sender_id=0,fname=None):
        self.client = Wit(ACCESS_TOKEN)
        self.firebase = firebase.FirebaseApplication(MY_DB)
        self.sender_id = sender_id
        self.fname = None

    def get_message_response(self,message):
        response = self.client.message(message)
        entity = None
        value = None
        entities = list(response['entities'])
        categories = {'subscribe':None,'greetings':None,'unsubscribe':None,'help':None,'number':None}
        for entity in entities:
            categories[entity] = response['entities'][entity][0]['value']
        return categories


    def get_user_name(self):
        r = requests.get('https://graph.facebook.com/v2.6/'+str(self.sender_id)+'?fields=first_name&access_token='+PAGE_ACCESS_TOKEN)
        if 'first_name' in list(r.json().keys()) :
            self.fname = r.json()['first_name']
            return self.fname
        else:
            return ""

    def get_sender(self):
        result = self.firebase.get('/sender',None)
        return result

    def get_sleep_time(self):
        result = self.firebase.get('/sleep/ssss',None)
        # result=2
        return result

    def set_sleep_time(self,sleep):
        result = self.firebase.put('/sleep','ssss',sleep)
        return result

    def get_prev_notice(self):
        result = self.firebase.get('/notice',None)
        return result

    def save_new_notice(self,notice):
        result = self.firebase.put('/notice','-LF1sU538Jg9JyVQ_Nfs',notice)
        return result

    def save_sender_id(self):
        print("***********SENDERID****************")
        print(self.sender_id)
        result = self.firebase.get('/sender',None)
        print(result)
        db_id = []
        if result != None:
            for x in result.values():
                db_id.append(x['id'])
            if self.sender_id not in db_id:
                payload={'id':self.sender_id,'fname':self.fname}
                result = self.firebase.post('/sender',payload)
                print(result)
                return True
            else:
                return False

        else:
            payload={'id':self.sender_id,'fname':self.fname}
            result = self.firebase.post('/sender',payload)
        return result

    def get_subscribers(self):
        result=self.firebase.get('/sender',None)

        subscribers_list=[]
        for x in result:
            if(result[x]['id']!='' and result[x]['id']!=None):
                subscribers_list.append(result[x]['id'])

        return subscribers_list
            # print(result[x]['fname']=='')

    def send_notice(self,title,subtitle,link,image='default'):
        # for many elements
        # notice_elements=[]
        # if(elements!=None):
        #     for element in elements:
        #         notice_elements.append(element)
        # for single element
        print('**********NOTICE(*********')
        payload={
  "recipient":{
    "id":self.sender_id
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"Welcome!",
            "image_url":""
            "subtitle":"We have the right hat for everyone.",
            "default_action": {
              "type": "web_url",
              "url": "https://petersfancybrownhats.com/view?item=103",
              "webview_height_ratio": "tall",
              "fallback_url": "https://petersfancybrownhats.com/"
            },
            "buttons":[
              {
                "type":"web_url",
                "url":"https://petersfancybrownhats.com",
                "title":"View Website"
              },{
                "type":"postback",
                "title":"Start Chatting",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              }]}]}}}}

        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token='+PAGE_ACCESS_TOKEN,json=payload)
        return r.json()

    def send_quick_replies(self,text,quick_replies):
        payload = {'recipient':{
                'id':self.sender_id,},
                   'message':{
                           'text':text,
                           'quick_replies':[]
                           }}
        for quick_reply in quick_replies:
                payload['message']['quick_replies'].append({
                        'content_type':'text',
                        'title':quick_reply,
                        'payload':'<POSTBACK_PAYLOAD>'
                        })

        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token='+PAGE_ACCESS_TOKEN,json=payload)
        return r.json()
