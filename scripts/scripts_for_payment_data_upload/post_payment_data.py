from django.http import response
import requests
import json

def post_payment_data(user_id=1, entity_id=1):
    base_url = "http://127.0.0.1:8000/payment/"
    endpoint = "payment_list/" + str(user_id)+"/" +str(entity_id)


    abs_url = base_url+endpoint

    data = {
        "payment_info":{
            "payment_category":"prepayment",
            "to_entity_id":3,
            "currency_code":"USD",
            "base_payment_amount":1.01,
            "payment_mode" : "ll",
            "payment_reference" : "ll",
            "applied_balance_amount" : 1.01,
            "total_amount" : 2.02,
            "comments" : "ll"
        },
        "invoice_item_list":[
            {
                "invoice_line_item_id":1,
                "amount_applied":2.02
            }
        ],
    }
    
    response = requests.post(abs_url, json=data, headers={'Content-Type': 'application/json'})
    print(response.status_code)
    
    data = {
        "payment_info":{
            "payment_category":"invoice_payment",
            "to_entity_id":3,
            "currency_code":"USD",
            "base_payment_amount":1.01,
            "payment_mode" : "ll",
            "payment_reference" : "ll",
            "applied_balance_amount" : 1.01,
            "total_amount" : 2.02,
            "comments" : "ll"
        },
        "invoice_item_list":[
            {
                "invoice_line_item_id":1,
                "amount_applied":2.02
            }
        ],
        "balance_usage":[
            {
                "balance_id":1,
                "used_amount": 1.01,
                "available_amount":1.01,
                "comments":"ll"
            }
        ]
    }
    
    response = requests.post(abs_url, json=data, headers={'Content-Type': 'application/json'})
    print(response.status_code)

post_payment_data(1,1)

