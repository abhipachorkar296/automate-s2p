from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class ItemModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating Test DB with an item
        '''
        data = {
            "item_name": "IPhone",
            "item_description": "An Apple Product"
        }
        Item.objects.create(**data)
        # url for item with id 1
        self.url = reverse("enterprise:item", args=[1])
    
    def test_get_valid_item(self):
        '''
        Getting item with ID 1
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["item_id"], 1)
        self.assertEqual(response.data["item_name"], "IPhone")

    def test_get_invalid_item(self):
        '''
        Getting Item with ID 2, which does not exist
        '''
        response = self.client.get(reverse("enterprise:item", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_item_list(self):
        '''
        Getting all item list
        '''
        response = self.client.get(reverse("enterprise:item_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        data = {
            "item_name": "Macbook",
            "item_description": ""
        }
        Item.objects.create(**data)
        response = self.client.get(reverse("enterprise:item_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_post_valid_item(self):
        '''
        Posting a new item
        '''
        data = {
            "item_name": "Macbook",
            "item_description": ""
        }
        response = self.client.post(reverse("enterprise:item_list"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["item_id"], 2)
        self.assertEqual(response.data["item_name"], "Macbook")
    
    def test_post_invalid_item(self):
        '''
        Posting a new item with invalid info
        '''
        data = {
            "item_name": "IPhone"
        }
        response = self.client.post(reverse("enterprise:item_list"), data)
        self.assertEqual(response.status_code, 400)

    def test_patch_valid_item(self):
        '''
        Patching item with ID 1 with name
        '''
        data = {
            "item_name": "IPhone1"
        }
        data = json.dumps(data)
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("item_name"), "IPhone1")
    
    def test_patch_invalid_item(self):
        data = {
            "item_name": "Macbook",
            "item_description": ""
        }
        Item.objects.create(**data)
        data = {
            "item_name": "Macbook"
        }
        data = json.dumps(data)
        # Patching a item with id 1 with name of item with ID 2, 
        # violating unique item name constraints
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_delete_valid_item(self):
        # Deleting item with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_item(self):
        # Deleting item with id 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        # Again deleting item with id 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 404)