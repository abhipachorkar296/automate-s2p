import requests
import json

def post_enterprise():
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/enterprise"


    abs_url = base_url+endpoint

    enterprises = [
        {
            "enterprise_name": "ENT 1"
        },
        {
            "enterprise_name": "ENT 2"
        }
    ]
    
    for enterprise in enterprises:
        response = requests.post(abs_url, enterprise)
        print(response.status_code)

post_enterprise()