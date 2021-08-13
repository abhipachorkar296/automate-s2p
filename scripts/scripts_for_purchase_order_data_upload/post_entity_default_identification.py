import requests
import json

def post_entity_default_identification():
    base_url = "http://127.0.0.1:8000/purchase_order"
    endpoint = "/entity_default_identification_list"

    data = [
        {
            "entity_id": 1,
            "identification_id": 1
        },
        {
            "entity_id": 1,
            "identification_id": 2
        },
        {
            "entity_id": 3,
            "identification_id": 3
        }
    ]
    
    headers = {
        "Content-Type": "application/json"
    }
    abs_url = base_url+endpoint
    response = requests.post(abs_url, data=json.dumps(data), headers=headers)
    print(response.status_code)

post_entity_default_identification()