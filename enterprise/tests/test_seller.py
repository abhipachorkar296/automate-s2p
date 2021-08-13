from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class SellerModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating Test DB with enterprise ID 1 and entity ID 1
        Entering the entity into seller Model with ID 1
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
            "seller_id": self.entity
        }
        Seller.objects.create(**data)
    
    def test_get_valid_seller_list(self):
        '''
        Getting the seller list
        '''
        response = self.client.get(reverse("enterprise:get_seller_list"))
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
        # Entering this entity into seller 
        data = {
            "seller_id": entity
        }
        Seller.objects.create(**data)
        # Getting the new list with length 2
        response = self.client.get(reverse("enterprise:get_seller_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_post_valid_seller(self):
        '''
        Posting a valid seller
        '''
        data = {
            "enterprise_id": self.enterprise,
            "entity_type": "IT",
            "entity_name": "Apple1",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple1@gmai.com"
        }
        Entity.objects.create(**data)
        response = self.client.post(reverse("enterprise:post_seller", args=[2]))
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid_seller(self):
        '''
        Posting a seller which already exists
        '''
        response = self.client.post(reverse("enterprise:post_seller", args=[1]))
        self.assertEqual(response.status_code, 400)
        # Posting an entity into seller which does not exist
        response = self.client.post(reverse("enterprise:post_seller", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_delete_valid_seller(self):
        # Deleting a seller with ID 1
        response = self.client.delete(reverse("enterprise:post_seller", args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_seller(self):
        # Deleting a seller with ID 1
        response = self.client.delete(reverse("enterprise:post_seller", args=[1]))
        self.assertEqual(response.status_code, 200)
        # Again deleting a seller with ID 1
        response = self.client.delete(reverse("enterprise:post_seller", args=[1]))
        self.assertEqual(response.status_code, 400)
        # Deleting a seller with ID 2, which does not exist
        response = self.client.delete(reverse("enterprise:post_seller", args=[2]))
        self.assertEqual(response.status_code, 404)