from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class UserEntityModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db with enterprise, user and Entity with ID 1
        Entering a user_entity with user id 1 and entity id 1
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
        user_data = {
            "enterprise_id": self.enterprise,
            "user_email": "apple1@gmail.com",
            "user_firstname": "Pratyush",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**user_data)
        self.client.post(reverse("enterprise:post_user_entity", args=[1,1]))
    
    def test_get_valid_user_entity_list(self):
        '''
        Getting user_entity list with user id 1
        '''
        response = self.client.get(reverse("enterprise:get_user_entity_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_id"], 1)
    
    def test_get_invalid_user_entity_list(self):
        '''
        Getting user_entity list with user_id 2 which does not exist
        '''
        response = self.client.get(reverse("enterprise:get_user_entity_list", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_entity_list(self):
        # Entering new user and entity with ID 2 for both
        user_data = {
            "enterprise_id": self.enterprise,
            "user_email": "apple1@gmail.com",
            "user_firstname": "Abhi",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**user_data)
        response = self.client.post(reverse("enterprise:post_user_entity", args=[2,1]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user_id"], 2)
        self.assertEqual(response.data["entity_id"], 1)
        entity_data = {
            "enterprise_id": self.enterprise,
            "entity_type": "IT 1",
            "entity_name": "Apple",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple@gmai.com"
        }
        Entity.objects.create(**entity_data)
        # Posting a user_entity with user id 2 and entity id 2
        response = self.client.post(reverse("enterprise:post_user_entity", args=[2,2]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user_id"], 2)
        self.assertEqual(response.data["entity_id"], 2)

    def test_post_invalid_entity_list(self):
        '''
        Posting a user_entity with user id 1 and entity id 1, which already exists
        violating unique_together constraint
        '''
        response = self.client.post(reverse("enterprise:post_user_entity", args=[1,1]))
        self.assertEqual(response.status_code, 400)
    
    def test_delete_valid_user_entity_list(self):
        # Deleting user_entity with user_id 1 and entity_id 1
        response = self.client.delete(reverse("enterprise:post_user_entity", args=[1,1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_user_entity_list(self):
        # Deleting user_entity with user_id 1 and entity_id 1
        response = self.client.delete(reverse("enterprise:post_user_entity", args=[1,1]))
        self.assertEqual(response.status_code, 200)
        # Again deleting user_entity with user_id 1 and entity_id 1
        response = self.client.delete(reverse("enterprise:post_user_entity", args=[1,1]))
        self.assertEqual(response.status_code, 400)
        # Deleting user_entity with user_id 2 and entity_id 2, which does not exist
        response = self.client.delete(reverse("enterprise:post_user_entity", args=[2,2]))
        self.assertEqual(response.status_code, 404)
