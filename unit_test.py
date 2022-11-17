
        
predictionKey = "df24026daeb14c39ace8906b63ccbb95"
predictionEndpoint = "res-name.cognitiveservices.azure.com"
predictionEndpoint = "https://res-name.cognitiveservices.azure.com/"
app_id = "d5faaa9c-9a65-4b51-a994-ae05432f13fe"

from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient

runtimeCredentials = CognitiveServicesCredentials(predictionKey)
clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)


predictionRequest = { "query" : "book a flight from paris to berlin for the 12/12/12 until 12/12/22 for $1200 max" }

predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
prediction_entities = predictionResponse.prediction.entities

assert prediction_entities['budget'] == [{'money': [{'number': 1200, 'units': 'Dollar'}]}]