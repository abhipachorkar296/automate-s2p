import requests
import json

def post_entity_address(entity_id=1):
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/entity_address/"+str(entity_id)


    abs_url = base_url+endpoint

    entity_addresses = [
        {  
            "address_id": 1,
            "is_billing_address": True,
            "is_shipping_address": True,
            "order_id" : 1
        },
        {
            "address_id": 2,
            "is_billing_address": True,
            "is_shipping_address": False,
            "order_id" : 1
        }
    ]
    
    for entity_address in entity_addresses:
        response = requests.post(abs_url, entity_address)
        print(response.status_code)

post_entity_address(1)
