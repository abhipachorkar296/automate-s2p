import requests
import json

def post_attribute_value_option(attribute_id):
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/attribute_value_option/"+str(attribute_id)


    abs_url = base_url+endpoint

    attribute_value_options = [
        {
            "value": "4GB"
        },
        {
            "value": "2GB"
        }
    ]
    
    for attribute_value_option in attribute_value_options:
        response = requests.post(abs_url, attribute_value_option)
        print(response.status_code)

post_attribute_value_option(1)