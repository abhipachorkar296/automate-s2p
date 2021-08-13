import requests
import json

def post_shift_draft_event(event_id=1):
    base_url = "http://127.0.0.1:8000/event"
    endpoint = "/draft_event_shift_event/"+str(event_id)


    abs_url = base_url+endpoint
    response = requests.post(abs_url)
    print(response.status_code)

post_shift_draft_event(1)