from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class ItemAttributeModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db with a item with ID 1 and an attribute with ID 1
        entering an item attribute with item with ID 1 and attribute with ID 1
        '''
        data = {
            "item_name": "IPhone",
            "item_description": "An Apple Product"
        }
        Item.objects.create(**data)
        self.item = Item.objects.get(item_id=1)
        data = {
            "attribute_name": "RAM",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**data)
        self.attribute = Attribute.objects.get(attribute_id=1)
        data = {
            "item_id": self.item,
            "attribute_id": self.attribute
        }
        ItemAttribute.objects.create(**data)
    
    def test_get_valid_item_attribute(self):
        # Getting item attribute list with item id 1
        response = self.client.get(reverse("enterprise:get_item_attribute_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["item_id"], 1)
        self.assertEqual(response.data[0]["attribute_id"], 1)

    def test_get_invalid_item_attribute(self):
        # Getting item attribute list with item id 2 which does not exist
        response = self.client.get(reverse("enterprise:get_item_attribute_list", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_item_attribute(self):
        # Posting a valid item attribute with an existing item and attribute
        data = {
            "attribute_name": "Color",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**data)
        response = self.client.post(reverse("enterprise:item_attribute", args=[1,2]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["item_id"], 1)
        self.assertEqual(response.data["attribute_id"], 2)
        data = {
            "item_name": "Macbook",
            "item_description": "An Apple Product"
        }
        Item.objects.create(**data)
        response = self.client.post(reverse("enterprise:item_attribute", args=[2,2]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["item_id"], 2)
        self.assertEqual(response.data["attribute_id"], 2)
    
    def test_post_invalid_item_attribute(self):
        # Posting an item_attribute which is already existing
        response = self.client.post(reverse("enterprise:item_attribute", args=[1,1]))
        self.assertEqual(response.status_code, 400)
        # Posting an item_attribute with item id 2 which does not exist
        response = self.client.post(reverse("enterprise:item_attribute", args=[2,1]))
        self.assertEqual(response.status_code, 404)
    
    def test_delete_valid_item_attribute(self):
        # Deleting an item_attribute with item id 1 and attribute id 1
        response = self.client.delete(reverse("enterprise:item_attribute", args=[1,1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_item_attribute(self):
        # Deleting an item_attribute with item id 1 and attribute id 1
        response = self.client.delete(reverse("enterprise:item_attribute", args=[1,1]))
        self.assertEqual(response.status_code, 200)
        # Again deleting an item_attribute with item id 1 and attribute id 1
        response = self.client.delete(reverse("enterprise:item_attribute", args=[1,1]))
        self.assertEqual(response.status_code, 404)