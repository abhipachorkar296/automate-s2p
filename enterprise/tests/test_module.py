from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class ModuleModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db with a module
        '''
        data = {
            "module_name": "Events"
        }
        Module.objects.create(**data)
        # url for module with id 1
        self.url = reverse("enterprise:module", args=[1])
    
    def test_get_valid_module(self):
        '''
        Getting module with id 1
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_module(self):
        '''
        Getting module with id 2 which does not exist
        '''
        response = self.client.get(reverse("enterprise:module", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_module_list(self):
        '''
        Getting module list
        '''
        response = self.client.get(reverse("enterprise:get_module_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # Entering a new module
        data = {
            "module_name": "PO"
        }
        Module.objects.create(**data)
        # Again getting the new list
        response = self.client.get(reverse("enterprise:get_module_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_post_valid_module(self):
        '''
        Posting a new module with valid data
        '''
        data = {
            "module_name": "PO"
        }
        response = self.client.post(reverse("enterprise:get_module_list"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["module_id"], 2)
    
    def test_post_invalid_module(self):
        '''
        Posting a module with name which alredy exists
        '''
        data = {
            "module_name": "Events"
        }
        response = self.client.post(reverse("enterprise:get_module_list"), data)
        self.assertEqual(response.status_code, 400)

    def test_patch_valid_module(self):
        '''
        Patching module with id 1 with module name
        '''
        data = {
            "module_name": "EVENTS"
        }
        data = json.dumps(data)
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("module_name"), "EVENTS")
    
    def test_patch_invalid_module(self):
        # Entering a new module with name PO
        data = {
            "module_name": "PO"
        }
        self.client.post(reverse("enterprise:get_module_list"), data)
        data = json.dumps(data)
        # Patching module with id 1 with name of the module with id 2
        # violating unique module name constraint
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_delete_valid_module(self):
        # Deleting module with id 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_module(self):
        # Deleting module with id 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        # Again deleting module with id 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 404)