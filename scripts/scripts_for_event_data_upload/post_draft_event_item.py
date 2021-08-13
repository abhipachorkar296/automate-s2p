import requests
import json

def post_draft_event_item(event_id=1):
    base_url = "http://127.0.0.1:8000/event"
    endpoint = "/draft_event_item_list/"+str(event_id)


    abs_url = base_url+endpoint

    draft_event_items = [
        {
            "item_info": {
                "currency_code": "USD",
                'item_id': 1, 
                'buyer_item_id': "200012 Iphone - Black", 
                'description': "Just an exp", 
                'measurement_unit_id': 1, 
                'meausrement_unit': "meters", 
                'desired_quantity': 100, 
                'currency_code': "USD", 
                'desired_price': 950, 
                'opening_bid': 950, 
                'total_amount': 100000
            },
            "item_attribute": [
                {
                    "attribute_id": 1,
                    "attribute_value": "BLUE"
                },
                {
                    "attribute_id": 2,
                    "attribute_value": "4GB"
                }
            ]
        }
    ]
    
    for draft_event_item in draft_event_items:
        response = requests.post(abs_url, json.dumps(draft_event_item), headers = {'content-type':'application/json'})
        print(response.status_code)

post_draft_event_item(1)