import requests
import json



def get_event_code(year,tag):
    params = (
        ('tags', tag),('season', year),
    )
    response = requests.get('https://api.isuresults.eu/events/', params=params)
    response_dict = json.loads(response.text)
    results = response_dict['results']
    event_code = results[0]['isuId']
    return event_code

