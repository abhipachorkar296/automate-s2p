from django.test import TestCase
from django.urls import reverse
import json
from django.utils import timezone
from unittest.mock import patch
import requests

from enterprise.models import *
from enterprise.serializers import *
from event.models import *
from event.serializers import *

class DraftAwardModelViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db
        '''
        Enterprise.objects.create(enterprise_name="ENT 1")
        self.enterprise = Enterprise.objects.get(enterprise_id=1)
        entity_data1 = {
            "enterprise_id": self.enterprise,
            "entity_type": "IT",
            "entity_name": "Apple",
            "entity_primary_address": "xyz",
            "entity_primary_email": "apple@gmail.com"
        }
        Entity.objects.create(**entity_data1)
        self.entity1 = Entity.objects.get(entity_id=1)
        buyer_data = {
            "buyer_id" : self.entity1
        }
        Buyer.objects.create(**buyer_data)
        self.buyer = Buyer.objects.get(buyer_id=1)
        user_data = {
            "enterprise_id": self.enterprise,
            "user_email": "apple1@gmail.com",
            "user_firstname": "Pratyush",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**user_data)
        self.user1 = User.objects.get(user_id=1)
        user_data = {
            "enterprise_id": self.enterprise,
            "user_email": "apple2@gmail.com",
            "user_firstname": "Abhishek",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**user_data)
        self.user2 = User.objects.get(user_id=2)
        address_data1 = {
            "address_nickname": "Berkeley Office",
            "country": "USA",
            "address1": "215 Dwight Way, Berkeley, CA 97074",
            "city" : "berkeley",
            "postal_code" : 97074
        }
        Address.objects.create(**address_data1)
        self.address1 = Address.objects.get(address_id=1)
        address_data2 = {
            "address_nickname": "New York Headquarters",
            "country": "USA",
            "address1": "156 Street Way, New York, NY 67809",
            "city" : "New York",
            "postal_code" : 67809
        }
        Address.objects.create(**address_data2)
        self.address2 = Address.objects.get(address_id=2)
        event_data = {
           "enterprise_id": self.enterprise, 
           "buyer_id" : self.buyer,
           "event_name": "Buy", 
           "event_type": "RFQ", 
           "event_start_datetime": "2021-05-17T09:49:43.583737Z", 
           "event_end_datetime": "2021-05-17T09:49:43.583737Z", 
           "buyer_billing_address_id": self.address1, 
           "buyer_shipping_address_id": self.address2, 
           "event_delivery_datetime": "2021-05-17T09:49:43.583737Z", 
           "payment_terms_code": "USD", 
           "created_by_user_id": self.user1, 
           "created_by_name": "Pratyush", 
           "created_by_phone": "xxxxxx991", 
           "created_by_email": "jaiswalprat@gmail.com", 
           "status": "Ongoing", 
           "last_modified_by_user_id": self.user1
        }
        Event.objects.create(**event_data)
        self.event = Event.objects.get(event_id=1)
        Enterprise.objects.create(enterprise_name="ENT 2")
        self.enterprise2 = Enterprise.objects.get(enterprise_id=2)
        entity_data2 = {
            "enterprise_id": self.enterprise2,
            "entity_type": "IT1",
            "entity_name": "Apple1",
            "entity_primary_address": "xyz1",
            "entity_primary_email": "apple1@gmail.com"
        }
        Entity.objects.create(**entity_data2)
        self.entity2 = Entity.objects.get(entity_id=2)
        seller_data1 = {
            "seller_id" : self.entity2
        }
        Seller.objects.create(**seller_data1)
        self.seller1 = Seller.objects.get(seller_id=2)
        Enterprise.objects.create(enterprise_name="ENT 3")
        self.enterprise3 = Enterprise.objects.get(enterprise_id=3)
        entity_data3 = {
            "enterprise_id": self.enterprise3,
            "entity_type": "IT2",
            "entity_name": "Apple2",
            "entity_primary_address": "xyz2",
            "entity_primary_email": "apple2@gmail.com"
        }
        Entity.objects.create(**entity_data3)
        self.entity3 = Entity.objects.get(entity_id=3)
        seller_data2 = {
            "seller_id" : self.entity3
        }
        Seller.objects.create(**seller_data2)
        self.seller2 = Seller.objects.get(seller_id=3)
        measurement_unit_data = {
            "measurement_unit_primary_name" : "meter",
            "measurement_unit_category" : "length",
            "measurement_unit_value_type" : "Dec"
        }
        MeasurementUnit.objects.create(**measurement_unit_data)
        self.measurement_unit_id = MeasurementUnit.objects.get(measurement_unit_id=1)
        CurrencyCode.objects.create(currency_code="USD")
        self.currency_code = CurrencyCode.objects.get(currency_code="USD")
        item_data = {
            "item_name": "IPhone",
            "item_description": "An Apple Product"
        }
        Item.objects.create(**item_data)
        self.item = Item.objects.get(item_id=1)
        event_item_data = {
            "currency_code": self.currency_code,
            "item_id": self.item, 
            "event_id" : self.event,
            "buyer_item_id": "200012 Iphone - Black", 
            "description": "Just an exp", 
            "measurement_unit_id": self.measurement_unit_id, 
            "meausrement_unit": "meters", 
            "desired_quantity": 100, 
            "desired_price": 950, 
            "opening_bid": 950, 
            "total_amount": 100000
        }
        EventItem.objects.create(**event_item_data)
        self.event_item = EventItem.objects.get(event_line_item_id=1)
        attribute_data = {
            "attribute_name": "Density",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**attribute_data)
        self.attribute = Attribute.objects.get(attribute_id=1)
        event_item_attribute_data = {
            "event_line_item_id" : self.event_item,
            "attribute_id" : self.attribute,
            "attribute_value" : "16"
        }
        EventItemAttribute.objects.create(**event_item_attribute_data)
        data = [
            {
                "event_line_item_id" : self.event_item,
                "event_id" : self.event,
                "seller_id" : self.seller1,
                "buyer_approval_required" : True,
                "approved_by_buyer" : True
            },
            {
                "event_line_item_id" : self.event_item,
                "event_id" : self.event,
                "seller_id" : self.seller2,
                "buyer_approval_required" : True,
                "approved_by_buyer" : True
            }
        ]
        EventItemSeller.objects.bulk_create(EventItemSeller(**x) for x in data)
        draft_award_info_data = {
            "event_id": self.event, 
            "creator_user_id": self.user1,
            "approver_user_id": self.user2, 
            "draft_purchase_order_id": 0, 
            "purchase_order_id": 0,
            "buyer_id": self.buyer, 
            "seller_id": self.seller1, 
            "seller_bid_id": "1234",
            "award_creation_datetime": "2021-06-01T06:08:20.014493Z", 
            "payment_terms_code": "USD", 
            "currency_code": self.currency_code, 
            "subtotal": 500, 
            "taxes": 100, 
            "total_shipping_cost": 0, 
            "total_other_charges": 0,
            "bulk_discount_percentage": 5, 
            "bulk_discount_amount": 30, 
            "total": 570, 
            "deal_status": "Deal Awarded"
        }
        DraftAward.objects.create(**draft_award_info_data)
        self.draft_award1 = DraftAward.objects.get(award_id=1)
        draft_award_item_info = { 
            "event_line_item_id": self.event_item,
            "award_id": self.draft_award1,
            "measurement_unit_id": self.measurement_unit_id, 
            "quantity_offered": 500, 
            "quantity_awarded": 100, 
            "currency_code": self.currency_code, 
            "price": 900, 
            "other_charges": 0, 
            "shipping_managed_by": "B", 
            "shipping_cost": 0, 
            "total_amount": 90000
        }
        DraftAwardItem.objects.create(**draft_award_item_info)
        self.draft_award_item1 = DraftAwardItem.objects.get(award_line_item_id=1)
        draft_award_item_tax1 = {
            "award_line_item_id": self.draft_award_item1,
            "tax_name": "GST",
            "value": 5
        }
        DraftAwardItemTax.objects.create(**draft_award_item_tax1)
        draft_award_item_tax2 = {
            "award_line_item_id": self.draft_award_item1,
            "tax_name": "CGST",
            "value": 5
        }
        DraftAwardItemTax.objects.create(**draft_award_item_tax2)
        
    def test_get_valid_draft_award_list(self):
        # Getting award_list with event id 1
        response = self.client.get(reverse("event:draft_award_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        award_info_1 = response.data[0]["award_info"]
        award_item_list_1 = response.data[0]["award_item_list"]
        self.assertEqual(award_info_1["award_id"], 1)
        self.assertIsNone(award_info_1["deleted_datetime"])
        self.assertEqual(len(award_item_list_1), 1)
        self.assertEqual(award_item_list_1[0]["item_info"]["award_line_item_id"], 1)
        self.assertEqual(award_item_list_1[0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_item_list_1[0]["item_tax"]), 2)
        self.assertEqual(award_item_list_1[0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_item_list_1[0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_item_list_1[0]["item_tax"][1]["tax_name"], "CGST")
        self.assertEqual(float(award_item_list_1[0]["item_tax"][1]["value"]), float(5))

        # Creating a new draft award within the event id 1
        draft_award_info_data = {
            "event_id": self.event, 
            "creator_user_id": self.user1,
            "approver_user_id": self.user2, 
            "draft_purchase_order_id": 0, 
            "purchase_order_id": 0,
            "buyer_id": self.buyer, 
            "seller_id": self.seller2,  
            "deal_status": "Deal Awarded"
        }
        DraftAward.objects.create(**draft_award_info_data)
        draft_award2 = DraftAward.objects.get(award_id=2)
        draft_award_item_info = { 
            "event_line_item_id": self.event_item,
            "award_id": draft_award2,
            "measurement_unit_id": self.measurement_unit_id, 
            "quantity_offered": 500, 
            "quantity_awarded": 100,  
            "shipping_cost": 0, 
            "total_amount": 90000
        }
        DraftAwardItem.objects.create(**draft_award_item_info)
        draft_award_item2 = DraftAwardItem.objects.get(award_line_item_id=2)
        award_item_tax1 = {
            "award_line_item_id": draft_award_item2,
            "tax_name": "GST",
            "value": 5
        }
        DraftAwardItemTax.objects.create(**award_item_tax1)
        draft_award_item_tax2 = {
            "award_line_item_id": draft_award_item2,
            "tax_name": "CGST",
        }
        DraftAwardItemTax.objects.create(**draft_award_item_tax2)

        # Getting draft_award_list with event id 1
        response = self.client.get(reverse("event:draft_award_list", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        response.data.sort(key=lambda x: x["award_info"]["award_id"])
        award_info_1 = response.data[0]["award_info"]
        award_item_list_1 = response.data[0]["award_item_list"]
        self.assertEqual(award_info_1["award_id"], 1)
        self.assertIsNone(award_info_1["deleted_datetime"])
        self.assertEqual(len(award_item_list_1), 1)
        self.assertEqual(award_item_list_1[0]["item_info"]["award_line_item_id"], 1)
        self.assertEqual(award_item_list_1[0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_item_list_1[0]["item_tax"]), 2)
        self.assertEqual(award_item_list_1[0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_item_list_1[0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_item_list_1[0]["item_tax"][1]["tax_name"], "CGST")
        self.assertEqual(float(award_item_list_1[0]["item_tax"][1]["value"]), float(5))

        award_info_2 = response.data[1]["award_info"]
        award_item_list_2 = response.data[1]["award_item_list"]
        self.assertEqual(award_info_2["award_id"], 2)
        self.assertIsNone(award_info_2["deleted_datetime"])
        self.assertEqual(len(award_item_list_2), 1)
        self.assertEqual(award_item_list_2[0]["item_info"]["award_line_item_id"], 2)
        self.assertEqual(award_item_list_2[0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_item_list_2[0]["item_tax"]), 2)
        self.assertEqual(award_item_list_2[0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_item_list_2[0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_item_list_2[0]["item_tax"][1]["tax_name"], "CGST")
    
    def test_get_invalid_draft_award_list(self):
        # Getting draft award list with event id 2 which does not exist
        response = self.client.get(reverse("event:draft_award_list", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_post_valid_draft_award_list(self):
        data = [
            {
                "award_info": {
                    "event_id": 1, 
                    "creator_user_id": 1,
                    "approver_user_id": 2, 
                    "draft_purchase_order_id": 0, 
                    "purchase_order_id": 0,
                    "buyer_id": 1, 
                    "seller_id": 3, 
                },
                "award_item_list": [
                    {
                        "item_info": { 
                            "event_line_item_id": 1, 
                            "measurement_unit_id": 1, 
                            "quantity_offered": 500, 
                            "quantity_awarded": 100
                        },
                        "item_tax": [
                            {
                                "tax_name": "GST",
                                "value": 5
                            },
                            {
                                "tax_name": "CGST",
                            }
                        ]
                    }
                ]
            }
        ]
        response = self.client.post(reverse("event:draft_award_list", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 1)
        award_object1 = response.data[0]
        self.assertEqual(award_object1["award_info"]["award_id"], 2)
        self.assertEqual(award_object1["award_info"]["event_id"], 1)
        self.assertEqual(len(award_object1['award_item_list']), 1)
        self.assertEqual(award_object1['award_item_list'][0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_object1['award_item_list'][0]["item_tax"]), 2)
        self.assertEqual(award_object1['award_item_list'][0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_object1['award_item_list'][0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_object1['award_item_list'][0]["item_tax"][1]["tax_name"], "CGST")
    
    def test_post_invalid_draft_award_list(self):
        # Posting award with invalid data to event 1
        data = [
            {
                "award_info": {
                    "event_id": 1, 
                    "creator_user_id": 3, # This user does not exist
                    "approver_user_id": 2, 
                    "draft_purchase_order_id": 0, 
                    "purchase_order_id": 0,
                    "buyer_id": 1, 
                    "seller_id": 3, 
                },
                "award_item_list": [
                    {
                        "item_info": { 
                            "event_line_item_id": 1, 
                            "measurement_unit_id": 1, 
                            "quantity_offered": 500, 
                            "quantity_awarded": 100
                        },
                        "item_tax": [
                            {
                                "tax_name": "GST",
                                "value": 5
                            },
                            {
                                "tax_name": "CGST",
                            }
                        ]
                    }
                ]
            }
        ]
        response = self.client.post(reverse("event:draft_award_list", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # Posting to an event id 2 which does not exist
        response = self.client.post(reverse("event:draft_award_list", args=[2]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        # Posting to an event which is deleted
        self.event.deleted_datetime = timezone.now()
        self.event.save()
        response = self.client.post(reverse("event:draft_award_list", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
    
    @patch.object(requests, "post")
    def test_post_valid_draft_award_list_shift_award(self, mock_post):
        # Shifting draft award list to award of an event with id 1
        data_to_be_mocked = [
            {
                "award_info": {
                    "event_id": 1,
                    "award_id": 1,
                    "parent_award_id": 0, 
                    "creator_user_id": 1,
                    "approver_user_id": 2, 
                    "draft_purchase_order_id": 0, 
                    "purchase_order_id": 0,
                    "buyer_id": 1, 
                    "seller_id": 3, 
                    "seller_bid_id": "1234",
                    "award_creation_datetime": "2021-06-01T06:08:20.014493Z", 
                    "payment_terms_code": "USD", 
                    "currency_code": "USD", 
                    "subtotal": 500, 
                    "taxes": 100, 
                    "total_shipping_cost": 0, 
                    "total_other_charges": 0,
                    "bulk_discount_percentage": 5, 
                    "bulk_discount_amount": 30, 
                    "total": 570, 
                    "deal_status": "Deal Awarded"
                },
                "award_item_list": [
                    {
                        "item_info": { 
                            "event_line_item_id": 1, 
                            "measurement_unit_id": 1, 
                            "quantity_offered": 500, 
                            "quantity_awarded": 100, 
                            "currency_code": "USD", 
                            "price": 900, 
                            "other_charges": 0, 
                            "shipping_managed_by": "B", 
                            "shipping_cost": 0, 
                            "total_amount": 90000
                        },
                        "item_tax": [
                            {
                                "tax_name": "GST",
                                "value": 5
                            },
                            {
                                "tax_name": "CGST",
                                "value": 5
                            }
                        ]
                    }
                ]
            }
        ]
        mock_post.return_value.status_code = 201
        mock_post.return_value.text = data_to_be_mocked
        response = self.client.post(reverse("event:draft_award_list_shift_award", args=["1"]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 1)
        award_object1 = response.data[0]
        self.assertEqual(award_object1["award_info"]["award_id"], 1)
        self.assertEqual(award_object1["award_info"]["event_id"], 1)
        self.assertEqual(award_object1["award_info"]["parent_award_id"], 0)
        self.assertEqual(len(award_object1['award_item_list']), 1)
        self.assertEqual(award_object1['award_item_list'][0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_object1['award_item_list'][0]["item_tax"]), 2)
        self.assertEqual(award_object1['award_item_list'][0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_object1['award_item_list'][0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_object1['award_item_list'][0]["item_tax"][1]["tax_name"], "CGST")
        self.assertEqual(float(award_object1['award_item_list'][0]["item_tax"][1]["value"]), float(5))
    
    @patch.object(requests, "post")
    def test_post_invalid_draft_award_list_shift_award(self, mock_post):
        # Shifting invalid draft award list to award of an event with id 1
        mock_post.return_value.status_code = 400
        response = self.client.post(reverse("event:draft_award_list_shift_award", args=["1"]))
        self.assertEqual(response.status_code, 400)

        # Shifting draft award list to award of an event with id 2 which doesn't exist
        response = self.client.post(reverse("event:draft_award_list_shift_award", args=["2"]))
        self.assertEqual(response.status_code, 404)
    
    