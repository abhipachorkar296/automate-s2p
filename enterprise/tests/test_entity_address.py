from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class EntityAddressModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db with Enterprise, Entity and Address with ID 1
        Entering a entity_address with enterprise id 1 and entity id 1
        '''
        Enterprise.objects.create(enterprise_name="ENT 1")
        self.enterprise = Enterprise.objects.get(enterprise_id=1)
        entity_data = {
            "enterprise_id": self.enterprise,
            "entity_type": "IT",
            "entity_name": "Apple",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple@gmai.com"
        }
        Entity.objects.create(**entity_data)
        self.entity = Entity.objects.get(entity_id=1)
        address_data = {
            "address_nickname": "Berkeley Office",
            "country": "USA",
            "address1": "215 Dwight Way, Berkeley, CA 97074",
            "city" : "berkeley",
            "postal_code" : 97074
        }
        Address.objects.create(**address_data)
        self.address = Address.objects.get(address_id=1)
        data = {
            "entity_id" : self.entity,
            "address_id" : self.address,
            "is_billing_address": True,
            "is_shipping_address": True,
            "order_id" : 1
        }
        EntityAddress.objects.create(**data)
    
    def test_get_valid_entity_address(self):
        '''
        Getting entity_address with id 1
        '''
        response = self.client.get(reverse("enterprise:get_entity_address", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["entity_addresses"][0]["entity_id"], 1)
        self.assertEqual(response.data["entity_addresses"][0]["address_id"], 1)
    
    def test_get_invalid_entity_address(self):
        '''
        Getting user_entity list with user_id 2 which does not exist
        '''
        response = self.client.get(reverse("enterprise:get_user_entity_list", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_entity_address(self):
        # Entering new entity and address in entity address with id 2
        entity_data = {
            "enterprise_id": self.enterprise,
            "entity_type": "IT 1",
            "entity_name": "Apple",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple@gmai.com"
        }
        Entity.objects.create(**entity_data)
        self.entity = Entity.objects.get(entity_id=2)
        address_data = {
                "address_nickname": "New York Headquarters",
                "country": "USA",
                "address1": "156 Street Way, New York, NY 67809",
                "city" : "New York",
                "postal_code" : 67809
            }
        Address.objects.create(**address_data)
        self.address = Address.objects.get(address_id=2)
        data = {
            "address_id" : 2,
            "is_billing_address": True,
            "is_shipping_address": True,
            "order_id" : 1
        }
        # Posting a entity_address with address id 2 and entity id 2
        response = self.client.post(reverse("enterprise:get_entity_address", args=[2]),data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["address_id"], 2)
        self.assertEqual(response.data["entity_id"], 2)

    def test_post_invalid_entity_address(self):
        '''
        Posting a entity_address with address id 1 and entity id 1, which already exists
        violating unique_together constraint
        '''
        data = {
            "address_id" : 1,
            "is_billing_address": True,
            "is_shipping_address": True,
            "order_id" : 1
        }
        response = self.client.post(reverse("enterprise:get_entity_address", args=[1]),data)
        self.assertEqual(response.status_code, 400)
    
    def test_get_all_entity_address_list(self):
        '''
        Getting all entity addresses
        '''
        response = self.client.get(reverse("enterprise:entity_address"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["entity_id"], 1)
        self.assertEqual(response.data[0]["address_id"], 1)
    