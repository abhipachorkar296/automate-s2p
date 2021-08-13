import requests
import json

def post_entity_identification():
    base_url = "http://127.0.0.1:8000/purchase_order"
    endpoint = "/entity_identification_list"

    data = [
        {
            "entity_id": 1,
            "identification_name": "GST",
            "identification_category": "GST",
            "identification_value": "1234557"
        },
        {
            "entity_id": 1,
            "identification_name": "CGST",
            "identification_category": "GCST",
            "identification_value": "1234557"
        },
        {
            "entity_id": 3,
            "identification_name": "GST",
            "identification_category": "GST",
            "identification_value": "1234557"
        },
        {
            "entity_id": 4,
            "identification_name": "CGST",
            "identification_category": "GCST",
            "identification_value": "1234557"
        }
    ]
    
    headers = {
        "Content-Type": "application/json"
    }
    abs_url = base_url+endpoint
    response = requests.post(abs_url, data=json.dumps(data), headers=headers)
    print(response.status_code)

post_entity_identification()