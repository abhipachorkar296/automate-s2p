from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class BuyerSellerRelationshipModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db with Enterprise, Buyer, Entity and Seller with ID 1
        Entering a buyer_seller_relationship_list with buyer id 1 and seller id 1
        '''
        Enterprise.objects.create(enterprise_name="ENT 1")
        self.enterprise1 = Enterprise.objects.get(enterprise_id=1)
        entity_data1 = {
            "enterprise_id": self.enterprise1,
            "entity_type": "IT",
            "entity_name": "Apple",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple@gmail.com"
        }
        Entity.objects.create(**entity_data1)
        self.entity1 = Entity.objects.get(entity_id=1)
        buyer_data = {
            "buyer_id" : self.entity1
        }
        Buyer.objects.create(**buyer_data)
        self.buyer = Buyer.objects.get(buyer_id=1)
        Enterprise.objects.create(enterprise_name="ENT 2")
        self.enterprise2 = Enterprise.objects.get(enterprise_id=2)
        entity_data2 = {
            "enterprise_id": self.enterprise2,
            "entity_type": "IT1",
            "entity_name": "Apple1",
            "entity_primary_address": "xyz1",
            "entity_primary_email": "apple1@gmail.com"
        }
        Entity.objects.create(**entity_data2)
        self.entity2 = Entity.objects.get(entity_id=2)
        seller_data = {
            "seller_id" : self.entity2
        }
        Seller.objects.create(**seller_data)
        self.seller = Seller.objects.get(seller_id=2)
        data = {
            "buyer_enterprise_id" : self.enterprise1,
            "buyer_entity_id" : self.buyer,
            "seller_entity_id" : self.seller,
            "relationship_type" : "xcvz"
        }
        BuyerSellerRelationship.objects.create(**data)
    
    def test_get_valid_buyer_seller_relationship(self):
        '''
        Getting buyer_seller_relationship with buyer_id 1
        '''
        response = self.client.get(reverse("enterprise:get_buyer_seller_relationship_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["buyer_enterprise_id"], 1)
        self.assertEqual(response.data[0]["seller_entity_id"], 2)
    
    def test_get_invalid_buyer_seller_relationship(self):
        '''
        Getting buyer_seller_relationship with buyer_id 2 which does not exist
        '''
        response = self.client.get(reverse("enterprise:get_buyer_seller_relationship_list", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_buyer_seller_relationship(self):
        # Entering new entity and address in entity address with id 2
        Enterprise.objects.create(enterprise_name="ENT 3")
        self.enterprise3 = Enterprise.objects.get(enterprise_id=3)
        entity_data3 = {
            "enterprise_id": self.enterprise3,
            "entity_type": "IT3",
            "entity_name": "Apple3",
            "entity_primary_address": "xyz3",
            "entity_primary_email": "apple3@gmail.com"
        }
        Entity.objects.create(**entity_data3)
        self.entity3 = Entity.objects.get(entity_id=3)
        buyer_data = {
            "buyer_id" : self.entity3
        }
        Buyer.objects.create(**buyer_data)
        self.buyer = Buyer.objects.get(buyer_id=3)
        Enterprise.objects.create(enterprise_name="ENT 4")
        self.enterprise4 = Enterprise.objects.get(enterprise_id=4)
        entity_data4 = {
            "enterprise_id": self.enterprise4,
            "entity_type": "IT4",
            "entity_name": "Apple4",
            "entity_primary_address": "xyz4",
            "entity_primary_email": "apple4@gmail.com"
        }
        Entity.objects.create(**entity_data4)
        self.entity4 = Entity.objects.get(entity_id=4)
        seller_data = {
            "seller_id" : self.entity4
        }
        Seller.objects.create(**seller_data)
        self.seller = Seller.objects.get(seller_id=4)
        data = {
            "relationship_type" : "xcvz"
        }
        # Posting a entity_address with address id 2 and entity id 2
        response = self.client.post(reverse("enterprise:buyer_seller_relationship_list", args=[3,4]),data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["buyer_enterprise_id"], 3)
        self.assertEqual(response.data["relationship_type"], "xcvz")

    def test_post_invalid_buyer_seller_relationship(self):
        '''
        Posting a buyer_seller_relationship with seller id 1 and buyer id 1, which already exists
        violating unique_together constraint
        '''
        data = {
            "relationship_type" : "xcvz"
        }
        response = self.client.post(reverse("enterprise:buyer_seller_relationship_list", args=[1,2]),data)
        self.assertEqual(response.status_code, 400)

        '''
        Posting buyer and sellers with nonexisting ids
        '''
        #invalid seller id
        response = self.client.post(reverse("enterprise:buyer_seller_relationship_list", args=[1,4]), data)
        self.assertEqual(response.status_code, 404)
        #invalid buyer id
        response = self.client.post(reverse("enterprise:buyer_seller_relationship_list", args=[3,2]), data)
        self.assertEqual(response.status_code, 404)
        
    def test_delete_valid_buyer_seller_relationship(self):
        # Deleting buyer_seller_relationship with id 1
        response = self.client.delete(reverse("enterprise:buyer_seller_relationship_list", args=[1,2]))
        self.assertEqual(response.status_code, 200)
        
    def test_delete_invalid_buyer_seller_relationship(self):
        '''
        Posting buyer and sellers with nonexisting ids
        '''
        #invalid seller id
        response = self.client.delete(reverse("enterprise:buyer_seller_relationship_list", args=[1,4]))
        self.assertEqual(response.status_code, 404)
        #invalid buyer id
        response = self.client.delete(reverse("enterprise:buyer_seller_relationship_list", args=[3,2]))
        self.assertEqual(response.status_code, 404)

        # Deleting buyer_seller_relationship with buyer id 1 seller id 2
        response = self.client.delete(reverse("enterprise:buyer_seller_relationship_list", args=[1,2]))
        self.assertEqual(response.status_code, 200)
        # Again deleting buyer_seller_relationship with buyer id 1 seller id 2
        response = self.client.delete(reverse("enterprise:buyer_seller_relationship_list", args=[1,2]))
        self.assertEqual(response.status_code, 400)
    