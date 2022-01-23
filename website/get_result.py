from website.get_event_code import get_event_code
from website.get_events import get_events
import requests
import json


def get_result(year,tag):
    event_code = get_event_code(year, tag)
    scheduleNumbers, events_with_spaces, starttimes = get_events(year,tag)
    events = []
    for q in events_with_spaces:
        r = q.replace(' ', '')
        events.append(r)

    # Get the results
    results = {}
    names = []
    podium_pictures = {}
    podium_event = []

    for i in range(len(scheduleNumbers)):
        response_result = requests.get('https://api.isuresults.eu/events/'
                                       + event_code
                                       + '/competitions/'
                                       + scheduleNumbers[i]
                                       + '/results/'
                                       )
        response_result_dict = json.loads(response_result.text)
        for j in range(len(response_result_dict)):
            if response_result_dict[j]:
                if response_result_dict[j]['time'] is not None:
                    key = 'competitor'
                    if key in response_result_dict[j]:
                        Full_name = str(response_result_dict[j]['competitor']['skater']['firstName']
                                        + " "
                                        + response_result_dict[j]['competitor']['skater']['lastName']
                                        + "   ("
                                        + response_result_dict[j]['competitor']['skater']['country']
                                        + ")"
    #                                    + response_result_dict[j]['time']
                                        )
                        if j < 3:
                            podium_url = response_result_dict[j]['competitor']['skater']['photo']
                            podium_event.append(podium_url)
                            podium_url = None

                        names.append(Full_name)
                    key2 = "team"
                    if key2 in response_result_dict[j]:
                        Full_name = str(response_result_dict[j]['team']['country']
                                        +" "
    #                                    + response_result_dict[j]['time']
                                                            )
                        names.append(Full_name)
                else:
                    key = 'competitor'
                    if key in response_result_dict[j]:
                        Full_name = str(response_result_dict[j]['competitor']['skater']['firstName']
                                        + " "
                                        + response_result_dict[j]['competitor']['skater']['lastName']
                                        + "   ("
                                        + response_result_dict[j]['competitor']['skater']['country']
                                        + ") "
                                        )
                        names.append(Full_name)
                    key2 = "team"
                    if key2 in response_result_dict[j]:
                        Full_name = str(response_result_dict[j]['team']['country'])
                        names.append(Full_name)
            results[str("startlist_" + events[i])] = names
            podium_pictures[str("startlist_" + events[i])] = podium_event
        names = []
        podium_event = []
    return results, podium_pictures
