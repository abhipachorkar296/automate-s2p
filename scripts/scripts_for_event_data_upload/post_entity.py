import requests
import json

def post_enterprise_entity1(enterprise_id=1):
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/enterprise_entity/"+str(enterprise_id)


    abs_url = base_url+endpoint

    enterprise_entities = [
        {
            "entity_type": "IT",
            "entity_name": "Apple",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple@gmai.com"
        },
        {
            "entity_type": "IT",
            "entity_name": "Apple1",
            "entity_primary_address": "xyz1",
            "entity_primary_email": "apple1@gmai.com"
        }
    ]
    
    for entity in enterprise_entities:
        response = requests.post(abs_url,entity)
        print(response.status_code)

post_enterprise_entity1(1)

def post_enterprise_entity2(enterprise_id=2):
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/enterprise_entity/"+str(enterprise_id)


    abs_url = base_url+endpoint

    enterprise_entities = [
        {
            "entity_type": "T",
            "entity_name": "pple",
            "entity_primary_address": "yz",
            "entity_primary_email": "pple@gmai.com"
        },
        {
            "entity_type": "T",
            "entity_name": "pple1",
            "entity_primary_address": "yz1",
            "entity_primary_email": "pple1@gmai.com"
        }
    ]
    
    for entity in enterprise_entities:
        response = requests.post(abs_url,entity)
        print(response.status_code)

post_enterprise_entity2(2)