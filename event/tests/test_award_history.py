from django.test import TestCase
from django.urls import reverse
import json
from django.urls.base import resolve
from django.utils import timezone

from enterprise.models import *
from enterprise.serializers import *
from event.models import *
from event.serializers import *

class AwardHistoryModelViewTest(TestCase):
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

        # Award for seller 1
        award_info_data = {
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
        Award.objects.create(**award_info_data)
        self.award1 = Award.objects.get(award_id=1)
        award_item_info = { 
            "event_line_item_id": self.event_item,
            "award_id": self.award1,
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
        AwardItem.objects.create(**award_item_info)
        self.award_item1 = AwardItem.objects.get(award_line_item_id=1)
        award_item_tax1 = {
            "award_line_item_id": self.award_item1,
            "tax_name": "GST",
            "value": 5
        }
        AwardItemTax.objects.create(**award_item_tax1)
        award_item_tax2 = {
            "award_line_item_id": self.award_item1,
            "tax_name": "CGST",
            "value": 5
        }
        AwardItemTax.objects.create(**award_item_tax2)

        # Award for seller 2
        award_info_data = {
            "event_id": self.event, 
            "creator_user_id": self.user1,
            "approver_user_id": self.user2, 
            "draft_purchase_order_id": 0, 
            "purchase_order_id": 0,
            "buyer_id": self.buyer, 
            "seller_id": self.seller2, 
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
        Award.objects.create(**award_info_data)
        self.award2 = Award.objects.get(award_id=2)
        award_item_info = { 
            "event_line_item_id": self.event_item,
            "award_id": self.award2,
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
        AwardItem.objects.create(**award_item_info)
        self.award_item2 = AwardItem.objects.get(award_line_item_id=2)
        award_item_tax1= {
            "award_line_item_id": self.award_item2,
            "tax_name": "GST",
            "value": 5
        }
        AwardItemTax.objects.create(**award_item_tax1)
        award_item_tax2 = {
            "award_line_item_id": self.award_item2,
            "tax_name": "CGST",
            "value": 5
        }
        AwardItemTax.objects.create(**award_item_tax2)

    def test_get_valid_event_award_history(self):
        # Posting a new award version of the award 1
        data = {
            "award_info": {
                "event_id": 1, 
                "creator_user_id": 1,
                "approver_user_id": 2, 
                "draft_purchase_order_id": 0, 
                "purchase_order_id": 0,
                "buyer_id": 1, 
                "seller_id": 2, 
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
                            "value": 10
                        }
                    ]
                }
            ]
        }
        response = self.client.post(reverse("event:award_new_version", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Getting event 1 award history
        response = self.client.get(reverse("event:event_award_history", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        seller_1_data = response.data[0]
        seller_2_data = response.data[1]
        if(seller_1_data==1):
            # Swap seller_1_data and seller_2_data to reduce writing the same 
            # checks again and again for two different cases:
            # (seller_1_data=1 and seller_2_data=2) and 
            # (seller_1_data=2 and seller_2_data=1)
            seller_1_data, seller_2_data = seller_2_data, seller_1_data
        
        # Here seller_1_data will be having length 2 and seller_2_data will be having 1
        self.assertEqual(len(seller_1_data), 2)
        self.assertEqual(len(seller_2_data), 1)
        # There will be two awards for seller_1
        # Checking awards for seller_1
        award_1 = seller_1_data[0]
        award_2 = seller_1_data[1]
        # Checking latest award
        award_info = award_1["award_info"]
        award_item_list = award_1["award_item_list"]
        self.assertEqual(award_info["award_id"], 3)
        self.assertIsNone(award_info["deleted_datetime"])
        self.assertEqual(len(award_item_list), 1)
        self.assertEqual(award_item_list[0]["item_info"]["award_line_item_id"], 3)
        self.assertEqual(award_item_list[0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_item_list[0]["item_tax"]), 2)
        self.assertEqual(award_item_list[0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_item_list[0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_item_list[0]["item_tax"][1]["tax_name"], "CGST")
        self.assertEqual(float(award_item_list[0]["item_tax"][1]["value"]), float(10))
        # Checking oldest award
        award_info = award_2["award_info"]
        award_item_list = award_2["award_item_list"]
        self.assertEqual(award_info["award_id"], 1)
        self.assertIsNotNone(award_info["deleted_datetime"])
        self.assertEqual(len(award_item_list), 1)
        self.assertEqual(award_item_list[0]["item_info"]["award_line_item_id"], 1)
        self.assertEqual(award_item_list[0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_item_list[0]["item_tax"]), 2)
        self.assertEqual(award_item_list[0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_item_list[0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_item_list[0]["item_tax"][1]["tax_name"], "CGST")
        self.assertEqual(float(award_item_list[0]["item_tax"][1]["value"]), float(5))

        # Checking awards for seller_2
        award_1 = seller_2_data[0]
        # Checking latest award
        award_info = award_1["award_info"]
        award_item_list = award_1["award_item_list"]
        self.assertEqual(award_info["award_id"], 2)
        self.assertIsNone(award_info["deleted_datetime"])
        self.assertEqual(len(award_item_list), 1)
        self.assertEqual(award_item_list[0]["item_info"]["award_line_item_id"], 2)
        self.assertEqual(award_item_list[0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_item_list[0]["item_tax"]), 2)
        self.assertEqual(award_item_list[0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_item_list[0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_item_list[0]["item_tax"][1]["tax_name"], "CGST")
        self.assertEqual(float(award_item_list[0]["item_tax"][1]["value"]), float(5))
    
    def test_get_invalid_event_award_history(self):
        # Getting award history for an event id 2 which doesn't exist
        response = self.client.get(reverse("event:event_award_history", args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_valid_seller_award_history(self):
        # Posting a new award version of the award 1
        data = {
            "award_info": {
                "event_id": 1, 
                "creator_user_id": 1,
                "approver_user_id": 2, 
                "draft_purchase_order_id": 0, 
                "purchase_order_id": 0,
                "buyer_id": 1, 
                "seller_id": 2, 
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
                            "value": 10
                        }
                    ]
                }
            ]
        }
        response = self.client.post(reverse("event:award_new_version", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Getting seller 1 award history
        response = self.client.get(reverse("event:seller_award_history", args=[1,2]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        award_1 = response.data[0]
        award_2 = response.data[1]
        # Checking latest award
        award_info = award_1["award_info"]
        award_item_list = award_1["award_item_list"]
        self.assertEqual(award_info["award_id"], 3)
        self.assertIsNone(award_info["deleted_datetime"])
        self.assertEqual(len(award_item_list), 1)
        self.assertEqual(award_item_list[0]["item_info"]["award_line_item_id"], 3)
        self.assertEqual(award_item_list[0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_item_list[0]["item_tax"]), 2)
        self.assertEqual(award_item_list[0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_item_list[0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_item_list[0]["item_tax"][1]["tax_name"], "CGST")
        self.assertEqual(float(award_item_list[0]["item_tax"][1]["value"]), float(10))
        # Checking oldest award
        award_info = award_2["award_info"]
        award_item_list = award_2["award_item_list"]
        self.assertEqual(award_info["award_id"], 1)
        self.assertIsNotNone(award_info["deleted_datetime"])
        self.assertEqual(len(award_item_list), 1)
        self.assertEqual(award_item_list[0]["item_info"]["award_line_item_id"], 1)
        self.assertEqual(award_item_list[0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_item_list[0]["item_tax"]), 2)
        self.assertEqual(award_item_list[0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_item_list[0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_item_list[0]["item_tax"][1]["tax_name"], "CGST")
        self.assertEqual(float(award_item_list[0]["item_tax"][1]["value"]), float(5))

        # Getting seller 2 award history
        response = self.client.get(reverse("event:seller_award_history", args=[1,3]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        award_1 = response.data[0]
        # Checking latest award
        award_info = award_1["award_info"]
        award_item_list = award_1["award_item_list"]
        self.assertEqual(award_info["award_id"], 2)
        self.assertIsNone(award_info["deleted_datetime"])
        self.assertEqual(len(award_item_list), 1)
        self.assertEqual(award_item_list[0]["item_info"]["award_line_item_id"], 2)
        self.assertEqual(award_item_list[0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(len(award_item_list[0]["item_tax"]), 2)
        self.assertEqual(award_item_list[0]["item_tax"][0]["tax_name"], "GST")
        self.assertEqual(float(award_item_list[0]["item_tax"][0]["value"]), float(5))
        self.assertEqual(award_item_list[0]["item_tax"][1]["tax_name"], "CGST")
        self.assertEqual(float(award_item_list[0]["item_tax"][1]["value"]), float(5))