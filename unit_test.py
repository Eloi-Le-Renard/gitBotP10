
predictionKey = "0af9b79b2d8e40479cd0d639e4940a2b"
predictionEndpoint = "https://res-namep10.cognitiveservices.azure.com/"
app_id = "b6d4fabd-7cb8-4329-90eb-aa5065d6f141"

from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient

runtimeCredentials = CognitiveServicesCredentials(predictionKey)
clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)


predictionRequest = { "query" : "book a flight from paris to berlin for the 12/12/12 until 12/12/22 for $1200 max" }
predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
prediction_entities = predictionResponse.prediction.entities
assert prediction_entities['budget'] == [{'money': [{'number': 1200, 'units': 'Dollar'}]}]
assert prediction_entities['or_city'] == [{'geographyV2': [{'value': 'paris', 'type': 'city'}]}]


predictionRequest = { "query" : "book a flight to berlin" }
predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
prediction_entities = predictionResponse.prediction.entities
assert prediction_entities['dst_city'] == [{'geographyV2': [{'value': 'berlin', 'type': 'city'}]}]


assert 1 == 2
