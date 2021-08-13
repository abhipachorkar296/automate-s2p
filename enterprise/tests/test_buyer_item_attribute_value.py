from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class BuyerItemAtrributeValueViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db 
        Entering a event with event_id 1
        '''
        Enterprise.objects.create(enterprise_name="ENT 1")
        self.enterprise = Enterprise.objects.get(enterprise_id=1)
        user_data = {
            "enterprise_id": self.enterprise,
            "user_email": "apple1@gmail.com",
            "user_firstname": "Pratyush",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**user_data)
        self.user = User.objects.get(user_id=1)
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
        self.buyer_item = BuyerItem.objects.get(entry_id=1)
        BuyerItem.objects.create(**buyer_item_data2)
        attribute_data = {
            "attribute_name": "RAM",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**attribute_data)
        self.attribute = Attribute.objects.get(attribute_id=1)
        data = {
            "buyer_item_entry_id" : self.buyer_item,
            "attribute_id" : self.attribute,
            "attribute_value" : "16GB"
        }
        BuyerItemAttributeValue.objects.create(**data)

    def test_get_valid_buyer_item_attribute_value_list(self):
        '''
        Getting buyer_item_attribute_value_list with entry_id 1
        '''
        response = self.client.get(reverse("enterprise:buyer_item_attribute_value_list" , args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["attribute_value"], "16GB")
        self.assertEqual(response.data[0]["attribute_id"], 1)

    def test_get_invalid_buyer_item_attribute_value_list(self):
        '''
        Getting buyer_item_attribute_value_list with entry_id 3
        '''
        response = self.client.get(reverse("enterprise:buyer_item_attribute_value_list" , args=[3]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_buyer_item_attribute_value_list(self):
        '''
        Posting a new buyer_item_attribute_value_list
        '''
        attribute_data = {
            "attribute_name": "Hard Disk",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**attribute_data)
        data = {
            "buyer_item_entry_id" : 1,
            "attribute_id" : 2,
            "attribute_value" : "1TB"
        }
        response = self.client.post(reverse("enterprise:buyer_item_attribute_value_list" , args=[1]), data)
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid_buyer_item_attribute_value_list(self):
        '''
        Posting a new buyer_item_attribute_value_list with invalid info
        '''
        attribute_data = {
            "attribute_name": "Hard Disk",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**attribute_data)
        data = {
            "buyer_item_entry_id" : 1,
            "attribute_id" : 3,
            "attribute_value" : "1TB"
        }
        response = self.client.post(reverse("enterprise:buyer_item_attribute_value_list" , args=[1]), data)
        self.assertEqual(response.status_code, 404)