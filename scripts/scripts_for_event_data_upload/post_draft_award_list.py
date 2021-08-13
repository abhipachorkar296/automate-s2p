import requests
import json

def post_draft_award_list(event_id=1):
    base_url = "http://127.0.0.1:8000/event"
    endpoint = "/draft_award_list/"+str(event_id)

    award_list = [
        {
            "award_info": {
                "event_id": 1, 
                "creator_user_id": 1,
                "approver_user_id": 2, 
                "draft_purchase_order_id": 0, 
                "purchase_order_id": 0,
                "buyer_id": 1, 
                "seller_id": 3, 
                "seller_bid_id": "1234",
                "award_creation_datetime": "2021-06-01T06:08:20.014493Z", 
                "payment_terms_code": "USD", 
                "currency_code": "USD", 
                "subtotal": 500, 
                "taxes": 100, 
                "total_shipping_cost": 0, 
                "total_other_charges": 0,
                "bulk_discount_percentage": 5, 
                "bulk_discount_amount": 30, 
                "total": 570, 
                "deal_status": "Deal Awarded"
            },
            "award_item_list": [
                {
                    "item_info": { 
                        "event_line_item_id": 1, 
                        "measurement_unit_id": 1, 
                        "quantity_offered": 500, 
                        "quantity_awarded": 100, 
                        "currency_code": "USD", 
                        "price": 900, 
                        "other_charges": 0, 
                        "shipping_managed_by": "B", 
                        "shipping_cost": 0, 
                        "total_amount": 90000
                    },
                    "item_tax": [
                        {
                            "tax_name": "GST",
                            "value": 5
                        },
                        {
                            "tax_name": "CGST",
                            "value": 5
                        }
                    ]
                }
            ]
        }
    ]

    headers = {
        'Content-Type': 'application/json'
    }
    abs_url = base_url+endpoint
    response = requests.post(abs_url, data=json.dumps(award_list), headers=headers)
    print(response.status_code)

post_draft_award_list(1)