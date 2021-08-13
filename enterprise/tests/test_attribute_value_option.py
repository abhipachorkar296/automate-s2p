from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class AttributeValueOptionModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating Test DB with an attribute and attribute_value_option
        '''
        data = {
            "attribute_name": "Color",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**data)
        self.attribute = Attribute.objects.get(attribute_id=1)
        data = {
            "attribute_id": self.attribute,
            "value": "Red"
        }
        AttributeValueOption.objects.create(**data)
        # url for attribute_value_option list with attribute ID 1
        self.url = reverse("enterprise:attribute_value_option", args=[1])
    
    def test_get_valid_attribute_value_option(self):
        '''
        Getting attribute_value_option_list with attribute ID 1
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # List will be having length 1 
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["attribute_id"], 1)
        self.assertEqual(response.data[0]["value"], "Red")

    def test_get_invalid_attribute_value_option(self):
        '''
        Getting attribute_value_option_list with attribute ID 2 
        which doesn't exist
        '''
        response = self.client.get(reverse("enterprise:attribute_value_option", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_attribute_value_option(self):
        '''
        Posting an attribute_value_option for attribute with ID 1
        '''
        data = {
            "value": "Blue"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["attribute_id"], 1)
        self.assertEqual(response.data["value"], "Blue")
    
    def test_post_invalid_attribute_value_option(self):
        '''
        Posting attribute_value_option for attribute with ID 2 
        which does not exist
        '''
        data = {
            "value": "Blue"
        }
        response = self.client.post(reverse("enterprise:attribute_value_option", args=[2]), data)
        self.assertEqual(response.status_code, 404)
        '''
        Posting attribute_value_option with invalid dtaa for attribute with ID 1
        '''
        data = {
            "value": ""
        }
        response = self.client.post(reverse("enterprise:attribute_value_option", args=[1]), data)
        self.assertEqual(response.status_code, 400)
        data = {}
        response = self.client.post(reverse("enterprise:attribute_value_option", args=[1]), data)
        self.assertEqual(response.status_code, 400)