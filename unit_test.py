
predictionKey = "61a8d29177404906829359111ef928ea"
predictionEndpoint = "https://luise-api-p10.cognitiveservices.azure.com"
app_id = "992aa391-8f2e-4d23-ad82-be89361b9092"

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