import requests
import json

def post_enterprise_user1(enterprise_id=1):
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/enterprise_user/"+str(enterprise_id)


    abs_url = base_url+endpoint

    enterprise_users = [
        {
            "user_email": "apple1@gmail.com",
            "user_firstname": "Pratyush",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
    ]
    
    for user in enterprise_users:
        response = requests.post(abs_url,user)
        print(response.status_code)

post_enterprise_user1(1)

def post_enterprise_user2(enterprise_id=2):
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/enterprise_user/"+str(enterprise_id)


    abs_url = base_url+endpoint

    enterprise_users = [
        {
            "user_email": "apple1@gmail.com",
            "user_firstname": "Pratyush",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
    ]
    
    for user in enterprise_users:
        response = requests.post(abs_url,user)
        print(response.status_code)

post_enterprise_user2(2)