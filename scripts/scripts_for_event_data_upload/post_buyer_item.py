import requests
import json

def post_buyer_item(enterprise_id=1):
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/enterprise_buyer_item/"+str(enterprise_id)


    abs_url = base_url+endpoint

    buyer_items = [
        {
            "buyer_item_id": "20013",
            "buyer_item_name": "20013 IPhone - White",
            "item_id": 1
        },
        {
            "buyer_item_id": "20014",
            "buyer_item_name": "20014 IPhone - Black",
            "item_id": 1
        }
    ]
    
    for buyer_item in buyer_items:
        response = requests.post(abs_url,buyer_item)
        print(response.status_code)

post_buyer_item(1)