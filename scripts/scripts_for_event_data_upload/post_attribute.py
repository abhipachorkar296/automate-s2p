import requests
import json

def post_attribute():
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/attribute"


    abs_url = base_url+endpoint

    attributes = [
        {
            "attribute_name": "Density",
            "attribute_value_type": "enum"
        },
        {
            "attribute_name": "RAM",
            "attribute_value_type": "enum"
        }
    ]
    
    for attribute in attributes:
        response = requests.post(abs_url, attribute)
        print(response.status_code)

post_attribute()