import requests
import json

def post_draft_event():
    base_url = "http://127.0.0.1:8000/event"
    endpoint = "/draft_event"


    abs_url = base_url+endpoint

    draft_events = [
        {  
           "event_id": 1, 
           "enterprise_id": 1,
           "buyer_id" : 1, 
           "event_name": "Buy", 
           "event_type": "RFQ", 
           "event_start_datetime": "2021-05-17T09:49:43.583737Z", 
           "event_end_datetime": "2021-05-17T09:49:43.583737Z", 
           "buyer_billing_address_id": 1, 
           "buyer_shipping_address_id": 2, 
           "event_delivery_datetime": "2021-05-17T09:49:43.583737Z", 
           "payment_terms_code": "USD", 
           "created_by_user_id": 1, 
           "created_by_name": "ll", 
           "created_by_phone": "xxxxxx991", 
           "created_by_email": "ll@gmail.com", 
           "status": "Draft", 
           "last_modified_by_user_id": 1
        }
    ]
    
    for draft_event in draft_events:
        response = requests.post(abs_url, draft_event)
        print(response.status_code)

post_draft_event()