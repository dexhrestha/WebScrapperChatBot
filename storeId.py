from firebase import firebase

firebase = firebase.FirebaseApplication('https://website-scrapper-bot.firebaseio.com')

result = firebase.post('/sender',{'id':[{'125465712':'name'}]})
result = firebase.get('/sender',None)
print(result)
