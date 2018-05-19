from wit import Wit
from firebase import firebase
from pymessenger import Element, Button
import requests
PAGE_ACCESS_TOKEN = "EAAZA6jaB1OAsBADOYKq10zzfMdGnZAMmxUkQQWtKzM7JTQ6CoEVlEJWdf5wIQSwFQAKMDhttfyyCiuq3lUZCn1jPn6PmoXxUtr9S2oqe3xp8OhKZB6577XAiwwRIeW3oD0stW8tZATADlBnCTklhso2hZCpzhZAb34EBdMGZBH3rQgZDZD"
ACCESS_TOKEN = "RGNBICRVSLZEPAWMT2FQRZVAFZ42PX6Y"
MY_DB = "https://website-scrapper-bot.firebaseio.com/"

#create Wit object
class ioeBot:
    def __init__(self,sender_id):
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
        
    def save_sender_id(self):
        result = self.firebase.get('/sender',None)
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
                
##
##
##ioe_bot = ioeBot(1928179273867668)
##res = ioe_bot.save_sender_id()
##print(res)

