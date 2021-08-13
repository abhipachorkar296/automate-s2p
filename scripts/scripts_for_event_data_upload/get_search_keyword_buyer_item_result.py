from django.http import response
import requests
import json

def get_keyword_search_result(user_id=1):
    base_url = "http://127.0.0.1:8000/enterprise/"
    endpoint = "search_keyword_buyer_items_result/" + str(user_id)+"/"


    abs_url = base_url+endpoint

    keywords = ["iphone", "macbook", "IPHO"]
    
    for keyword in keywords:
        print(abs_url+keyword)
        response = requests.get(abs_url+keyword)
        print(response.status_code)
        print(response.text)

get_keyword_search_result(1)