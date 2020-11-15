# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#cusrtom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
import requests
import json

url_red = 'https://profile-predictor.herokuapp.com/bayesian_network'

carac_index = {
    'perception':0,
    'processing':1,
    'input':2,
    'understanding':3,
}


class ActionCreateVector(Action):

    def name(self) -> Text:
        return "action_create_vector"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        valorText = tracker.latest_message["text"]
        print(valorText)    
        intent_name = tracker.latest_message['intent']['name']
        print(intent_name)
        caracteristicas=tracker.get_slot("caracteristicas")

        bot_event = next(e for e in reversed(tracker.events) if e["event"] == "bot")
        pregunta=bot_event.get("text")
        items=pregunta.split(".",1)
        index_preg=0

        # List of Perception
        listOfPerception = ['2' , '6']
        # List of Processing
        listOfProcessing = ['1' , '5', '9']
        # List of Input
        listOfInput = ['3' , '7']
        # List of Understanding
        listOfUnderstanding = ['4' , '8']

        if items[0] in listOfPerception :
            index_preg=carac_index['perception']
        elif items[0] in listOfProcessing :
            index_preg=carac_index['processing']
        elif items[0] in listOfInput :
            index_preg=carac_index['input']
        elif items[0] in listOfUnderstanding :
            index_preg=carac_index['understanding']


        entities=tracker.latest_message['entities']
        for e in entities:
            if e['entity']=='respuesta':
                name=e['value']
                if name == "A":
                    caracteristicas[index_preg]+= 1
                elif name == "B":
                    caracteristicas[index_preg]+= -1
        #dispatcher.utter_message(text="Vector: " + str(caracteristicas))

        return [SlotSet("caracteristicas", caracteristicas)]

class ActionFelder(Action):

     def name(self) -> Text:
        return "action_felder"
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        caracteristicas=tracker.get_slot("caracteristicas")

        if caracteristicas[carac_index['perception']] > 0:
            message="Sensitivo: "+str(caracteristicas[carac_index['perception']])
        else:
            message="Intuitivo: "+str((-1*caracteristicas[carac_index['perception']]))

        if caracteristicas[carac_index['processing']] > 0:
            message=message+" Activo: "+str(caracteristicas[carac_index['processing']])
        else:
            message=message+" Reflexivo: "+str((-1*caracteristicas[carac_index['processing']]))    

        if caracteristicas[carac_index['input']] > 0:
            message=message+" Visual: "+str(caracteristicas[carac_index['input']])
        else:
            message=message+" Verbal: "+str((-1*caracteristicas[carac_index['input']]))  

        if caracteristicas[carac_index['understanding']] > 0:
            message=message+" Secuencial: "+str(caracteristicas[carac_index['understanding']])
        else:
            message=message+" Global: "+str((-1*caracteristicas[carac_index['understanding']]))        
        dispatcher.utter_message(text=message)

        return []

class ActionInteracciones(Action):
    def name(self) -> Text:
        return "action_interacciones"

    def get_interacciones(self,intent_name,cantidad):
        message=''
        if intent_name == 'cant_interacciones':
            message="Interacciones: "+cantidad
        elif intent_name == 'max_interacciones':
            message="Max de interacciones: "+cantidad
        return message

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        texto = tracker.latest_message["text"]
        intent_name = tracker.latest_message['intent']['name']
        cantidad=''
        for letra in texto:
            if str.isdigit(letra):
                cantidad=cantidad+letra    
        message=self.get_interacciones(intent_name,cantidad)
        dispatcher.utter_message(text=message)
        return []

class ActionMultimedia(Action):
    def name(self) -> Text:
        return "action_multimedia"
    
    def setRecurso(self,intent_name):
        if intent_name == 'imagenes':
            return "Indice imagen+1"
        elif intent_name == 'audio':
            return "Indice audio+1"
        elif intent_name == 'texto':
            return "Indice texto+1"
        return 'Indice no detectado'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name = tracker.latest_message['intent']['name']
        message=self.setRecurso(intent_name)
        dispatcher.utter_message(text=message)
        return []

class FormUserStorie(FormAction):
# your form functions go here
    def name(self):
        return "formUserStories"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot('iscomprensionUS') == False:
            return ["tiempo_empleado", "iscomprensionUS", "comprensionUS"]
        else:
            return ["tiempo_empleado", "iscomprensionUS"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "tiempo_empleado": [
                self.from_text(intent="tiempo"),
            ],
            "iscomprensionUS": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "comprensionUS": [
                self.from_entity(entity="entendimiento"),
            ],
        }
    def getIdUser(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        name=tracker.get_slot('user_name')
        id=0
        if name == 'Matias':    
            id=1
        if name == "Bruno":
            id=2
        return id
    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
            texto=tracker.get_slot('tiempo_empleado')
            cantidad=''
            for letra in texto:
                if str.isdigit(letra):
                    cantidad=cantidad+letra   
            msg = {
                'user_id': int(self.getIdUser(dispatcher,tracker,domain)),                      
                'factor_id': 0,                     
                'factor_name': 'TiempoTrabajoUS',
                'value_new_ocurr': int(cantidad)
            }
            print(requests.put(url_red, json = msg).json())   
            dispatcher.utter_message("Thanks, great job!")
            return []

class ActionUserName(Action):

    def name(self) -> Text:
        return "action_user_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        for e in tracker.latest_message['entities']:
             if e['entity'] == 'nombre_user':
                 username=e['value']
        print(username)
        return [SlotSet("user_name", username)]