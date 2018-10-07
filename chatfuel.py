MAIN_URL = "https://api.chatfuel.com/bots/5bb8ab8a76ccbc7dfccb5d23/users/{0}/send?chatfuel_token=mELtlMAHYqR0BvgEiMq8zVek3uYUK3OJMbtyrdNPTrQB9ndV0fM7lWTFZbM4MZvD&chatfuel_block_name=Notice&noticeTitle={1}&noticeUrl={2}"
# BOT_ID = '5bb8ab8a76ccbc7dfccb5d23'
# TOKEN = 'mELtlMAHYqR0BvgEiMq8zVek3uYUK3OJMbtyrdNPTrQB9ndV0fM7lWTFZbM4MZvD'

# def send_message(user_id,title,url)
#     MAIN_URL.format(user_id,'asd','23'))

import requests

result = requests.post(MAIN_URL.format(1928179273867668,"new_notice_title","http://www.google.com"))

print(result)
