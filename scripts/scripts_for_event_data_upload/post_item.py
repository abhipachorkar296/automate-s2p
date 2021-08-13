import requests
import json

def post_item():
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/item"


    abs_url = base_url+endpoint

    items = [
        {
            "item_name": "IPhone",
            "item_description": "An Apple Product"
        },
        {
            "item_name": "MacBook"
        }
    ]
    
    for item in items:
        response = requests.post(abs_url, item)
        print(response.status_code)

post_item()