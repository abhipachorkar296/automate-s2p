from django.test import TestCase
from django.urls import reverse
import json
from unittest.mock import patch
from enterprise.models import * 
from enterprise.serializers import *
from purchase_order.models import *
from purchase_order.serializers import *
from purchase_order.models import *
from purchase_order.serializers import *
import requests

class DraftPurchaseOrderListViewTest(TestCase):
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
        user_data1 = {
            "enterprise_id": self.enterprise,
            "user_email": "apple1@gmail.com",
            "user_firstname": "Pratyush",
            "user_lastname": "Jaiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**user_data1)
        self.user1 = User.objects.get(user_id=1)
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
        user_data2 = {
            "enterprise_id": self.enterprise2,
            "user_email": "appl1@gmail.com",
            "user_firstname": "Prtyush",
            "user_lastname": "aiswal",
            "user_phonenumber": "xxxxxx91"
        }
        User.objects.create(**user_data2)
        self.user2 = User.objects.get(user_id=2)
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
        event_item_seller_data = [
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
        EventItemSeller.objects.bulk_create(EventItemSeller(**x) for x in event_item_seller_data)
        data_entity_identitfication1 = {
            "entity_id": self.entity1,
            "identification_name": "GST",
            "identification_category": "GST",
            "identification_value": "1234557"
        }
        EntityIdentification.objects.create(**data_entity_identitfication1)
        self.entity_identitfication1 = EntityIdentification.objects.get(identification_id=1)
        data_entity_identitfication2 = {
            "entity_id": self.entity2,
            "identification_name": "SGST",
            "identification_category": "SGST",
            "identification_value": "124557"
        }
        EntityIdentification.objects.create(**data_entity_identitfication2)
        self.entity_identitfication2 = EntityIdentification.objects.get(identification_id=2)
        draft_purchase_order_info_data ={ 
            "event_id": self.event, 
            "purchase_order_creation_datetime": "2021-05-17T09:49:43.583737Z", 
            "buyer_id": self.buyer, 
            "buyer_purchase_order_id": "1233", 
            "buyer_entity_name": "Factwise", 
            "buyer_billing_address_id": self.address1, 
            "buyer_shipping_address_id": self.address1, 
            "buyer_approver_user_id": self.user1, 
            "buyer_approver_name": "Pratyush", 
            "buyer_contact_user_id": self.user1, 
            "buyer_contact_name": "Abhishek", 
            "buyer_contact_phone": "9xxxxxx12", 
            "buyer_contact_email": "jaiswalpratyush2015@gmail.com", 
            "is_freight_purchase_order": "False", 
            "seller_id": self.seller2, 
            "seller_entity_name": "Apple", 
            "seller_address_id": self.address2, 
            "seller_contact_user_id": self.user2, 
            "seller_contact_name": "Nishant", 
            "seller_contact_phone": "9xxxxx12", 
            "seller_contact_email": "apple1@gmail.com", 
            "seller_acknowledgement_user_id": self.user2, 
            "seller_acknowledgement_datetime": "2021-05-17T09:49:43.583737Z",
            "delivery_schedule_type": "kfiuw", 
            "payment_terms_code": "USD", 
            "purchase_order_discount_percentage": 0, 
            "buyer_comments": "Nothing", 
            "status": "issued"
        }
        DraftPurchaseOrder.objects.create(**draft_purchase_order_info_data)
        self.draft_purchase_order = DraftPurchaseOrder.objects.get(purchase_order_id=1)
        data_purchase_order_buyer_info = {
            "purchase_order_id" : self.draft_purchase_order,
            "buyer_id": self.buyer,
            "identification_id": self.entity_identitfication1,
            "identification_name": "GST",
            "identification_value": "1234557"
        }
        DraftPurchaseOrderBuyerInformation.objects.create(**data_purchase_order_buyer_info)
        data_purchase_order_seller_info = {
            "purchase_order_id" : self.draft_purchase_order,
            "seller_id": self.seller2,
            "identification_id": self.entity_identitfication2,
            "identification_name": "CGST",
            "identification_value": "1234557"
        }
        DraftPurchaseOrderSellerInformation.objects.create(**data_purchase_order_seller_info)
        data_purchase_order_item_info = {
            "purchase_order_id" : self.draft_purchase_order,
            "item_id": self.item, 
            "buyer_item_id": "20013", 
            "buyer_item_name": "20013 IPhone - White", 
            "buyer_item_description": "", 
            "due_date": "2021-05-17T09:49:43.583737Z", 
            "currency_code": self.currency_code, 
            "measurement_unit_id": self.measurement_unit_id, 
            "rate": 100, 
            "quantity": 100, 
            "max_acceptable_quantity": 300, 
            "taxes_and_charges_percentage": 0, 
            "taxes_and_charges_value": 0,
            "total_order_value": 10000
        }
        DraftPurchaseOrderItem.objects.create(**data_purchase_order_item_info)
        self.draft_purchase_order_item = DraftPurchaseOrderItem.objects.get(purchase_order_line_item_id=1)
        data_purchase_order_item_attribute = {
            "purchase_order_line_item_id" : self.draft_purchase_order_item,
            "attribute_id": self.attribute,
            "attribute_value": "BLUE"
        }
        DraftPurchaseOrderItemAttribute.objects.create(**data_purchase_order_item_attribute)
        data_purchase_order_item_charge = {
            "purchase_order_line_item_id" : self.draft_purchase_order_item,
            "charge_name": "GST",
            "charge_percentage": 5
        }
        DraftPurchaseOrderItemCharge.objects.create(**data_purchase_order_item_charge)


    def test_get_valid_purchase_order_list(self):
        '''
        Getting purchase order with event id  1, seller id 3
        '''
        response = self.client.get(reverse("purchase_order:draft_purchase_order_list" , args=[1,3]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["purchase_order_info"]["purchase_order_id"], 1)
        self.assertEqual(response.data["purchase_order_info"]["buyer_purchase_order_id"], "1233")
        self.assertEqual(response.data["purchase_order_item_list"][0]["item_info"]["purchase_order_line_item_id"], 1)
        self.assertEqual(response.data["purchase_order_item_list"][0]["item_attribute"][0]["attribute_id"], 1)
        self.assertEqual(response.data["purchase_order_item_list"][0]["item_charge"][0]["charge_name"], "GST")

    def test_get_invalid_purchase_order_list(self):
        '''
        Getting purchase order with event id  1, seller id 2 (does not exist)
        '''
        response = self.client.get(reverse("purchase_order:draft_purchase_order_list" , args=[1,2]))
        self.assertEqual(response.status_code, 404)
        '''
        Getting purchase order with event id  2, seller id 3 (does not exist)
        '''
        response = self.client.get(reverse("purchase_order:draft_purchase_order_list" , args=[2,3]))
        self.assertEqual(response.status_code, 404)

    def test_post_valid_purchase_order(self):
        '''
        posting purchase order with event 1 and seller id 4 with status
        '''
        data = {
            "purchase_order_info": {
                "purchase_order_creation_datetime": "2021-05-17T09:49:43.583737Z", 
                "buyer_id": 1, 
                "buyer_purchase_order_id": "1233", 
                "buyer_entity_name": "Factwise", 
                "buyer_billing_address_id": 1, 
                "buyer_shipping_address_id": 2, 
                "buyer_approver_user_id": 1, 
                "buyer_approver_name": "a", 
                "buyer_contact_user_id": 1, 
                "buyer_contact_name": "a", 
                "buyer_contact_phone": "9xxxxxx12", 
                "buyer_contact_email": "aa@gmail.com", 
                "is_freight_purchase_order": "False", 
                "seller_entity_name": "Apple", 
                "seller_address_id": 2, 
                "seller_contact_user_id": 2, 
                "seller_contact_name": "Nishant", 
                "seller_contact_phone": "9xxxxx12", 
                "seller_contact_email": "apple1@gmail.com", 
                "seller_acknowledgement_user_id": 2, 
                "seller_acknowledgement_datetime": "2021-05-17T09:49:43.583737Z",
                "delivery_schedule_type": "kfiuw", 
                "payment_terms_code": "USD", 
                "purchase_order_discount_percentage": 0, 
                "buyer_comments": "Nothing", 
                "status": "issued"
            },
            "purchase_order_item_list": [
                {
                    "item_info": {
                        "item_id": 1, 
                        "buyer_item_id": "20013", 
                        "buyer_item_name": "20013 IPhone - White", 
                        "buyer_item_description": "", 
                        "due_date": "2021-05-17T09:49:43.583737Z", 
                        "currency_code": "USD", 
                        "measurement_unit_id": 1, 
                        "rate": 100, 
                        "quantity": 100, 
                        "max_acceptable_quantity": 300, 
                        "taxes_and_charges_percentage": 0, 
                        "taxes_and_charges_value": 0,
                        "total_order_value": 10000
                    },
                    "item_attribute": [
                        {
                            "attribute_id": 1,
                            "attribute_value": "BLUE"
                        }   
                    ],
                    "item_charge": [
                        {
                            "charge_name": "GST",
                            "charge_percentage": 5
                        }
                    ]
                }
                
            ],
            "purchase_order_buyer_information": [
                {
                    "buyer_id": 1,
                    "identification_id": 1,
                    "identification_name": "GST",
                    "identification_value": "1234557"
                }
            ],
            "purchase_order_seller_information": [
                {
                    "identification_id": 2,
                    "identification_name": "CGST",
                    "identification_value": "1234557"
                }
            ]
        }
        data = json.dumps(data)
        response = self.client.post(reverse("purchase_order:draft_purchase_order_list" , args=[1,2]), data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["purchase_order_info"]["purchase_order_id"], 2)
        self.assertEqual(response.data["purchase_order_info"]["buyer_purchase_order_id"], "1233")
        self.assertEqual(response.data["purchase_order_item_list"][0]["item_info"]["purchase_order_line_item_id"], 2)
        self.assertEqual(response.data["purchase_order_item_list"][0]["item_attribute"][0]["attribute_id"], 1)
        self.assertEqual(response.data["purchase_order_item_list"][0]["item_charge"][0]["charge_name"], "GST")

    def test_post_invalid_purchase_order(self):
        '''
        posting purchase order with ID 2 with stauts
        '''
        data = {
            "purchase_order_info": {
                "purchase_order_creation_datetime": "2021-05-17T09:49:43.583737Z", 
                "buyer_id": 1, 
                "buyer_purchase_order_id": "1233", 
                "buyer_entity_name": "Factwise", 
                "buyer_billing_address_id": 1, 
                "buyer_shipping_address_id": 2, 
                "buyer_approver_user_id": 1, 
                "buyer_approver_name": "a", 
                "buyer_contact_user_id": 1, 
                "buyer_contact_name": "a", 
                "buyer_contact_phone": "9xxxxxx12", 
                "buyer_contact_email": "aa@gmail.com", 
                "is_freight_purchase_order": "False", 
                "seller_entity_name": "Apple", 
                "seller_address_id": 2, 
                "seller_contact_user_id": 2, 
                "seller_contact_name": "Nishant", 
                "seller_contact_phone": "9xxxxx12", 
                "seller_contact_email": "apple1@gmail.com", 
                "seller_acknowledgement_user_id": 2, 
                "seller_acknowledgement_datetime": "2021-05-17T09:49:43.583737Z",
                "delivery_schedule_type": "kfiuw", 
                "payment_terms_code": "USD", 
                "purchase_order_discount_percentage": 0, 
                "buyer_comments": "Nothing", 
                "status": "issued"
            },
            "purchase_order_item_list": [
                {
                    "item_info": {
                        "item_id": 1, 
                        "buyer_item_id": "20013", 
                        "buyer_item_name": "20013 IPhone - White", 
                        "buyer_item_description": "", 
                        "due_date": "2021-05-17T09:49:43.583737Z", 
                        "currency_code": "USD", 
                        "measurement_unit_id": 1, 
                        "rate": 100, 
                        "quantity": 100, 
                        "max_acceptable_quantity": 300, 
                        "taxes_and_charges_percentage": 0, 
                        "taxes_and_charges_value": 0,
                        "total_order_value": 10000
                    },
                    "item_attribute": [
                        {
                            "attribute_id": 1,
                            "attribute_value": "BLUE"
                        }   
                    ],
                    "item_charge": [
                        {
                            "charge_name": "GST",
                            "charge_percentage": 5
                        }
                    ]
                }
                
            ],
            "purchase_order_buyer_information": [
                {
                    "buyer_id": 1,
                    "identification_id": 1,
                    "identification_name": "GST",
                    "identification_value": "1234557"
                }
            ],
            "purchase_order_seller_information": [
                {
                    "identification_id": 2,
                    "identification_name": "CGST",
                    "identification_value": "1234557"
                }
            ]
        }
        data = json.dumps(data)
        #for non-exisiting event
        response = self.client.post(reverse("purchase_order:draft_purchase_order_list" , args=[2,2]), data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        #for non-exisiting seller
        response = self.client.post(reverse("purchase_order:draft_purchase_order_list" , args=[2,1]), data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_post_valid_draft_purchase_order_shift_purchase_order(self):
        '''
        shifting purchase order with po id 1
        '''
        response = self.client.post(reverse("purchase_order:draft_purchase_order_shift_purchase_order" , args=[1]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["purchase_order_info"]["purchase_order_id"], 1)
        self.assertEqual(response.data["purchase_order_info"]["buyer_purchase_order_id"], "1233")
        self.assertEqual(response.data["purchase_order_item_list"][0]["item_info"]["purchase_order_line_item_id"], 1)
        self.assertEqual(response.data["purchase_order_item_list"][0]["item_attribute"][0]["attribute_id"], 1)
        self.assertEqual(response.data["purchase_order_item_list"][0]["item_charge"][0]["charge_name"], "GST")

    def test_post_invalid_draft_purchase_order_shift_purchase_order(self):
        '''
        shifting purchase order with ID 2 with stauts
        '''
        #for non-exisiting purchase order
        response = self.client.post(reverse("purchase_order:draft_purchase_order_shift_purchase_order" , args=[2]))
        self.assertEqual(response.status_code, 404)