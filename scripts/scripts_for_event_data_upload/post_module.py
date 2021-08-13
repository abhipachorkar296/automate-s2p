import requests
import json

def post_module():
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/module"


    abs_url = base_url+endpoint

    modules = [
        {
            "module_name": "Events"
        },
        {
            "module_name": "Payment"
        }
    ]
    
    for module in modules:
        response = requests.post(abs_url, module)
        print(response.status_code)

post_module()