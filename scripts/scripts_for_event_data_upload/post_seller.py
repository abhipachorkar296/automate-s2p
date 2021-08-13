import requests
import json

def post_seller():
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/seller/"


    abs_url = base_url+endpoint
    sellers = [3, 4] # Entity Ids
    
    for seller in sellers:
        response = requests.post(abs_url+str(seller))
        print(response.status_code)

post_seller()