from django.test import TestCase
from django.urls import reverse
import json
from enterprise.models import *
from enterprise.serializers import *
class ItemMeasurementUnitModelViewTest(TestCase):
    def setUp(self):
        '''
        Making a clear database with ItemMeasurement unit
        '''
        item_data ={
            "item_name": "IPhone",
            "item_description": "An Apple Product"
        }
        Item.objects.create(**item_data)
        self.item = Item.objects.get(item_id=1)
        measurement_unit_data = {
            "measurement_unit_primary_name" : "meter",
            "measurement_unit_category" : "length",
            "measurement_unit_value_type" : "Dec"
        }
        MeasurementUnit.objects.create(**measurement_unit_data)
        self.measurement_unit = MeasurementUnit.objects.get(measurement_unit_id=1)
        data = {
            "item_id" : self.item,
            "measurement_unit_id" : self.measurement_unit
        }
        ItemMeasurementUnit.objects.create(**data)
    
    def test_get_valid_measurement_unit(self):
        '''
        Getting MeasurementUnit with item_id 1 using ItemMeasurementUnit, a valid response
        '''
        response = self.client.get(reverse("enterprise:get_item_measurement_unit", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["measurement_unit_primary_name"], "meter")
    
    def test_get_invalid_measurement_unit(self):
        '''
        Getting MeasurementUnit with item_id 1 using ItemMeasurementUnit, a invalid response
        '''
        response = self.client.get(reverse("enterprise:get_item_measurement_unit", args=[2]))
        self.assertEqual(response.status_code, 404)
    def test_get_valid_all_measurement_unit(self):
        '''
        Getting all item measurement units
        '''
        response = self.client.get(reverse("enterprise:item_measurement_unit"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["item_id"], 1)
        self.assertEqual(response.data[0]["measurement_unit_id"], 1)
    def test_post_valid_item_measurement_unit(self):
        '''
        Posting a new ItemMeasurementUnit
        '''
        item_data ={
            "item_name": "IPone",
            "item_description": "AnApple Product"
        }
        Item.objects.create(**item_data)
        self.item = Item.objects.get(item_id=2)
        measurement_unit_data = {
            "measurement_unit_primary_name" : "cm",
            "measurement_unit_category" : "length",
            "measurement_unit_value_type" : "Dec"
        }
        MeasurementUnit.objects.create(**measurement_unit_data)
        self.measurement_unit = MeasurementUnit.objects.get(measurement_unit_id=2)
        data = {
            "measurement_unit_id" : 2
        }
        response = self.client.post(reverse("enterprise:get_item_measurement_unit", args=[2]), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data[0]["measurement_unit_id"], 2)
    def test_post_invalid_item_measurement_unit(self):
        '''
        Posting an item measurement unit with with wrong measurement_unit_id, item_id
        '''
        item_data ={
            "item_name": "IP",
            "item_description": "AnAppleProduct"
        }
        Item.objects.create(**item_data)
        self.item = Item.objects.get(item_id=2)
        measurement_unit_data = {
            "measurement_unit_primary_name" : "mm",
            "measurement_unit_category" : "length",
            "measurement_unit_value_type" : "Dec"
        }
        MeasurementUnit.objects.create(**measurement_unit_data)
        self.measurement_unit = MeasurementUnit.objects.get(measurement_unit_id=2)
        data = {
            "measurement_unit_id" : 3
        }
        # with wrong measurement_unit_id
        response = self.client.post(reverse("enterprise:get_item_measurement_unit", args=[2]), data)
        self.assertEqual(response.status_code, 400)
        # with wrong item_id
        response = self.client.post(reverse("enterprise:get_item_measurement_unit", args=[3]), data)
        self.assertEqual(response.status_code, 404)
    def test_delete_valid_item_measurement_unit(self):
        '''
        Deleting an item_measurement_unit with ID 1
        '''
        response = self.client.delete(reverse("enterprise:delete_item_measurement_unit", args=[1,1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_measurement_unit(self):
        '''
        Deleting same item measurement unit twice
        '''
        response = self.client.delete(reverse("enterprise:delete_item_measurement_unit", args=[1,1]))
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(reverse("enterprise:delete_item_measurement_unit", args=[1,1]))
        self.assertEqual(response.status_code, 404)
        '''
        Deleting an item_measurement_unit with ID 2 which does not exist
        '''
        response = self.client.delete(reverse("enterprise:delete_item_measurement_unit", args=[2,2]))
        self.assertEqual(response.status_code, 404)  
