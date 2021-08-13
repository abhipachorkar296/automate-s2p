from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *

class CurrencyCodeModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db with Currency Code id "USD"
        '''
        CurrencyCode.objects.create(currency_code="USD")
    
    def test_get_valid_all_currency_code(self):
        '''
        Getting all currency codes
        '''
        response = self.client.get(reverse("enterprise:currency_code"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["currency_code"], "USD")
    
    def test_post_valid_currency_code(self):
        # Entering new currency code with id "INR"
        data = {
            "currency_code" : "INR"
        }
        response = self.client.post(reverse("enterprise:currency_code"),data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["currency_code"], "INR")

    def test_post_invalid_currency_code(self):
        '''
        Posting a currency_code with id "USD", which already exists
        violating unique_together constraint
        '''
        data = {
            "currency_code" : "USD"
        }
        response = self.client.post(reverse("enterprise:currency_code"),data)
        self.assertEqual(response.status_code, 400)
    
    def test_delete_valid_currency_code(self):
        # Deleting currency_code with ID "USD"
        response = self.client.delete(reverse("enterprise:delete_currency_code", args=["USD"]))
        self.assertEqual(response.status_code, 200)
        
    def test_delete_valid_invalid_user(self):
        # Deleting currency_code with ID "USD"
        response = self.client.delete(reverse("enterprise:delete_currency_code", args=["USD"]))
        self.assertEqual(response.status_code, 200)
        # Again deleting currency_code with ID "USD"
        response = self.client.delete(reverse("enterprise:delete_currency_code", args=["USD"]))
        self.assertEqual(response.status_code, 404)
        # Deleting currency_code with id "INR", which does not exist
        response = self.client.delete(reverse("enterprise:delete_currency_code", args=["INR"]))
        self.assertEqual(response.status_code, 404)