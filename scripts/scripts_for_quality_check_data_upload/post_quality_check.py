import requests
import json

def post_quality_check(goods_receipt_entry_id=1):
    base_url = "http://127.0.0.1:8000/quality_check"
    endpoint = "/quality_check_list"+"/"+str(goods_receipt_entry_id)
    data = {
        "quality_check_info":{
            "goods_receipt_entry_id": goods_receipt_entry_id,
            "created_by_user_id": 1,
            "created_by_name": "Matt Parr",
            "created_by_phone": "91xxxx11",
            "created_by_email": "mattparr@factwise.io",
            "quality_check_reason": "Tested",
            "measurement_unit_id": 1,
            "quantity_rejected": 10
        }
    }

    headers = {
        "Content-Type": "application/json"
    }
    abs_url = base_url+endpoint
    response = requests.post(abs_url, data=json.dumps(data), headers=headers)
    print(response.status_code)

post_quality_check(1)