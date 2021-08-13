from datetime import time
from django.test import TestCase
from django.urls import reverse
import json
from django.utils import timezone

from enterprise.models import *
from enterprise.serializers import *
from event.models import *
from event.serializers import *
from purchase_order.models import *
from purchase_order.serializers import *

class SellerPurchaseOrdeResponseViewTest(TestCase):

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
            "seller_id": self.entity2
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
            "attribute_name": "Color",
            "attribute_value_type": "enum"
        }
        Attribute.objects.create(**attribute_data)
        self.attribute = Attribute.objects.get(attribute_id=1)
        event_item_attribute_data = {
            "event_line_item_id" : self.event_item,
            "attribute_id" : self.attribute,
            "attribute_value" : "BLUE"
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

        purchase_order_info_data ={ 
            "event_id": self.event, 
            "purchase_order_creation_datetime": "2021-05-17T09:49:43.583737Z", 
            "buyer_id": self.buyer, 
            "buyer_purchase_order_id": "1233", 
            "buyer_entity_name": "Factwise", 
            "buyer_billing_address_id": self.address1, 
            "buyer_shipping_address_id": self.address1, 
            "buyer_approver_user_id": self.user1, 
            "buyer_approver_name": "Person1", 
            "buyer_contact_user_id": self.user1, 
            "buyer_contact_name": "Person2", 
            "buyer_contact_phone": "9xxxxxx12", 
            "buyer_contact_email": "factwise@gmail.com", 
            "is_freight_purchase_order": "False", 
            "seller_id": self.seller1, 
            "seller_entity_name": "Apple", 
            "seller_address_id": self.address2, 
            "seller_contact_user_id": self.user2, 
            "seller_contact_name": "Nishant", 
            "seller_contact_phone": "9xxxxx12", 
            "seller_contact_email": "apple1@gmail.com", 
            
            "delivery_schedule_type": "kfiuw", 
            "payment_terms_code": "USD", 
            "purchase_order_discount_percentage": 0, 
            "buyer_comments": "Nothing", 
            "status": "issued"
        }
        # "seller_acknowledgement_user_id": self.user2, 
        # "seller_acknowledgement_datetime": "2021-05-17T09:49:43.583737Z",
        PurchaseOrder.objects.create(**purchase_order_info_data)
        self.purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        data_purchase_order_buyer_info = {
            "purchase_order_id": self.purchase_order,
            "buyer_id": self.buyer,
            "identification_id": self.entity_identitfication1,
            "identification_name": "GST",
            "identification_value": "1234557"
        }
        PurchaseOrderBuyerInformation.objects.create(**data_purchase_order_buyer_info)
        data_purchase_order_seller_info = {
            "purchase_order_id": self.purchase_order,
            "seller_id": self.seller1,
            "identification_id": self.entity_identitfication2,
            "identification_name": "CGST",
            "identification_value": "1234557"
        }
        PurchaseOrderSellerInformation.objects.create(**data_purchase_order_seller_info)
        data_purchase_order_item_info = {
            "purchase_order_id" : self.purchase_order,
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
        PurchaseOrderItem.objects.create(**data_purchase_order_item_info)
        self.purchase_order_item = PurchaseOrderItem.objects.get(purchase_order_line_item_id=1)
        data_purchase_order_item_attribute = {
            "purchase_order_line_item_id" : self.purchase_order_item,
            "attribute_id": self.attribute,
            "attribute_value": "BLUE"
        }
        PurchaseOrderItemAttribute.objects.create(**data_purchase_order_item_attribute)
        data_purchase_order_item_charge = {
            "purchase_order_line_item_id" : self.purchase_order_item,
            "charge_name": "GST",
            "charge_percentage": 5
        }
        PurchaseOrderItemCharge.objects.create(**data_purchase_order_item_charge)
        user_entity_data1 = {
            "user_id": self.user1,
            "entity_id": self.entity1
        }
        UserEntity.objects.create(**user_entity_data1)
        user_entity_data2 = {
            "user_id": self.user2,
            "entity_id": self.entity2
        }
        UserEntity.objects.create(**user_entity_data2)
    
    def test_patch_valid_seller_accept_purchase_order(self):
        # Accepting a Purchase Order with id 1, user_id 2 and entity_id 3 (seller side)
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        self.assertEqual(purchase_order.status, "issued")
        self.assertIsNone(purchase_order.seller_acknowledgement_user_id)
        self.assertIsNone(purchase_order.seller_acknowledgement_datetime)
        data = {
            "status": "ongoing"
        }
        response = self.client.patch(reverse("purchase_order:seller_purchase_order_response", args=[2, 2, 1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # Getting this accepted purchase order
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        self.assertEqual(purchase_order.status, "ongoing")
        self.assertEqual(purchase_order.seller_acknowledgement_user_id.user_id, 2)
        self.assertIsNotNone(purchase_order.seller_acknowledgement_datetime)
    
    def test_patch_valid_seller_decline_purchase_order(self):
        # Accepting a Purchase Order with id 1, user_id 2 and entity_id 3 (seller side)
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        self.assertEqual(purchase_order.status, "issued")
        self.assertIsNone(purchase_order.seller_acknowledgement_user_id)
        self.assertIsNone(purchase_order.seller_acknowledgement_datetime)
        self.assertIsNone(purchase_order.closing_user_id_seller)
        self.assertEqual(purchase_order.closing_comment_seller, "")
        self.assertIsNone(purchase_order.closing_datetime_seller)
        self.assertIsNone(purchase_order.purchase_order_close_datetime)
        data = {
            "status": "declined",
            "closing_comment_seller": "I am not interested"
        }
        response = self.client.patch(reverse("purchase_order:seller_purchase_order_response", args=[2, 2, 1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # Getting this declined purchase order
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        self.assertEqual(purchase_order.status, "declined")
        self.assertEqual(purchase_order.seller_acknowledgement_user_id.user_id, 2)
        self.assertIsNotNone(purchase_order.seller_acknowledgement_datetime)
        self.assertEqual(purchase_order.closing_user_id_seller.user_id, 2)
        self.assertEqual(purchase_order.closing_comment_seller, "I am not interested")
        self.assertIsNotNone(purchase_order.closing_datetime_seller)
        self.assertIsNotNone(purchase_order.purchase_order_close_datetime)

    def test_patch_invalid_seller_accept_purchase_order(self):
        # Accepting a Purchase Order with id 1, user_id 2 and entity_id 2 (seller side)
        # that is already accepted
        # First accepting
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        purchase_order.status = "ongoing"
        purchase_order.seller_acknowledgement_user_id = self.user2
        purchase_order.seller_acknowledgement_datetime = timezone.now()
        purchase_order.save()
        # Again accepting
        data = {
            "status": "ongoing"
        }
        response = self.client.patch(reverse("purchase_order:seller_purchase_order_response", args=[2, 2, 1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        # Again renewing the data
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        purchase_order.status = "issued"
        purchase_order.seller_acknowledgement_user_id = None
        purchase_order.seller_acknowledgement_datetime = None
        purchase_order.save()

        # Accepting a declined Purchase Order

        # Declining the Purchase Order
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        purchase_order.status = "declined"
        purchase_order.seller_acknowledgement_user_id = self.user2
        purchase_order.seller_acknowledgement_datetime = timezone.now()
        purchase_order.closing_user_id_seller = self.user2
        purchase_order.closing_comment_seller = "I am not interested"
        purchase_order.closing_datetime_seller = timezone.now()
        purchase_order.purchase_order_close_datetime = timezone.now()
        purchase_order.save()

        # Accepting this declined Purchase Order
        data = {
            "status": "ongoing"
        }
        response = self.client.patch(reverse("purchase_order:seller_purchase_order_response", args=[2, 2, 1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
    
    def test_patch_invalid_seller_decline_purchase_order(self):
        # Declining a Purchase Order with id 1, user_id 2 and entity_id 2 (seller side)
        # that is already declined
        # Declining the Purchase Order
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        purchase_order.status = "declined"
        purchase_order.seller_acknowledgement_user_id = self.user2
        purchase_order.seller_acknowledgement_datetime = timezone.now()
        purchase_order.closing_user_id_seller = self.user2
        purchase_order.closing_comment_seller = "I am not interested"
        purchase_order.closing_datetime_seller = timezone.now()
        purchase_order.purchase_order_close_datetime = timezone.now()
        purchase_order.save()

        # Again declining
        data = {
            "status": "declined",
            "closing_comment_seller": "I am not interested"
        }
        response = self.client.patch(reverse("purchase_order:seller_purchase_order_response", args=[2, 2, 1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        # Again renewing the data
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        purchase_order.status = "issued"
        purchase_order.seller_acknowledgement_user_id = None
        purchase_order.seller_acknowledgement_datetime = None
        purchase_order.closing_user_id_seller = None
        purchase_order.closing_comment_seller = ""
        purchase_order.closing_datetime_seller = None
        purchase_order.purchase_order_close_datetime = None
        purchase_order.save()

        # Declining a accepted Purchase Order

        # Accepting the Purchase Order
        purchase_order = PurchaseOrder.objects.get(purchase_order_id=1)
        purchase_order.status = "ongoing"
        purchase_order.seller_acknowledgement_user_id = self.user2
        purchase_order.seller_acknowledgement_datetime = timezone.now()
        purchase_order.save()

        # Declining this accepted Purchase Order
        data = {
            "status": "declined"
        }
        response = self.client.patch(reverse("purchase_order:seller_purchase_order_response", args=[2, 2, 1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
    
    def test_patch_invalid_seller_purchase_order_response(self):
        # Some status other than declined and ongoing
        data = {
            "status": "something which is invalid"
        }
        response = self.client.patch(reverse("purchase_order:seller_purchase_order_response", args=[2, 2, 1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)