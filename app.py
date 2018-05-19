import os,sys,requests
from flask import Flask,request
from pymessenger import Bot
from utils import ioeBot
PAGE_TOKEN = open('token.txt','r').readline()

app = Flask(__name__)

bot = Bot(PAGE_TOKEN)

@app.route('/',methods=['GET'])
def verify_webhook():
    #Webhook Verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "ioeBot":
            return "Verification token Mismatch" , 403
        return request.args["hub.challenge"],200
        print("Verfiy")
    return "Hello world",200


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
                       
                        result = bot.send_text_message(sender_id,messaging_text)
                       
                    else:
                        messaging_text='Not a text'
                    
                    categories = ioe_bot.get_message_response(messaging_text)
                    print(categories)
                    if categories['subscribe'] != None:
                       
                        
                       
                        try:
                            res = ioe_bot.save_sender_id()
                            if res:
                                result = bot.send_text_message(sender_id,'Thank you for your subscription,'+ioe_bot.get_user_name()+'!')
                            else:
                                result = bot.send_text_message(sender_id,ioe_bot.get_user_name+', you have already subscribed!! Thank you!!')
                            print(res)
                        except :
                            print("***********Cannot************")
                #if message is a postback                        
    return "ok",200

def log(message):
    print(message)
    sys.stdout.flush()


if __name__== "__main__":
    app.run(debug = True , port=5000)
