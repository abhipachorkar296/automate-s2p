from django.test import TestCase
from django.urls import reverse
import json
from enterprise.models import *
from enterprise.serializers import *
class MeasurementUnitModelViewTest(TestCase):
    def setUp(self):
        '''
        Making a clear database with Measurement unit
        '''
        data = {
            "measurement_unit_primary_name" : "meter",
            "measurement_unit_category" : "length",
            "measurement_unit_value_type" : "Dec"
        }
        MeasurementUnit.objects.create(**data)
    
    def test_get_valid_measurement_unit(self):
        '''
        Getting MeasurementUnit with ID 1, a valid response
        '''
        response = self.client.get(reverse("enterprise:get_measurement_unit", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("measurement_unit_primary_name"), "meter")
    
    def test_get_invalid_measurement_unit(self):
        '''
        Getting MeasurementUnit with ID 2, which is not existing
        '''
        response = self.client.get(reverse("enterprise:get_measurement_unit", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_valid_all_measurement_unit(self):
        '''
        Getting all measurement units
        '''
        response = self.client.get(reverse("enterprise:measurement_unit"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["measurement_unit_primary_name"], "meter")
        self.assertEqual(response.data[0]["measurement_unit_category"], "length")

    def test_post_valid_measurement_unit(self):
        '''
        Posting a new MeasurementUnit
        '''
        data = {
            "measurement_unit_primary_name" : "cm",
            "measurement_unit_category" : "length",
            "measurement_unit_value_type" : "Dec"
        }
        response = self.client.post(reverse("enterprise:measurement_unit"), data)
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid_measurement_unit(self):
        '''
        Posting an measurement unit with a pre-existing measurement_unit_primary_name , 
        violating unique measruemetn_unit_primary_name
        '''
        data = {
            "measurement_unit_primary_name" : "meter",
            "measurement_unit_category" : "length",
            "measurement_unit_value_type" : "Dec"
        }

        response = self.client.post(reverse("enterprise:measurement_unit"), data)
        self.assertEqual(response.status_code, 400)
    
    def test_delete_valid_measurement_unit(self):
        '''
        Deleting an measurement_unit with ID 1
        '''
        response = self.client.delete(reverse("enterprise:get_measurement_unit", args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_measurement_unit(self):
        # Deleting an measurement_unit with ID 1
        response = self.client.delete(reverse("enterprise:get_measurement_unit", args=[1]))
        self.assertEqual(response.status_code, 200)
        # Again Deleting the measurement_unit with ID 1
        response = self.client.delete(reverse("enterprise:get_measurement_unit", args=[1]))
        self.assertEqual(response.status_code, 404)
        # Deleting an measurement_unit with ID 2 which does not exist
        response = self.client.delete(reverse("enterprise:get_measurement_unit", args=[2]))
        self.assertEqual(response.status_code, 404)
