from django.db import reset_queries
from django.test import TestCase
from django.urls import reverse
import json

from rest_framework import response

from enterprise.models import *
from enterprise.serializers import *

class BuyerItemModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db with required entries
        '''
        Enterprise.objects.create(enterprise_name="ENT 1")
        self.enterprise = Enterprise.objects.get(enterprise_id=1)
        item_data = {
            "item_name": "IPhone",
            "item_description": "An Apple Product"
        }
        Item.objects.create(**item_data)
        self.item = Item.objects.get(item_id=1)
        buyer_item_data1 = {
            "enterprise_id" : self.enterprise,
            "buyer_item_id": "20013",
            "buyer_item_name": "20013 IPhone - White",
            "item_id": self.item
        }
        buyer_item_data2 = {
            "enterprise_id" : self.enterprise,
            "buyer_item_id": "20014",
            "buyer_item_name": "20014 IPhone - Black",
            "item_id": self.item
        }
        BuyerItem.objects.create(**buyer_item_data1)
        BuyerItem.objects.create(**buyer_item_data2)
    
    def test_get_valid_buyer_item(self):
        # Getting buyer_item with entry_id 1
        response = self.client.get(reverse("enterprise:buyer_item", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["buyer_item_id"], "20013")
        self.assertEqual(response.data["buyer_item_name"], "20013 IPhone - White")
        # Getting buyer_item with entry_id 2
        response = self.client.get(reverse("enterprise:buyer_item", args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["buyer_item_id"], "20014")
        self.assertEqual(response.data["buyer_item_name"], "20014 IPhone - Black")
    
    def test_get_valid_buyer_item_list(self):
        # Getting buyer_item list with enterprise id 1
        response = self.client.get(reverse("enterprise:buyer_item_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["buyer_item_id"], "20013")
        self.assertEqual(response.data[0]["buyer_item_name"], "20013 IPhone - White")
        self.assertEqual(response.data[1]["buyer_item_id"], "20014")
        self.assertEqual(response.data[1]["buyer_item_name"], "20014 IPhone - Black")
    
    def test_get_invalid_buyer_item(self):
        # Getting buyer_item with entry_id 3 which does not exist
        response = self.client.get(reverse("enterprise:buyer_item", args=[3]))
        self.assertEqual(response.status_code, 404)

    def test_get_invalid_buyer_item_list(self):
        # Getting buyer_item list with enterprise id 2 which does not exist
        response = self.client.get(reverse("enterprise:buyer_item_list", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_buyer_item_list(self):
        # Posting a buyer item with enterprise id 1
        data = {
            "buyer_item_id": "20015",
            "buyer_item_name": "20015 IPhone - RED",
            "item_id": 1
        }
        response = self.client.post(reverse("enterprise:buyer_item_list", args=[1]), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["entry_id"], 3)
        self.assertEqual(response.data["buyer_item_id"], "20015")
    
    def test_post_invalid_buyer_item_list(self):
        # Posting a buyer item with enterprise id 1 and item_id 2 which does not exist
        data = {
            "buyer_item_id": "20015",
            "buyer_item_name": "20015 IPhone - RED",
            "item_id": 2
        }
        response = self.client.post(reverse("enterprise:buyer_item_list", args=[1]), data=data)
        self.assertEqual(response.status_code, 400)
        # Posting a buyer item with enterprise id 2 which does not exist
        data = {
            "buyer_item_id": "20015",
            "buyer_item_name": "20015 IPhone - RED",
            "item_id": 1
        }
        response = self.client.post(reverse("enterprise:buyer_item_list", args=[2]), data=data)
        self.assertEqual(response.status_code, 404)
    
    def test_patch_valid_buyer_item(self):
        # Patching a buyer item with entry_id 1 with buyer_item_name
        data = {
            "buyer_item_name": "20015 IPhone - RED - 256GB Storage"
        }
        response = self.client.patch(reverse("enterprise:buyer_item", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["entry_id"], 1)
        self.assertEqual(response.data["buyer_item_name"], "20015 IPhone - RED - 256GB Storage")
    
    def test_patch_invalid_buyer_item(self):
        # Patching a buyer item with entry_id 1 with item_id which does not exist
        data = {
            "item_id": 2
        }
        response = self.client.patch(reverse("enterprise:buyer_item", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # Patching a buyer item with entry_id 3 which does not exist
        data = {
            "item_id": 1
        }
        response = self.client.patch(reverse("enterprise:buyer_item", args=[3]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)
    
    def test_delete_valid_buyer_item(self):
        # Deleting a buyer_item with entery_id 1
        response = self.client.delete(reverse("enterprise:buyer_item", args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_buyer_item(self):
        # Deleting a buyer_item with entery_id 1
        response = self.client.delete(reverse("enterprise:buyer_item", args=[1]))
        self.assertEqual(response.status_code, 200)
        # Again deleting a buyer_item with entery_id 1
        response = self.client.delete(reverse("enterprise:buyer_item", args=[1]))
        self.assertEqual(response.status_code, 400)
        # Deleting a buyer_item with entery_id 3 which does not exist
        response = self.client.delete(reverse("enterprise:buyer_item", args=[3]))
        self.assertEqual(response.status_code, 404)