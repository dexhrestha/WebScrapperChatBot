from wit import Wit
from firebase import firebase
from pymessenger import Element, Button
import requests
PAGE_ACCESS_TOKEN = open('token.txt','r').readline()
ACCESS_TOKEN = "WD7F5SXIT5E5YJ2J3EAWAPWZT6F57AYA"
MY_DB = "https://website-scrapper-bot.firebaseio.com/"

#create Wit object
class ioeBot:
    def __init__(self,sender_id=0):
        self.client = Wit(ACCESS_TOKEN)
        self.firebase = firebase.FirebaseApplication(MY_DB)
        self.sender_id = sender_id
        self.fname = None
        
    def get_message_response(self,message):
        response = self.client.message(message)
        entity = None
        value = None
        entities = list(response['entities'])
        categories = {'subscribe':None,'greetings':None}
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
        # result = self.firebase.get('/sleep',None)
        result=20
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
                payload={'id':self.sender_id,'fname':self.get_user_name()}
                result = self.firebase.post('/sender',payload)
                print(result)
                return True
            else:
                return False
                    
        else:
            payload={'id':self.sender_id,'fname':self.get_user_name()}
            result = self.firebase.post('/sender',payload)
            print(result)
                
    def get_subscribers(self):
        result=self.firebase.get('/sender',None)

        subscribers_list=[]
        for x in result:
            if(result[x]['fname']!='' and result[x]['fname']!=None):                
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
            "image_url":"data:image/jpeg;base64,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",
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