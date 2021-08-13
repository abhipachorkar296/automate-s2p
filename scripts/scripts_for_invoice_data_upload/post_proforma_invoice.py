import requests
import json

def post_proforma_invoice(purchase_order_id=1):
    base_url = "http://127.0.0.1:8000/invoice"
    endpoint = "/proforma_invoice_list/"+str(purchase_order_id)

    abs_url = base_url+endpoint

    data = {
        "invoice_info": { 
            "purchase_order_id": purchase_order_id, 
            "buyer_purchase_order_id": "131", 
            "created_by_user_id": 2, 
            "invoice_creation_datetime": "2021-06-22T07:40:55.646607Z",
            "seller_id": 3, 
            "buyer_id": 1, 
            "seller_comments": "Please pay this much before goods need to be transported.", 
            "status": "issued", 
            "currency_code": "USD", 
            "amount_invoiced": "2000", 
            "amount_paid": 0
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    abs_url = base_url+endpoint
    response = requests.post(abs_url, data=json.dumps(data), headers=headers)
    print(response.status_code)

post_proforma_invoice(1)