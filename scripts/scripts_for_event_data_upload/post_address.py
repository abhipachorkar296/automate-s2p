
from django.http import response
import requests
import json

def post_address():
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/address"


    abs_url = base_url+endpoint

    addresses = [
        {
             "address_nickname": "Berkeley Office",
            "country": "USA",
            "address1": "215 Dwight Way, Berkeley, CA 97074",
            "city" : "berkeley",
            "postal_code" : 97074
        },
        {
            "address_nickname": "New York Headquarters",
            "country": "USA",
            "address1": "156 Street Way, New York, NY 67809",
            "city" : "New York",
            "postal_code" : 67809
        }
    ]
    
    # for address in addresses:
    #     response = requests.post(abs_url, address)
    #     print(response.status_code)
    response = requests.post(abs_url, json=addresses, headers={'Content-Type': 'application/json'})
    print(response.status_code)

post_address()