subscription_key = "2292fabc461849e2ad69949ede7ea881"
text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"

import requests
from pprint import pprint

headers   = {"Ocp-Apim-Subscription-Key": subscription_key}

sentiment_api_url = text_analytics_base_url + "sentiment"

print(sentiment_api_url)

documents = {'documents' : [
  {'id': '1', 'language': 'en', 'text': 'Very good Experience'},
  {'id': '2', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},  
  {'id': '3', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},  
  {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]}
# headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
response  = requests.post(sentiment_api_url, headers=headers, json=documents,verify=False)
sentiments = response.json()
print(sentiments['documents'][0]['score'])
pprint(sentiments)
