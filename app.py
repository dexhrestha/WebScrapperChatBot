import os,sys,requests
from utils import ioeBot
# from detectChange import detectChange
from flask import Flask,request
from pymessenger import Bot
import datetime
PAGE_TOKEN = open('token.txt','r').readline()

ADMIN_SENDER_ID = "1928179273867668"
SLEEP_TIME = 60

app = Flask(__name__)

bot = Bot(PAGE_TOKEN)

state={'subscribe':False}


# START=datetime.datetime.now
# print(START)

# if(START-datetime.datetime.now==20):
#     detectChange()

@app.route('/',methods=['GET'])
def verify_webhook():
    #Webhook Verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "ioeBot":
            return "Verification token Mismatch" , 403
        return request.args["hub.challenge"],200
        print("Verfiy")
    return "Hello world",200

@app.route('/show',methods=['GET'])
def show():
    return 'Show me',200

@app.route('/',methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    messaging_text = ""
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                ioe_bot = ioeBot(sender_id)
                if messaging_event.get('message'):
                    #if message is a text save text
                    if 'text' in messaging_event['message']:

                        messaging_text=messaging_event['message']['text']
                        # if(sender_id=ADMIN_SENDER_ID and )
                        # result = bot.send_text_message(sender_id,messaging_text)                       
                    else:
                        messaging_text='Not a text'
                    
                    categories = ioe_bot.get_message_response(messaging_text)
                    print("categories:")
                    print(categories)
                    if categories['numbers'] !=None and sender_id == '1928179273867668' :
                        try:
                            if int(messaging_text) > 0:
                               ioe_bot.set_sleep_time(int(messaging_text))
                        except Exception as e:
                            print(e)
                        
                    elif categories['subscribe'] != None:
                        res = ioe_bot.save_sender_id()
                        if res:
                            
                            result = bot.send_text_message(sender_id,'Thank you for your subscription,'+ioe_bot.get_user_name()+'!')
                        else:
                            result = bot.send_text_message(sender_id,ioe_bot.get_user_name()+', you have already subscribed!! Thank you!!')
                    elif categories['unsubscribe'] !=None:
                        state['unsubscribe']=True
                        res=ioe_bot.save_sender_id()
                        if not res:
                            result = bot.send_text_message(sender_id,'Thank you. Do send us feedback.')
                            # remove from database ioe_bot.remove_sender_id()
                        else:
                            result = bot.send_text_message(sender_id,'You have not subscribed!!Would you like to Subscribe?')
                            state['subscribe']=True
                    elif categories['help'] != None:
                        result = bot.send_text_message(sender_id,'Hello I am IOEbot . I will send you latest notice from IOE. Would you like to Subscribe?')
                        state['subscribe']=True
                             
                    else:
                        bot.send_text_message(sender_id,'Sorry i did not get that . Type help for Help')

                    if state['subscribe']:
                        if categories['Yes'] != None:
                            categories['subscribe']=True
                        elif categories['No'] !=None:
                            bot.send_text_message(sender_id,'Type Subscribe to subscribe any time.')

                    
                if messaging_event.get('postback'):
                    if (messaging_event['postback']['payload']=='firsthandshake'):
                        get_started_text='Hello Hello I am IOEbot . I will send you latest notice from IOE. Would you like to Subscribe?'
                        state['subscribe']=True
                        result = bot.send_text_message(sender_id,get_started_text) 

    return "ok",200

def log(message):
    print(message)
    sys.stdout.flush()


if __name__== "__main__":
    app.run(debug = True , port=5000)
