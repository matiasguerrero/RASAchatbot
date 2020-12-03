import json
import requests

url = 'https://botdisenio.herokuapp.com/webhooks/my_connector/webhook/' ##change rasablog with your app name
#https://botdisenio.herokuapp.com/webhooks/my_connector/webhook/
#http://localhost:5005/webhooks/my_connector/webhook/

def response(mensaje,datos):
    myobj = {
    "message": str(mensaje),
    "sender": "matias",
    "metadata":{
                "name": str(datos)
            }
    }
    request_response = requests.post(url, json = myobj)
    return request_response

while True:
    mensaje= input('¿Mensaje?: ')
    if mensaje == "/stop":
        break
    datos= input('¿Datos?: ')
    chat_recibidos=response(mensaje,datos).json()
    print(chat_recibidos)
    for chat in chat_recibidos:
        if 'text' in chat: #verifica si existe el campo text, ya que podemos recibir una imagen
            textReceive=chat['text']
            print(textReceive)
        if 'image' in chat: #verifica si existe el campo text, ya que podemos recibir una imagen
            imageReceive=chat['image']
            print(imageReceive)