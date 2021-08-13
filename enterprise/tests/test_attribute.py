from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class AttributeModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db with an attribute
        '''
        data = {
            "attribute_name": "Density",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**data)
         # url for attribute with ID 1
        self.url = reverse("enterprise:attribute", args=[1])
    
    def test_get_valid_attribute(self):
        '''
        Getting attribute with ID 1
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["attribute_id"], 1)
        self.assertEqual(response.data["attribute_name"], "Density")

    def test_get_invalid_attribute(self):
        '''
        Getting attribute with ID 2, which does not exist
        '''
        response = self.client.get(reverse("enterprise:attribute", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_attribute_list(self):
        '''
        Getting attribute list
        '''
        response = self.client.get(reverse("enterprise:get_attribute_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # Entering a new attribute
        data = {
            "attribute_name": "Color",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**data)
        response = self.client.get(reverse("enterprise:get_attribute_list"))
        self.assertEqual(response.status_code, 200)
        # Now the list of attributes will be of length 2
        self.assertEqual(len(response.data), 2)
    
    def test_post_valid_attribute(self):
        '''
        Posting an attribute with valid info
        '''
        data = {
            "attribute_name": "Color",
            "attribute_value_type": "enum"
        }
        response = self.client.post(reverse("enterprise:get_attribute_list"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["attribute_id"], 2)
    
    def test_post_invalid_attribute(self):
        '''
        Posting an attribute with invalid data
        '''
        data = {
            "attribute_name": "Color"
        }
        response = self.client.post(reverse("enterprise:get_attribute_list"), data)
        self.assertEqual(response.status_code, 400)
        # Posting a new attribute with a pre-existing attribute_name
        data = {
            "attribute_name": "Density",
            "attribute_value_type": "enum"
        }
        response = self.client.post(reverse("enterprise:get_attribute_list"), data)
        self.assertEqual(response.status_code, 400)

    def test_patch_valid_attribute(self):
        '''
        Patching attribute with ID 1 with attribute value type
        '''
        data = {
            "attribute_value_type": "enum1"
        }
        data = json.dumps(data)
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("attribute_value_type"), "enum1")
    
    def test_patch_invalid_attribute(self):
        # Entering a new attribute
        data = {
            "attribute_name": "Color",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**data)
        # Updating the name of the attribute with ID 1 with the 
        # name of attribute wiht ID 2, violating unique name constraint
        data = {
            "attribute_name": "Color"
        }
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # Updating an attribute with ID 3 which does not exist
        response = self.client.patch(reverse("enterprise:attribute", args=[3]), data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_valid_attribute(self):
        # Deleting attribute with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_valid_invalid_attribute(self):
        # Deleting attribute with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        # Again Deleting attribute with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 404)