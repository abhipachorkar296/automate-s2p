import requests
import json

def post_draft_event_item_attribute(event_line_item_id=1):
    base_url = "http://127.0.0.1:8000/event"
    endpoint = "/draft_event_item_attribute/"+str(event_line_item_id)


    abs_url = base_url+endpoint

    draft_event_item_attributes = [
        {
            "attribute_id": 1,
            "attribute_value": "RED"
        },
        {
            "attribute_id": 2,
            "attribute_value": "4GB"
        }
    ]
    headers = {
        'Content-Type': 'application/json'
    }
    
    # for draft_event_item_attribute in draft_event_item_attributes:
    #     response = requests.post(abs_url, draft_event_item_attribute)
    #     print(response.status_code)
    response = requests.post(abs_url, json.dumps(draft_event_item_attributes), headers=headers)
    print(response.status_code)

post_draft_event_item_attribute(2)