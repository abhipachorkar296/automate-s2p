import requests
import json

def post_draft_po(event_id=1, seller_id=3):
    base_url = "http://127.0.0.1:8000/purchase_order"
    endpoint = "/draft_purchase_order_list/"+str(event_id)+"/"+str(seller_id)

    data = {
        "purchase_order_info": {
            "purchase_order_id": 1, 
            "event_id": 1, 
            "purchase_order_creation_datetime": "2021-05-17T09:49:43.583737Z", 
            "buyer_id": 1, 
            "buyer_purchase_order_id": "1233", 
            "buyer_entity_name": "Factwise", 
            "buyer_billing_address_id": 1, 
            "buyer_shipping_address_id": 2, 
            "buyer_approver_user_id": 1, 
            "buyer_approver_name": "Pratyush", 
            "buyer_contact_user_id": 1, 
            "buyer_contact_name": "Abhishek", 
            "buyer_contact_phone": "9xxxxxx12", 
            "buyer_contact_email": "jaiswalpratyush2015@gmail.com", 
            "is_freight_purchase_order": "False", 
            "seller_id": 3, 
            "seller_entity_name": "Apple", 
            "seller_address_id": 2, 
            "seller_contact_user_id": 2, 
            "seller_contact_name": "Nishant", 
            "seller_contact_phone": "9xxxxx12", 
            "seller_contact_email": "apple1@gmail.com", 
            "seller_acknowledgement_user_id": 2, 
            "seller_acknowledgement_datetime": "2021-05-17T09:49:43.583737Z",
            "delivery_schedule_type": "kfiuw", 
            "payment_terms_code": "USD", 
            "purchase_order_discount_percentage": 0, 
            "buyer_comments": "Nothing", 
            "status": "issued"
        },
        "purchase_order_item_list": [
            {
                "item_info": {
                    "item_id": 1, 
                    "buyer_item_id": "20013", 
                    "buyer_item_name": "20013 IPhone - White", 
                    "buyer_item_description": "", 
                    "due_date": "2021-05-17T09:49:43.583737Z", 
                    "currency_code": "USD", 
                    "measurement_unit_id": 1, 
                    "rate": 100, 
                    "quantity": 100,
                    "shipping_per_unit": 5,
                    "max_acceptable_quantity": 150, 
                    "taxes_and_charges_percentage": 0, 
                    "taxes_and_charges_value": 0,
                    "total_order_value": 11500
                },
                "item_attribute": [
                    {
                        "attribute_id": 1,
                        "attribute_value": "BLUE"
                    },
                    {
                        "attribute_id": 2,
                        "attribute_value": "8GB"
                    }
                ],
                "item_charge": [
                    {
                        "charge_name": "GST",
                        "charge_percentage": 5
                    },
                    {
                        "charge_name": "CGST",
                        "charge_percentage": 5
                    }
                ]
            }
            
        ],
        "purchase_order_buyer_information": [
            {
                "buyer_id": 1,
                "identification_id": 1,
                "identification_name": "GST",
                "identification_value": "1234557"
            }
        ],
        "purchase_order_seller_information": [
            {
                "seller_id": 3,
                "identification_id": 3,
                "identification_name": "CGST",
                "identification_value": "1234557"
            }
        ]
    }
    


    headers = {
        "Content-Type": "application/json"
    }
    abs_url = base_url+endpoint
    response = requests.post(abs_url, data=json.dumps(data), headers=headers)
    print(response.status_code)

post_draft_po(1,3)