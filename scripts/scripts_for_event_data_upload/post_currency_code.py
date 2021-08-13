import requests
import json
 
def post_currency_code():
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/currency_code"
    
    abs_url = base_url+endpoint
 
    currency_codes = [
        {
            "currency_code" : "USD"
        },
        {
            "currency_code" : "INR"
        }
    ]
 
    for currency_code in currency_codes:
        response = requests.post(abs_url, currency_code)
        print(response.status_code)

post_currency_code()