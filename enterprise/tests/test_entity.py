from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class EntityModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating Test DB with enterprise ID 1 and entity ID 1
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
        # Url for entity ID 1
        self.url = reverse("enterprise:entity", args=[1])
    
    def test_get_valid_entity(self):
        '''
        Getting entity with ID 1
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_entity(self):
        '''
        Getting entity with ID 2, which does not exist
        '''
        response = self.client.get(reverse("enterprise:entity", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_valid_entity_list(self):
        '''
        Getting entity list with Enterprise ID 1
        '''
        response = self.client.get(reverse("enterprise:enterprise_entity_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # entering a new entity
        data = {
            "enterprise_id": self.enterprise,
            "entity_type": "IT",
            "entity_name": "Apple1",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple1@gmai.com"
        }
        Entity.objects.create(**data)
        response = self.client.get(reverse("enterprise:enterprise_entity_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_invalid_entity_list(self):
        '''
        Getting entity list with enterprise ID 2, which does not exist
        '''
        response = self.client.get(reverse("enterprise:enterprise_entity_list", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_entity(self):
        '''
        Posting a valid entity
        '''
        data = {
            "entity_type": "IT",
            "entity_name": "Apple1",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple1@gmai.com"
        }
        response = self.client.post(reverse("enterprise:enterprise_entity_list", args=[1]), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["entity_name"], "Apple1")
    
    def test_post_invalid_entity(self):
        '''
        Posting an entity with invalid info
        '''
        data = {
            "entity_type": "",
            "entity_name": "Apple1",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple1@gmai.com"
        }
        response = self.client.post(reverse("enterprise:enterprise_entity_list", args=[1]), data)
        self.assertEqual(response.status_code, 400)
        data = {
            "entity_type": "IT",
            "entity_name": "",
            "entity_primary_address": "",
            "entity_primary_email": "apple1@gmai.com"
        }
        response = self.client.post(reverse("enterprise:enterprise_entity_list", args=[1]), data)
        self.assertEqual(response.status_code, 400)
        # Posting entity with enterpirse id 2 which does not exist
        response = self.client.post(reverse("enterprise:enterprise_entity_list", args=[2]), data)
        self.assertEqual(response.status_code, 404)

    
    def test_patch_valid_valid_entity(self):
        '''
        Patching/Updating Entity with ID 1 with entity_primary_email
        '''
        data = {
            "entity_primary_email": "apple3@gmai.com"
        }
        data = json.dumps(data)
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("entity_primary_email"), "apple3@gmai.com")
    
    def test_patch_invalid_entity(self):
        '''
        Patching Entity with ID 1 with invalid data
        '''
        data = {
            "entity_primary_email": "ap.com"
        }
        data = json.dumps(data)
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # Patching Entity with ID 2 with entity_primary_email which does not exist
        data = {
            "entity_primary_email": "apple1@gmai.com"
        }
        data = json.dumps(data)
        response = self.client.patch(reverse("enterprise:entity", args=[2]), data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_valid_entity(self):
        # Deleting entity with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_entity(self):
        # Deleting entity with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        # Again deleting entity with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 400)
        # Deleting entity with ID 2 which does not exist
        response = self.client.delete(reverse("enterprise:entity", args=[2]))
        self.assertEqual(response.status_code, 404)
        