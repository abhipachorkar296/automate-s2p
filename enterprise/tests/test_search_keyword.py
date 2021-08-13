from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class SearchKeyWordViewTest(TestCase):
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
        BuyerItem.objects.create(**buyer_item_data2)

    def test_get_valid_search_keyword_result(self):
        '''
        Getting keyword_search with user_id 1 and searchword IPhone
        '''
        response = self.client.get(reverse("enterprise:search_keyword_buyer_items_result" , args=[1,"IPhone"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["item_id"], 1)
        self.assertEqual(response.data[0]["buyer_item_id"], "20013")
        self.assertEqual(response.data[1]["buyer_item_id"], "20014")

    def test_get_invalid_search_keyword_result(self):
        '''
        Getting keyword_search with user_id 2, which does not exist
        '''
        response = self.client.get(reverse("enterprise:search_keyword_buyer_items_result" , args=[2,"Ip" ]))
        self.assertEqual(response.status_code, 404)
    
    