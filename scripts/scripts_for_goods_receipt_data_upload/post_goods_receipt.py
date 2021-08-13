import requests
import json

def post_goods_receipt(user_id=1, invoice_line_item_id=1):
    base_url = "http://127.0.0.1:8000/goods_receipt"
    endpoint = "/goods_receipt_list"+"/"+str(user_id)+"/"+str(invoice_line_item_id)
    data = {
        "goods_receipt_info": {
            "invoice_line_item_id": 1,
            "buyer_goods_receipt_id": "12",
            "receiving_user_id": user_id,
            "receiving_user_name": "Matt Par",
            "receiving_user_email": "matt@factwise.io",
            "measurement_unit_id": 1,
            "delivered_quantity": 30,
            "porblem_category": "111",
            "receipt_quantity_accepted": 20,
            "receipt_quantity_rejected": 10
        },
        "invoice_info": {
            "status": "ongoing",
            "payment_due_date": "2021-05-17T09:49:43.583737Z",
            "amount_due": "2300"
        }
    }

    headers = {
        "Content-Type": "application/json"
    }
    abs_url = base_url+endpoint
    # response = requests.post(abs_url, data=json.dumps(data), headers=headers)
    # print(response.status_code)
    response = requests.post(abs_url, data=json.dumps(data), headers=headers)
    print(response.status_code)

post_goods_receipt(1, 1)