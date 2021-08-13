import requests
import json

def post_measurement_unit():
    base_url = "http://127.0.0.1:8000/enterprise"
    endpoint = "/measurement_unit"


    abs_url = base_url+endpoint

    measurement_units = [
    {
        "measurement_unit_primary_name" : "meter",
        "measurement_unit_category" : "length",
        "measurement_unit_value_type" : "dec"
    },
    {
        "measurement_unit_primary_name" : "cm",
        "measurement_unit_category" : "length",
        "measurement_unit_value_type" : "dec"
    }
]
    
    for measurement_unit in measurement_units:
        response = requests.post(abs_url, measurement_unit)
        print(response.status_code)

post_measurement_unit()