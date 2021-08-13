from django.http import request
from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class UserModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating Test DB with enterprise ID 1 and user ID 1
        '''
        Enterprise.objects.create(enterprise_name="ENT 1")
        self.enterprise = Enterprise.objects.get(enterprise_id=1)
        data = {
            "enterprise_id": self.enterprise,
            "user_email": "apple1@gmail.com",
            "user_firstname": "Pratyush",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**data)
        # url for user with id 1
        self.url = reverse("enterprise:user", args=[1])
    
    def test_get_valid_user(self):
        '''
        Getting user with ID 1
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_get_invalid_user(self):
        '''
        Getting user with ID 2, which does not exist
        '''
        response = self.client.get(reverse("enterprise:user", args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_get_valid_user_list(self):
        '''
        Getting user list with Enterprise ID 1
        '''
        response = self.client.get(reverse("enterprise:enterprise_user_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # entering a new user
        data = {
            "enterprise_id": self.enterprise,
            "user_email": "apple4@gmail.com",
            "user_firstname": "Pratyush",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**data)
        response = self.client.get(reverse("enterprise:enterprise_user_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_invalid_user_list(self):
        '''
        Getting user list with enterprise ID 2, which does not exist
        '''
        response = self.client.get(reverse("enterprise:enterprise_user_list", args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_post_valid_user(self):
        '''
        Posting a valid user
        '''
        data = {
            "user_email": "apple2@gmail.com",
            "user_firstname": "Abhishek",
            "user_lastname": "Pachorkar",
            "user_phonenumber": "xxxxxx91"
        }
        response = self.client.post(reverse("enterprise:enterprise_user_list", args=[1]), data)
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid_user(self):
        '''
        Posting a user with invalid info
        '''
        data = {
            "user_email": "apple2@gmail.com",
            "user_firstname": "",
            "user_lastname": "Pachorkar",
            "user_phonenumber": "xxxxxx91"
        }
        response = self.client.post(reverse("enterprise:enterprise_user_list", args=[1]), data)
        self.assertEqual(response.status_code, 400)
        data = {
            "user_email": "apple2@gmail.com",
            "user_firstname": "Abhishek",
            "user_lastname": "Pachorkar",
            "user_phonenumber": ""
        }
        response = self.client.post(reverse("enterprise:enterprise_user_list", args=[1]), data)
        self.assertEqual(response.status_code, 400)
        data = {
            "user_email": "apple2@gmail.com",
            "user_lastname": "Pachorkar",
            "user_phonenumber": "xxxxxx91"
        }
        response = self.client.post(reverse("enterprise:enterprise_user_list", args=[1]), data)
        self.assertEqual(response.status_code, 400)
        # Posting user with enterpirse id 2 which does not exist
        response = self.client.post(reverse("enterprise:enterprise_user_list", args=[2]), data)
        self.assertEqual(response.status_code, 404)
    
    def test_patch_valid_user(self):
        '''
        Patching/Updating user with ID 1 with user_email
        '''
        data = {
            "user_email": "apple2@gmail.com"
        }
        data = json.dumps(data)
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("user_email"), "apple2@gmail.com")
    
    def test_patch_invalid_user(self):
        '''
        Patching Entity with ID 2 
        '''
        data = {
            "user_email": "apple2@gmail.com"
        }
        data = json.dumps(data)
        response = self.client.patch(reverse("enterprise:user", args=[2]), data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        # Patching User with ID 1 with invalid data
        data = {
            "user_email": "@gmail.com"
        }
        data = json.dumps(data)
        response = self.client.patch(reverse("enterprise:user", args=[1]), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_delete_valid_user(self):
        # Deleting user with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_delete_valid_invalid_user(self):
        # Deleting user with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        # Again deleting user with ID 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 400)
        # Deleting user with id 2, which does not exist
        response = self.client.delete(reverse("enterprise:user", args=[2]))
        self.assertEqual(response.status_code, 404)