from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class EnterpriseModelViewTest(TestCase):
    def setUp(self):
        '''
        Making a clear database with Enterprise ID 1
        '''
        Enterprise.objects.create(enterprise_name="ENT 1")
    
    def test_get_valid_enterprise(self):
        '''
        Getting Enterprise with ID 1, a valid response
        '''
        response = self.client.get(reverse("enterprise:enterprise", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("enterprise_name"), "ENT 1")
    
    def test_get_invalid_enterprise(self):
        '''
        Getting Enterprise with ID 2, which is not existing
        '''
        response = self.client.get(reverse("enterprise:enterprise", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_enterprise(self):
        '''
        Posting a new Enterprise
        '''
        response = self.client.post(reverse("enterprise:enterprise_list"), {"enterprise_name": "ENT 2"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["enterprise_name"], "ENT 2")
    
    def test_post_invalid_enterprise(self):
        '''
        Posting an enterprise with a pre-existing enterprise name, 
        violating unique enterprise name
        '''
        response = self.client.post(reverse("enterprise:enterprise_list"), {"enterprise_name": "ENT 1"})
        self.assertEqual(response.status_code, 400)

    def test_patch_valid_enterprise(self):
        '''
        Patching Enterprise ID 1 with a new name
        '''
        data = {"enterprise_name": "ENT 2"}
        data = json.dumps(data)
        response = self.client.patch(reverse("enterprise:enterprise", args=[1]), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["enterprise_name"], "ENT 2")

    def test_patch_invalid_enterprise(self):
        '''
        Patching the enterprise ID 1 with a pre-existing enterprise name "ENT 2", 
        violating unique enterprise name
        '''
        Enterprise.objects.create(enterprise_name="ENT 2")
        data = {"enterprise_name": "ENT 2"}
        data = json.dumps(data)
        response = self.client.patch(reverse("enterprise:enterprise", args=[1]), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_delete_valid_enterprise(self):
        '''
        Deleting an enterprise with ID 1
        '''
        response = self.client.delete(reverse("enterprise:enterprise", args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_enterprise(self):
        # Deleting an enterprise with ID 1
        response = self.client.delete(reverse("enterprise:enterprise", args=[1]))
        self.assertEqual(response.status_code, 200)
        # Again Deleting the enterprise with ID 1
        response = self.client.delete(reverse("enterprise:enterprise", args=[1]))
        self.assertEqual(response.status_code, 400)
        # Deleting an enterprise with ID 2 which does not exist
        response = self.client.delete(reverse("enterprise:enterprise", args=[2]))
        self.assertEqual(response.status_code, 404)