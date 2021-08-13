from django.test import TestCase
from django.urls import reverse
import json
from unittest.mock import patch
from event.models import *
from event.serializers import *
import requests

class SellerBidHistoryViewTest(TestCase):
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
        self.user = User.objects.get(user_id=1)
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
           "created_by_user_id": self.user, 
           "created_by_name": "Pratyush", 
           "created_by_phone": "xxxxxx991", 
           "created_by_email": "jaiswalprat@gmail.com", 
           "status": "Ongoing", 
           "last_modified_by_user_id": self.user
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
        self.entity2 = Entity.objects.get(entity_id=3)
        seller_data2 = {
            "seller_id" : self.entity2
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
        bid_info_data = {
            "event_id" : self.event,
            "bid_creator_user_id" : self.user, 
            "bid_creator_entity_type" : "S", 
            "buyer_id" : self.buyer,
            "seller_id" : self.seller1,
            "seller_bid_id" : "12345",
            "bid_creation_datetime" : "2021-08-02T06:03:08.583002Z",
            "bid_valid_till_datetime" : "2021-08-04T06:03:08.583002Z",
            "payment_terms_code" : "xyz",
            "seller_comments": "not good",
            "rebid_request_comments" : "new",
            "currency_code" : self.currency_code,
            "subtotal" : 100,
            "taxes" : 12,
            "total_shipping_cost" :14,
            "total_other_charges" : 16,
            "bulk_discount_percentage" : 1,
            "bulk_discount_amount" :1,
            "total" : 200,
            "status" : "Response submitted"
        }
        Bid.objects.create(**bid_info_data)
        self.bid = Bid.objects.get(bid_id=1)
        bid_item_data = {
            "bid_id" : self.bid,
            "event_line_item_id" : self.event_item,
            "measurement_unit_id" : self.measurement_unit_id,
            "quantity_offered" : 100.00,
            "quantity_awarded" : 100.00, 
            "currency_code" : self.currency_code,
            "price" : 0.01,
            "other_charges" : 50, 
            "shipping_managed_by" : "S",
            "shipping_cost" : 1,
            "total_amount" : 1,
            "seller_comments" : "ll" 
        }
        BidItem.objects.create(**bid_item_data)
        self.bid_item = BidItem.objects.get(bid_line_item_id=1)
        bid_item_tax_data = {
            "bid_line_item_id" : self.bid_item,
            "tax_name" : "ll",
            "value" : 1
        }
        BidItemTax.objects.create(**bid_item_tax_data)
        

    def test_get_valid_seller_bid_history(self):
        '''
        Getting bid with event id 1 and seller id 2
        '''
        response = self.client.get(reverse("event:seller_bid_history" , args=[1,2]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["bid_info"]["bid_id"], 1)
        self.assertEqual(response.data[0]["bid_item_list"][0]["item_info"]["bid_line_item_id"], 1)
        self.assertEqual(response.data[0]["bid_item_list"][0]["item_tax"][0]["tax_name"], "ll")


    def test_get_invalid_seller_bid_history(self):
        '''
        Getting bid with event id 1 and seller id 3, which does not exist
        '''
        response = self.client.get(reverse("event:seller_bid_history" , args=[1,3]))
        self.assertEqual(response.status_code, 404)
        '''
        Getting bid with event id 2 and seller id 2, which does not exist
        '''
        response = self.client.get(reverse("event:seller_bid_history" , args=[2,2]))
        self.assertEqual(response.status_code, 404)