import requests
import json

def post_buyer():
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/buyer/"


    abs_url = base_url+endpoint
    buyers = [1, 2] # Entity Ids
    
    for buyer in buyers:
        response = requests.post(abs_url+str(buyer))
        print(response.status_code)

post_buyer()