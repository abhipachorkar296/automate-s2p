import requests
import json

def post_user_entity(user_id, entity_id):
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/user_entity/"+str(user_id)+"/"+str(entity_id)


    abs_url = base_url+endpoint

    response = requests.post(abs_url)
    print(response.status_code)

post_user_entity(1,1)
post_user_entity(1,2)
post_user_entity(2,3)
post_user_entity(2,4)