from django.test import TestCase
from django.urls import reverse
import json 
from unittest.mock import patch
import requests

from enterprise.models import *
from enterprise.serializers import *
from event.models import *
from event.serializers import *


class DraftEventItemModelViewTest(TestCase):
    def setUp(self):

        # Populating db with necessary entries
        # Entering a measurement unit
        data = {
            "measurement_unit_primary_name" : "meter",
            "measurement_unit_category" : "length",
            "measurement_unit_value_type" : "Dec"
        }
        MeasurementUnit.objects.create(**data)
        self.measurement_unit = MeasurementUnit.objects.get(measurement_unit_id=1)
        # Entering a currency code
        data = {
            "currency_code": "USD"
        }
        CurrencyCode.objects.create(**data)
        self.currency_code = CurrencyCode.objects.get(currency_code="USD")
        # Entering a draft event and the related foreign objects
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
           "enterprise_id": self.enterprise, 
           "event_name": "Buy", 
           "event_type": "RFQ", 
           "buyer_billing_address_id": self.address1, 
           "buyer_shipping_address_id": self.address2, 
           "event_delivery_datetime": "2021-05-17T09:49:43.583737Z", 
           "payment_terms_code": "USD", 
           "created_by_user_id": self.user, 
           "created_by_name": "Pratyush", 
           "created_by_phone": "xxxxxx991", 
           "created_by_email": "jaiswalprat@gmail.com", 
           "status": "Draft", 
           "last_modified_by_user_id": self.user
        }
        DraftEvent.objects.create(**data)
        self.draft_event = DraftEvent.objects.get(event_id=1)
        data = {
            "item_name": "IPhone",
            "item_description": "An Apple Product"
        }
        Item.objects.create(**data)
        self.item = Item.objects.get(item_id=1)
        data = {
            "event_id": self.draft_event,
            "item_id": self.item,
            "buyer_item_id": "200012 Iphone - Black",
            "description": "Just an exp",
            "measurement_unit_id": self.measurement_unit, 
            "meausrement_unit": "meters", 
            "desired_quantity": 100, 
            "currency_code": self.currency_code, 
            "desired_price": 950, 
            "opening_bid": 950, 
            "total_amount": 100000
        }
        DraftEventItem.objects.create(**data)
        self.draft_event_item = DraftEventItem.objects.get(event_line_item_id=1)
        data = {
            "attribute_name": "Color",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**data)
        self.attribute1 = Attribute.objects.get(attribute_id=1)
        data = {
            "event_line_item_id": self.draft_event_item,
            "attribute_id": self.attribute1,
            "attribute_value": "BLUE"
        }
        DraftEventItemAttribute.objects.create(**data)
    
    def test_get_valid_draft_event_item_info(self):
        # Getting item_info of item with event_line_item_id 1
        response = self.client.get(reverse("event:draft_event_item_info", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["event_line_item_id"], 1)
        self.assertEqual(response.data["buyer_item_id"], "200012 Iphone - Black")
        # Entering a new item
        data = {
            "event_id": self.draft_event,
            "item_id": self.item
        }
        DraftEventItem.objects.create(**data)
        # Getting item_info of item with event_line_item_id 2
        response = self.client.get(reverse("event:draft_event_item_info", args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["event_line_item_id"], 2)
    
    def test_get_valid_draft_event_item_attribute(self):
        # getting item_attribute of item with event_line_item_id 1
        response = self.client.get(reverse("event:draft_event_item_attribute", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["event_line_item_id"], 1)
        self.assertEqual(response.data[0]["attribute_id"], 1)
        self.assertEqual(response.data[0]["attribute_value"], "BLUE")
        # Entering item_attribute for item with ID 1
        data = {
            "attribute_name": "RAM",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**data)
        attribute = Attribute.objects.get(attribute_id=2)
        data = {
            "event_line_item_id": self.draft_event_item,
            "attribute_id": attribute,
            "attribute_value": "4GB"
        }
        DraftEventItemAttribute.objects.create(**data)
        # Getting new item_attribute list of event_line_item_id 1 with 2 attributes
        response = self.client.get(reverse("event:draft_event_item_attribute", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["event_line_item_id"], 1)
        self.assertEqual(response.data[0]["attribute_id"], 1)
        self.assertEqual(response.data[0]["attribute_value"], "BLUE")
        self.assertEqual(response.data[1]["event_line_item_id"], 1)
        self.assertEqual(response.data[1]["attribute_id"], 2)
        self.assertEqual(response.data[1]["attribute_value"], "4GB")
    
    def get_valid_draft_event_item(self):
        # Getting item_info and item_attribute for event_line_item_id 1
        response = self.client.get(reverse("event:draft_event_item", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("item_info", None))
        self.assertIsNotNone(response.data.get("item_attribute", None))
        self.assertEqual(response.data["item_info"]["event_line_item_id"], 1)
        self.assertEqual(response.data["item_info"]["item_id"], 1)
        self.assertEqual(len(response.data["item_attribute"]), 1)
        self.assertEqual(response.data["item_attribute"][0]["attribute_id"], 1)
        self.assertEqual(response.data["item_attribute"][0]["attribute_value"], "BLUE")

    def test_get_valid_draft_event_item_list(self):
        # Getting item_list with draft_event_id 1
        response = self.client.get(reverse("event:draft_event_item_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["event_line_item_id"], 1)
        self.assertEqual(response.data[0]["buyer_item_id"], "200012 Iphone - Black")
        # Entering a new item for draft event with ID 1
        data = {
            "event_id": self.draft_event,
            "item_id": self.item
        }
        DraftEventItem.objects.create(**data)
        # Getting new item list of draft event with id 1
        response = self.client.get(reverse("event:draft_event_item_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1]["event_line_item_id"], 2)
    
    def test_get_invalid_draft_event_item_info(self):
        # Getting item_info with event_line_item_id 2 which does not exist
        response = self.client.get(reverse("event:draft_event_item_info", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_invalid_draft_event_item_attribute(self):
        # Getting item_attribute with event_line_item_id 2 which does not exist
        response = self.client.get(reverse("event:draft_event_item_attribute", args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_get_invalid_draft_event_item(self):
        # Getting item with event_line_item_id 2 which does not exist
        response = self.client.get(reverse("event:draft_event_item", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_invalid_draft_event_item_list(self):
        # Getting item_list of draft event with id 2 which does not exist
        response = self.client.get(reverse("event:draft_event_item_list", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    @patch.object(requests, "post")
    def test_post_valid_draft_event_item(self, mock_post):
        # Posting item_info and item_attributes
        data = {
            "item_info":{
                "item_id": 1,
                "description": "Item poslished",
                "buyer_item_id": "20001"
            },
            "item_attribute":[
                {
                    "attribute_id": 1,
                    "attribute_value": "RED"
                }
            ]
        }
        # This data is being mocked for the post request being made to 
        # the draft_event_item_attribute
        attribute_data_being_mocked = [
            {
                "event_line_item_id": 2,
                "attribute_id": 1,
                "attribute_value": "RED"
            }
        ]
        mock_post.return_value.status_code = 201
        mock_post.return_value.text = attribute_data_being_mocked
        response = self.client.post(reverse("event:draft_event_item_list", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["item_info"]["event_line_item_id"], 2)
        self.assertEqual(response.data["item_info"]["description"], "Item poslished")
        self.assertEqual(response.data["item_attribute"][0]["event_line_item_id"], 2)
        self.assertEqual(response.data["item_attribute"][0]["attribute_id"], 1)
        self.assertEqual(response.data["item_attribute"][0]["attribute_value"], "RED")
        # posting only item_info
        data = {
            "item_info":{
                "item_id": 1,
                "description": "Item poslished and crafted",
                "desired_quantity": 100,
                "buyer_item_id": "20001"
            }
        }
        response = self.client.post(reverse("event:draft_event_item_list", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["item_info"]["event_line_item_id"], 3)
        self.assertEqual(response.data["item_info"]["description"], "Item poslished and crafted")
        # float() used because the desired_quantity is a decimal field
        self.assertEqual(float(response.data["item_info"]["desired_quantity"]), float(100))
    
    def test_post_valid_draft_event_item_attribute(self):
        # Creating a new item with event_line_item_id 2
        data = {
            "event_id": self.draft_event,
            "item_id": self.item
        }
        DraftEventItem.objects.create(**data)
        data = [{
            "attribute_id": 1,
            "attribute_value": "RED"
        }]
        # Posting item_attribute with event_line_item_id 2
        response = self.client.post(reverse("event:draft_event_item_attribute", args=[2]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["event_line_item_id"], 2)
        self.assertEqual(response.data[0]["attribute_id"], 1)
        self.assertEqual(response.data[0]["attribute_value"], "RED")

    @patch.object(requests, "post")
    def test_post_invalid_draft_item(self, mock_post):
        # Posting item_info without item_id (invalid)
        data = {
            "item_info":{
                "description": "Item poslished"
            },
            "item_attribute":[
                {
                    "attribute_id": 1,
                    "attribute_value": "RED"
                }
            ]
        }
        response = self.client.post(reverse("event:draft_event_item_list", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # Posting item_info with item_id 2 which does not exist
        data = {
            "item_info":{
                "item_id": 2,
                "description": "Item poslished"
            },
            "item_attribute":[
                {
                    "attribute_id": 1,
                    "attribute_value": "RED"
                }
            ]
        }
        response = self.client.post(reverse("event:draft_event_item_list", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # Posting item_info with event_id 2 which does not exist
        data = {
            "item_info":{
                "item_id": 1,
                "description": "Item poslished"
            },
            "item_attribute":[
                {
                    "attribute_id": 1,
                    "attribute_value": "RED"
                }
            ]
        }
        response = self.client.post(reverse("event:draft_event_item_list", args=[2]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)
    
    def test_post_invalid_draft_event_item_attribute(self):
        # Creating a fresh new item
        data = {
            "event_id": self.draft_event,
            "item_id": self.item
        }
        DraftEventItem.objects.create(**data)
        # Posting an attribute with id 2 which does not exist
        data = [{
            "attribute_id": 2,
            "attribute_value": "RED"
        }]
        response = self.client.post(reverse("event:draft_event_item_attribute", args=[2]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # Posting an attribute without attribute id
        data = [{
            "attribute_value": "RED"
        }]
        response = self.client.post(reverse("event:draft_event_item_attribute", args=[2]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
    
    def test_patch_valid_draft_event_item_info(self):
        # Patching event_item_info with event_line_item_id 1
        data = {
            "desired_quantity": 95
        }
        response = self.client.patch(reverse("event:draft_event_item_info", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["event_line_item_id"], 1)
        # float() is used because desired_quantity is a decimalfield
        self.assertEqual(float(response.data["desired_quantity"]), float(95))
        # with a new foreignkey
        data = {
            "currency_code": "INR"
        }
        CurrencyCode.objects.create(**data)
        response = self.client.patch(reverse("event:draft_event_item_info", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["event_line_item_id"], 1)
        self.assertEqual(response.data["currency_code"], "INR")

    def test_patch_valid_draft_event_item_attribute(self):
        # Patching with item_attribute of event_line_itme_id 1 with new attribute value
        data = [{
            "attribute_id": 1,
            "attribute_value": "RED"
        }]
        response = self.client.patch(reverse("event:draft_event_item_attribute", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data[0]["event_line_item_id"], 1)
        self.assertEqual(response.data[0]["attribute_id"], 1)
        self.assertEqual(response.data[0]["attribute_value"], "RED")
    
    def test_patch_invalid_event_item_info(self):
        # Patching event_item_info with event_line_item_id 1 with some invalid foreignkeys which don't exist
        data = {
            "currency_code": "INR"
        }
        response = self.client.patch(reverse("event:draft_event_item_info", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # Patching event_item_info with event_line_item_id 1 with some invalid foreignkeys which don't exist
        data = {
            "item_id": 2
        }
        response = self.client.patch(reverse("event:draft_event_item_info", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # Patching event_item_info with event_line_item_id 2 whcih does not exist
        data = {
            "currency_code": "USD"
        }
        response = self.client.patch(reverse("event:draft_event_item_info", args=[2]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_patch_invalid_draft_event_item_attribute(self):
        # Patching with item_attribute of event_line_itme_id 1 with attribute id 2 which does not exist
        data = [{
            "attribute_id": 2,
            "attribute_value": "RED"
        }]
        response = self.client.patch(reverse("event:draft_event_item_attribute", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # Patching event_item_attribute with event_line_item_id 2 whcih does not exist
        data = [{
            "attribute_id": 1,
            "attribute_value": "RED"
        }]
        response = self.client.patch(reverse("event:draft_event_item_attribute", args=[2]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)
    
    def test_valid_delete_draft_event_item(self):
        # Deleting event_item with event_line_item 1
        response = self.client.delete(reverse("event:draft_event_item", args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_delete_draft_event_item(self):
        # Deleting event_item with event_line_item 1
        response = self.client.delete(reverse("event:draft_event_item", args=[1]))
        self.assertEqual(response.status_code, 200)
        # Again deleting event_item with event_line_item 1
        response = self.client.delete(reverse("event:draft_event_item", args=[1]))
        self.assertEqual(response.status_code, 404)
        # Deleting event_item with event_line_item 2 which does not exist
        response = self.client.delete(reverse("event:draft_event_item", args=[2]))
        self.assertEqual(response.status_code, 404)