from django.test import TestCase
from django.urls import reverse
import json
from enterprise.models import *
from enterprise.serializers import *
class UserModuleModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db with a user and module with ID 1 for both
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
        module_data = {
            "module_name": "Events"
        }
        Module.objects.create(**module_data)
        self.client.post(reverse("enterprise:user_module_list", args=[1,1]))
    
    def test_get_valid_user_module_list(self):
        '''
        Getting user_module list with user_id 1 with length 1
        '''
        response = self.client.get(reverse("enterprise:get_user_module_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_id"], 1)
        self.assertEqual(response.data[0]["module_id"], 1)
    
    def test_get_invalid_user_module_list(self):
        '''
        Getting user_module list with user_id 2 which does not exist
        '''
        response = self.client.get(reverse("enterprise:get_user_module_list", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_user_module_list(self):
        # Entering a new user and module
        user_data = {
            "enterprise_id": self.enterprise,
            "user_email": "apple1@gmail.com",
            "user_firstname": "Abhi",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**user_data)
        response = self.client.post(reverse("enterprise:user_module_list", args=[2,1]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user_id"], 2)
        self.assertEqual(response.data["module_id"], 1)
        module_data = {
            "module_name": "PO"
        }
        Module.objects.create(**module_data)
        # Posting a new user_module with user_id 2 and module_id 2
        response = self.client.post(reverse("enterprise:user_module_list", args=[2,2]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user_id"], 2)
        self.assertEqual(response.data["module_id"], 2)
    def test_post_invalid_user_module_list(self):
        # Posting an existing user_module with user_id 1 and module_id 1
        response = self.client.post(reverse("enterprise:user_module_list", args=[1,1]))
        self.assertEqual(response.status_code, 400)
        # Posting a user_module with user_id 2 which does not exist
        response = self.client.post(reverse("enterprise:user_module_list", args=[2,1]))
        self.assertEqual(response.status_code, 404)
        # Posting a user_module with module_id 2 which does not exist
        response = self.client.post(reverse("enterprise:user_module_list", args=[1,2]))
        self.assertEqual(response.status_code, 404)
    
    def test_delete_valid_user_module_list(self):
        # Deleting a user_module with user_id 1 and module_id 1
        response = self.client.delete(reverse("enterprise:user_module_list", args=[1,1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_user_module_list(self):
        # Deleting a user_module with user_id 1 and module_id 1
        response = self.client.delete(reverse("enterprise:user_module_list", args=[1,1]))
        self.assertEqual(response.status_code, 200)
        # Again deleting a user_module with user_id 1 and module_id 1
        response = self.client.delete(reverse("enterprise:user_module_list", args=[1,1]))
        self.assertEqual(response.status_code, 400)
        # Deleting a user_module with user_id 2 which does not exist
        response = self.client.post(reverse("enterprise:user_module_list", args=[2,1]))
        self.assertEqual(response.status_code, 404)
        # Deleting a user_module with module_id 2 which does not exist
        response = self.client.post(reverse("enterprise:user_module_list", args=[1,2]))
        self.assertEqual(response.status_code, 404)