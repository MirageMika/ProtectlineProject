# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

import requests,json


import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Launch Request Handler
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        #Check if the request is LaunchRequest if yes then launch function handle
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = "Bonjour, c'est votre système d'alarme"
        ask_output   = "Que puis-je faire pour vous ?"
        return (
            handler_input.response_builder
                .speak(speak_output) # Say what is in "speak_output"
                .ask(ask_output)   # If no answer then ask what is in "ask_output"
                .response
        )



# Function to send to the back end 
def armAlarm():
    
    # data that we want to send to our backend
    data = {'type':"0"}
    # Transform our dictionnary into jsonstring
    data = json.dumps(data) 
    
    # Add information for our http request
    headers = {'Content-Type': 'application/json',}
    response_dict = {}
    try:
        #Send answer and get response
        req = requests.post('https://a865v31iwe.execute-api.eu-west-3.amazonaws.com/dev',headers=headers, data=data)
        response_dict = req.json()["body"]
    except:
        print("")
    return response_dict


def send_passcode(passcode):
    
    # data that we want to send to our backend
    data = {'type':"1",'passcode': str(passcode)}
    # Transform our dictionnary into jsonstring
    data = json.dumps(data) 
    
    # Add information for our http request
    headers = {'Content-Type': 'application/json',}
    response_dict = {}
    try:
        #Send answer and get response
        req = requests.post('https://a865v31iwe.execute-api.eu-west-3.amazonaws.com/dev',headers=headers, data=data)
        response_dict = req.json()["body"]
    except:
        print("")
    return response_dict

def disableAlarm():
    
    # data that we want to send to our backend
    data = {'type':"2"}
    # Transform our dictionnary into jsonstring
    data = json.dumps(data) 
    
    # Add information for our http request
    headers = {'Content-Type': 'application/json',}
    response_dict = {}
    try:
        #Send answer and get response
        req = requests.post('https://a865v31iwe.execute-api.eu-west-3.amazonaws.com/dev',headers=headers, data=data)
        response_dict = req.json()["body"]
    except:
        print("")
    return response_dict

def send_voice_recognized():
    
    # data that we want to send to our backend
    data = {'type':"3",'isRecognized': True}
    # Transform our dictionnary into jsonstring
    data = json.dumps(data) 
    
    # Add information for our http request
    headers = {'Content-Type': 'application/json',}
    response_dict = {}
    try:
        #Send answer and get response
        req = requests.post('https://a865v31iwe.execute-api.eu-west-3.amazonaws.com/dev',headers=headers, data=data)
        response_dict = req.json()["body"]
    except:
        print("")
    return response_dict


### Function not use because the features has been aborted during the project

# # Function to send the answer of the question received by the back end
# def send_answer(answer):
# # data that we want to send to our backend
#     data = {'type':"2",'answer':answer}
# # Transform our dictionnary into jsonstring
#     data = json.dumps(data) 
# # Add information for our http request
#     headers = {'Content-Type': 'application/json',}
#     req = requests.post('https://a865v31iwe.execute-api.eu-west-3.amazonaws.com/dev',headers=headers, data=data)
#     response_dict = req.json()["body"]
#     return response_dict



#Handler for Passcode Intent 
class CapturePasscodeIntentHandler(AbstractRequestHandler):
    #Check if the intent triggered is this one, if yes then go into handle function
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Passcode")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        #Take slots received from alexa
        slots = handler_input.request_envelope.request.intent.slots
        #In this handler the slot should be digits
        passcode = slots["digits"].value
        
        #Sending passcode to back and receive response
        response_dict = json.loads(send_passcode(passcode))
        
        #If the passcode sent is correct say that the alarm is desactivated
        if response_dict['iscorrect']:
            speak_output = "Merci, le code a bien été reconnu. Système d'alarme désactivé"
            return (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
        #If the passcode sent is not correct ask the passcode
        else :
            ask_output = "Le code {passcode} n'a pas été reconnu, veuillez réessayer".format(passcode=passcode)
            return (
            handler_input.response_builder
                .speak(ask_output)
                .ask(ask_output)
                .response
            )
        


#Handler for TrustedUser Intent 
class CaptureTrustedUserIntentHandler(AbstractRequestHandler):
    #Check if the intent triggered is this one, if yes then go into handle function
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TrustedUser")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        consentToken = handler_input.request_envelope.context.system.api_access_token
        person = handler_input.request_envelope.context.system.person
        
        #Check if the person field exist if not then user not isn't recognized
        if person:
            disableAlarm()
            speak_output = "Personne reconnue, alarme désactivé"
            return (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            
        else:
            speak_output = "Personne non reconnue, veuillez dire le mot de passe"
            return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
            )
        


#Handler for ArmSystem Intent 
class CaptureArmSystemIntentHandler(AbstractRequestHandler):
    #Check if the intent triggered is this one, if yes then go into handle function
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_intent_name("ArmSystem")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        armAlarm()
        speak_output = "Système d'alarme activé, vous pouvez partir l'esprit léger"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        ) 
        
        
### Handler function not use because the features has been aborted during the project

# class CaptureAnswerIntentHandler(AbstractRequestHandler):

#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
        
        
#         #isPhase2 = getPhase()["phase"] == "2"
#         return ask_utils.is_intent_name("Answer")(handler_input)# && isPhase2

#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         slots = handler_input.request_envelope.request.intent.slots
        
        
#         animal = slots["animal"].value
#         date = slots["date"].value
#         firstName = slots["firstName"].value
#         country = slots["country"].value
#         number = slots["number"].value
        
#         slotsValue = [animal,date,firstName,country,number]
        
#         ans = None
#         for s in slotsValue:
#             if s != None :
#                 ans=s
#                 break
        
        
        
#         #Si le la requete n'a pas abouti
#         speak_output = "Un problème a surgi veuillez réessayer ou bien contacter le support"
#         response_dict = json.loads(send_answer(ans))
        
        
#         if response_dict['iscorrect'] :
#             speak_output = "Bonne réponse, l'alarme est désormait désactivé "
#         else :
#             speak_output   = "Mauvaise réponse." # Voici une nouvelle question {question}".format(question)
        
#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .response
#         )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bonjour, l'aide n'a pas encore été mise en place"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Au revoir!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, je ne suis pas sûr"
        reprompt = "Je n'ai pas compris, comment puis-je vous aider ?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Vous venez d'activer " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Oops, j'ai du mal. C'est pas faute pas celle des dévelloppeur"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )





# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

#Ajoutons les handler qu'on veut 
sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(CapturePasscodeIntentHandler())
# sb.add_request_handler(CaptureAnswerIntentHandler())
sb.add_request_handler(CaptureArmSystemIntentHandler())
sb.add_request_handler(CaptureTrustedUserIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
