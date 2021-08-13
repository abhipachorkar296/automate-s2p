
from django.test import TestCase
from django.urls import reverse
import json
from enterprise.models import *
from enterprise.serializers import *
from event.models import *
from event.serializers import *

class DraftEventModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating db with necessary data
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
        self.user = User.objects.get(user_id=1)
        data = {
            "address_nickname": "Berkeley Office",
            "country": "USA",
            "address1": "215 Dwight Way, Berkeley, CA 97074",
            "city" : "berkeley",
            "postal_code" : 97074
        }
        Address.objects.create(**data)
        self.address1 = Address.objects.get(address_id=1)
        data = {
            "address_nickname": "New York Headquarters",
            "country": "USA",
            "address1": "156 Street Way, New York, NY 67809",
            "city" : "New York",
            "postal_code" : 67809
        }
        Address.objects.create(**data)
        self.address2 = Address.objects.get(address_id=2)
        data = {
           'enterprise_id': self.enterprise, 
           'event_name': "Buy", 
           'event_type': "RFQ", 
           'buyer_billing_address_id': self.address1, 
           'buyer_shipping_address_id': self.address2, 
           'event_delivery_datetime': "2021-05-17T09:49:43.583737Z", 
           'payment_terms_code': "USD", 
           'created_by_user_id': self.user, 
           'created_by_name': "Pratyush", 
           'created_by_phone': "xxxxxx991", 
           'created_by_email': "jaiswalprat@gmail.com", 
           'status': "Draft", 
           'last_modified_by_user_id': self.user
        }
        DraftEvent.objects.create(**data)
        # url for draft event with id 1
        self.url = reverse("event:get_draft_event", args=[1])
    
    def test_get_valid_draft_event(self):
        # Getting Draft Event with ID 1
        response = self.client.get(self.url)
        self.assertEqual(response.data["event_id"], 1)
        self.assertEqual(response.data["event_name"], "Buy")
        self.assertEqual(response.data["status"], "Draft")
    
    def test_get_invalid_event(self):
        # Getting draft event with id 2 which does not exist
        response = self.client.get(reverse("event:get_draft_event", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_event_list(self):
        # Getting all draft event list
        response = self.client.get(reverse("event:draft_event"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["event_id"], 1)
        self.assertEqual(response.data[0]["event_type"], "RFQ")
    
    def test_post_valid_event(self):
        # Posting a valid event
        data = {
           'enterprise_id': 1, 
           'event_name': "Buy", 
           'event_type': "RFQ", 
           'payment_terms_code': "USD", 
           'created_by_user_id': 1,  
           'status': "Draft", 
           'last_modified_by_user_id': 1
        }
        response = self.client.post(reverse("event:draft_event"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["event_id"], 2)
        self.assertEqual(response.data["event_name"], "Buy")
        self.assertEqual(response.data["created_by_user_id"], 1)
    
    def test_post_invalid_event(self):
        # Posting an invalid event
        data = {
           'enterprise_id': 3, 
           'event_name': "Buy", 
           'event_type': "RFQ", 
           'payment_terms_code': "USD", 
           'created_by_user_id': 1,  
           'status': "Draft", 
           'last_modified_by_user_id': 1 
        }
        response = self.client.post(reverse("event:draft_event"), data)
        self.assertEqual(response.status_code, 400)
        data = {}
        response = self.client.post(reverse("event:draft_event"), data)
        self.assertEqual(response.status_code, 400)
    
    def test_patch_valid_event(self):
        # Patching draft event with id 1
        data = {
            "event_start_datetime": "2021-05-17T09:49:43.583737Z", 
            "event_end_datetime": "2021-05-17T09:49:43.583737Z"
        }
        response = self.client.patch(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["event_id"], 1)
        self.assertEqual(response.data["event_start_datetime"], "2021-05-17T09:49:43.583737Z"),
        self.assertEqual(response.data["event_end_datetime"], "2021-05-17T09:49:43.583737Z"),
    def test_patch_invalid_event(self):
        # Patching draft event with id 1 with user_id 2 which does not exist
        data = {
            "created_by_user_id": 2
        }
        response = self.client.patch(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # Patching draft event with id 2 which does not exist
        data = {
            "created_by_user_id": 2
        }
        response = self.client.patch(reverse("event:get_draft_event", args=[2]), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_valid_event(self):
        # Deleting event with id 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
    def test_delete_invalid_event(self):
        # Deleting event with id 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        # Again deleting event with id 1
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 404)
        # Deleting event with id 2 which does not exist
        response = self.client.delete(reverse("event:get_draft_event", args=[2]))
        self.assertEqual(response.status_code, 404)