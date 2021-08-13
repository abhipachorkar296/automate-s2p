from django.test import TestCase
from django.urls import reverse
import json
from enterprise.models import *
from enterprise.serializers import *
class AddressModelViewTest(TestCase):
    def setUp(self):
        '''
        Making a clear database with Address
        '''
        data = {
            "address_nickname": "Berkeley Office",
            "country": "USA",
            "address1": "215 Dwight Way, Berkeley, CA 97074",
            "city" : "berkeley",
            "postal_code" : 97074
        }
        Address.objects.create(**data)
    
    def test_get_valid_address(self):
        '''
        Getting Address with ID 1, a valid response
        '''
        response = self.client.get(reverse("enterprise:get_address", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("address_nickname"), "Berkeley Office")
    
    def test_get_invalid_address(self):
        '''
        Getting Address with ID 2, which is not existing
        '''
        response = self.client.get(reverse("enterprise:get_address", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_valid_all_address(self):
        '''
        Getting all Addresss
        '''
        response = self.client.get(reverse("enterprise:address_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["address_nickname"], "Berkeley Office")
        self.assertEqual(response.data[0]["postal_code"], 97074)

    def test_post_all_valid_address(self):
        '''
        Posting a new Address
        '''
        data = [{
                "address_nickname": "New York Headquarters",
                "country": "USA",
                "address1": "156 Street Way, New York, NY 67809",
                "city" : "New York",
                "postal_code" : 67809
            }]
        response = self.client.post(reverse("enterprise:address_list"), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.data[0]["city"], "berkeley")
    
    def test_post_invalid_address(self):
        '''
        Posting an Address with invalid address 
        '''
        data = {
                "address_nickname": "New York Headquarters",
                "country": "USA",
                "address1": "156 Street Way, New York, NY 67809",
                "city" : "New ork",
                "postal_code" : "asd"
            }
        response = self.client.post(reverse("enterprise:address_list"), data)
        self.assertEqual(response.status_code, 400)
    
    def test_delete_valid_address(self):
        '''
        Deleting an address with ID 1
        '''
        response = self.client.delete(reverse("enterprise:get_address", args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_address(self):
        # Deleting an address with ID 1
        response = self.client.delete(reverse("enterprise:get_address", args=[1]))
        self.assertEqual(response.status_code, 200)
        # Again Deleting the address with ID 1
        response = self.client.delete(reverse("enterprise:get_address", args=[1]))
        self.assertEqual(response.status_code, 400)
        # Deleting an address with ID 2 which does not exist
        response = self.client.delete(reverse("enterprise:get_address", args=[2]))
        self.assertEqual(response.status_code, 404)
