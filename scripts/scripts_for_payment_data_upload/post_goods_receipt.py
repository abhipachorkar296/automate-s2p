from django.http import response
import requests
import json

def post_goods_receipt(user_id=1, invoice_line_item_id=1):
    base_url = "http://localhost:8000/goods_receipt/"
    endpoint = "goods_receipt_list/" + str(user_id)+"/" +str(invoice_line_item_id)


    abs_url = base_url+endpoint

    data = {
        "goods_receipt_info":{
            "invoice_line_item_id" : 1,
            "buyer_goods_receipt_id" : "1134",
            "receiving_user_id" : 1,
            "receiving_user_name" : "ll",
            "receiving_user_email" : "matt@factwise.co",
            "measurement_unit_id" : 1,
            "delivered_quantity" : 0.5,
            "receipt_quantity_rejected" : 0,
            "receipt_quantity_accepted" : 0.1,
            "problem_category":"ll"
        },
        "invoice_info": {
				"status": "ongoing",
				"payment_due_date": "2021-06-25T10:18:44.950889Z",
				"amount_due": 1

			}
    }
    
    response = requests.post(abs_url, json=data, headers={'Content-Type': 'application/json'})
    print(response.status_code)
    
post_goods_receipt(1,1)

