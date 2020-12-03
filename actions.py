# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
import pathlib
import json

url_red = 'https://profile-predictor.herokuapp.com/event_list'

class ManagerBD():
    def guardarDatos(self,info):
        try:
            python_json=json.loads(info) #Convierte el string a json
        except ValueError:
            pass # invalid json
            return "El JSON enviado es inválido"
        else:
            pass # valid json    
            name_ind=python_json["nombre"]
            i=0
            dictsend={}
            try:
                for item in python_json["Items"]:
                    tupla={}
                    tupla['user_id']=item["user_id"]
                    tupla['factor_id']=int(self.get_factorIndicador(name_ind))
                    tupla['value']=self.getValorType(item["value"],self.isIndCualitative(name_ind))
                    dictsend[int(i)]=tupla    
                    i=i+1
            except KeyError:
                return "El JSON tiene un error de clave"
            else:
                print(requests.put(url_red, json = json.dumps(dictsend)).json())
                return "Recibido"

    def get_factorIndicador(self,name):
        switcher = {
            "TiempoLecturaUserStory": 0,
            "TiempoTrabajoUserStory": 1,
            "ParticipacionesMeetings": 2,
            "Recurso": 3,
            "LineasCodigo": 4,
        }
        return switcher.get(name, -1)

    def isIndCualitative(self,name):
        switcher = {
            "TiempoLecturaUserStory": False,
            "TiempoTrabajoUserStory": True,
            "ParticipacionesMeetings": False,
            "Recurso": True,
            "LineasCodigo": False,
        }
        return switcher.get(name, False)
    
    def getValorType(self,valor,cualitative):
        if cualitative == True:
            return str(valor)
        else:
            return int(valor)

class ActionSendData(Action):

    def name(self) -> Text:
        return "action_sendData"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent_name = tracker.latest_message['intent']['name']
        if intent_name == 'negacion':
            dispatcher.utter_message("Ok")
        else:  
            event_list = tracker.current_state()['events']
            event = [e for e in reversed(event_list) if e['event'] == 'user']
            metadata=event[0]['metadata'] #Obtiene el string enviado en metadata
            manager=ManagerBD()
            info=metadata['name'] #Obtiene el string del campo name de metadata
            message=manager.guardarDatos(info)
            dispatcher.utter_message(text=message)
        return []