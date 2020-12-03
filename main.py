import requests
import json
url = 'http://localhost:5005/webhooks/my_connector/webhook/' ##change rasablog with your app name
myobj = {
"message": "hi",
"sender": "asdasd",
"metadata":{
            "name": '6'
        }
}
x = requests.post(url, json = myobj)
print(x.text)

