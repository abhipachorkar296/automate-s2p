import requests
import json

def post_draft_event_item_seller(event_line_item_id=1):
    base_url = "http://127.0.0.1:8000/event"
    endpoint = "/draft_event_item_seller/"+str(event_line_item_id)


    abs_url = base_url+endpoint

    draft_event_item_sellers = [
        {
            "seller_id": 3
        },
        {
            "seller_id": 4
        }
    ]
    headers = {
        'Content-Type': 'application/json'
    }
    
    # for draft_event_item_seller in draft_event_item_sellers:
    #     response = requests.post(abs_url, draft_event_item_seller)
    #     print(response.status_code)
    response = requests.post(abs_url, json.dumps(draft_event_item_sellers), headers=headers)
    print(response.status_code)

post_draft_event_item_seller(1)