from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class BuyerModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating Test DB with enterprise ID 1 and entity ID 1
        Entering the entity into Buyer Model with ID 1
        '''
        Enterprise.objects.create(enterprise_name="ENT 1")
        self.enterprise = Enterprise.objects.get(enterprise_id=1)
        data = {
            "enterprise_id": self.enterprise,
            "entity_type": "IT",
            "entity_name": "Apple",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple@gmai.com"
        }
        Entity.objects.create(**data)
        self.entity = Entity.objects.get(entity_id=1)
        data = {
            "buyer_id": self.entity
        }
        Buyer.objects.create(**data)
    
    def test_get_valid_buyer_list(self):
        '''
        Getting the buyer list
        '''
        response = self.client.get(reverse("enterprise:get_buyer_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # Entering a new entity
        data = {
            "enterprise_id": self.enterprise,
            "entity_type": "IT",
            "entity_name": "Apple1",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple1@gmai.com"
        }
        Entity.objects.create(**data)
        entity = Entity.objects.get(entity_id=2)
        Buyer.objects.create(buyer_id=entity)
        # Getting the new list with length 2
        response = self.client.get(reverse("enterprise:get_buyer_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_post_valid_buyer(self):
        '''
        Posting a valid Buyer
        '''
        data = {
            "enterprise_id": self.enterprise,
            "entity_type": "IT",
            "entity_name": "Apple1",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple1@gmai.com"
        }
        Entity.objects.create(**data)
        response = self.client.post(reverse("enterprise:post_buyer", args=[2]))
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid_buyer(self):
        '''
        Posting a buyer which already exists
        '''
        response = self.client.post(reverse("enterprise:post_buyer", args=[1]))
        self.assertEqual(response.status_code, 400)
        # Posting an entity into Buyer which does not exist
        response = self.client.post(reverse("enterprise:post_buyer", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_delete_valid_buyer(self):
        # Deleting a buyer with ID 1
        response = self.client.delete(reverse("enterprise:post_buyer", args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_buyer(self):
        # Deleting a buyer with ID 1
        response = self.client.delete(reverse("enterprise:post_buyer", args=[1]))
        self.assertEqual(response.status_code, 200)
        # Again deleting a buyer with ID 1
        response = self.client.delete(reverse("enterprise:post_buyer", args=[1]))
        self.assertEqual(response.status_code, 400)
        # Deleting a buyer with ID 2, which does not exist
        response = self.client.delete(reverse("enterprise:post_buyer", args=[2]))
        self.assertEqual(response.status_code, 404)