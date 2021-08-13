import requests
import json

def post_draft_award_list_shift_award(event_id=1):
    base_url = "http://127.0.0.1:8000/event"
    endpoint = "/draft_award_list_shift_award/"+str(event_id)


    abs_url = base_url+endpoint
    response = requests.post(abs_url)
    print(response.status_code)

post_draft_award_list_shift_award(1)