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
from invoice.models import *
from invoice.serializers import *

class InvoiceModelViewTest(TestCase):

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
            "user_firstname": "ll",
            "user_lastname": "ll",
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
            "user_firstname": "ll",
            "user_lastname": "ll",
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
            "seller_id": self.seller2,
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
        data_invoice_info = {
			"invoice_type": "goods",
			"created_by_user_id": self.user1,
			"seller_invoice_id": "123",
			"provisional_invoice_id": "",
			"delivery_document_id": "",
			"purchase_order_id": self.purchase_order,
			"buyer_purchase_order_id": "131",
			"invoice_creation_datetime": "2021-06-22T07:40:55.646607Z",
			"seller_id": self.seller2,
			"seller_entity_name": "Apple",
			"seller_address_id": self.address1,
			"seller_contact_user_id": self.user2,
			"seller_contact_name": "Apps",
			"seller_contact_phone": "99xxxx",
			"seller_contact_email": "apple1@gmail.com",
			"buyer_id": self.buyer,
			"buyer_entity_name": "Factwise",
			"buyer_billing_address_id": self.address2,
			"buyer_shipping_address_id": self.address2,
			"buyer_contact_user_id": self.user1,
			"buyer_contact_name": "Matt ",
			"buyer_contact_phone": "91xxx91",
			"buyer_contact_email": "matt@factwise.io",
			"invoice_discount_percentage": "0.0000000000",
			"seller_comments": "",
			"status": "issued"
		}
        DraftInvoice.objects.create(**data_invoice_info)
        self.invoice = DraftInvoice.objects.get(invoice_id=1)
        data_invoice_item = {
            "invoice_id" : self.invoice,
            "purchase_order_line_item_id": self.purchase_order_item,
            "item_id": self.item,
            "buyer_item_id": "20013",
            "buyer_item_name": "20013 IPhone - White",
            "buyer_item_description": "",
            "seller_comments": "",
            "measurement_unit_id": self.measurement_unit_id,
            "rate": 5,
            "quantity_invoiced": 50,
            "shipping_per_unit": 5,
            "amount_invoiced": 250,
            "amount_due": 0,
            "amount_paid": 0,
            "currency_code": self.currency_code,
            "payment_terms_reference_date_type": "",
            "payment_due_date": "2021-05-17T09:49:43.583737Z"
        }
        DraftInvoiceItem.objects.create(**data_invoice_item)
        self.invoice_item = DraftInvoiceItem.objects.get(invoice_line_item_id=1)
        data_invoice_item_charge = {
            "invoice_line_item_id" : self.invoice_item,
            "charge_name": "GST",
            "charge_percentage": 5
        }
        DraftInvoiceItemCharge.objects.create(**data_invoice_item_charge)
        data_invoice_item_attribute = {
            "invoice_line_item_id" : self.invoice_item,
            "attribute_id": self.attribute,
            "attribute_value": "6GB"
        }
        DraftInvoiceItemAttribute.objects.create(**data_invoice_item_attribute)
        data_invoice_buyer_info = {
            "invoice_id" : self.invoice,
            "buyer_id": self.buyer,
            "identification_id": self.entity_identitfication1,
            "identification_name": "GST",
            "identification_value": "1234557"
        }
        DraftInvoiceBuyerInformation.objects.create(**data_invoice_buyer_info)
        data_invoice_seller_info = {
            "invoice_id" : self.invoice,
            "seller_id": self.seller2,
            "identification_id": self.entity_identitfication2,
            "identification_name": "CGST",
            "identification_value": "1234557"
        }
        DraftInvoiceSellerInformation.objects.create(**data_invoice_seller_info)
    
    def test_get_valid_draft_invoice(self):
        # Getting draft invoice with id 1
        response = self.client.get(reverse("invoice:draft_invoice", args=[1]))
        self.assertEqual(response.status_code, 200)
        invoice_info = response.data["invoice_info"]
        invoice_item_list = response.data["invoice_item_list"]
        invoice_buyer_information = response.data["invoice_buyer_information"]
        invoice_seller_information = response.data["invoice_seller_information"]
        
        self.assertEqual(invoice_info["invoice_id"], 1)
        self.assertEqual(invoice_info["buyer_id"], 1)
        self.assertEqual(invoice_info["seller_id"], 3)
        self.assertEqual(invoice_info["status"], "issued")
        
        self.assertEqual(len(invoice_item_list), 1)
        self.assertEqual(invoice_item_list[0]["item_info"]["invoice_line_item_id"], 1)
        self.assertEqual(invoice_item_list[0]["item_info"]["invoice_id"], 1)
        self.assertEqual(invoice_item_list[0]["item_info"]["item_id"], 1)
        
        self.assertEqual(len(invoice_item_list[0]["item_attribute"]), 1)
        self.assertEqual(invoice_item_list[0]["item_attribute"][0]["invoice_line_item_id"], 1)
        
        self.assertEqual(len(invoice_item_list[0]["item_charge"]), 1)
        self.assertEqual(invoice_item_list[0]["item_charge"][0]["invoice_line_item_id"], 1)
        
        self.assertEqual(len(invoice_buyer_information), 1)
        self.assertEqual(invoice_buyer_information[0]["invoice_id"], 1)
        self.assertEqual(invoice_buyer_information[0]["buyer_id"], 1)
        
        self.assertEqual(len(invoice_seller_information), 1)
        self.assertEqual(invoice_seller_information[0]["invoice_id"], 1)
        self.assertEqual(invoice_seller_information[0]["seller_id"], 3)
    
    def test_get_invalid_draft_invoice(self):
        # Getting draft invoice with id 2 which doesn't exist
        response = self.client.get(reverse("invoice:draft_invoice", args=[2]))
        self.assertEqual(response.status_code, 404)
        
    def test_patch_valid_invoice(self):
        # Patching status invoice with 1
        data = {
            "invoice_info": {
                "invoice_type": "goods",
                "created_by_user_id": 1,
                "seller_invoice_id": "123",
                "provisional_invoice_id": "",
                "delivery_document_id": "",
                "purchase_order_id": 1,
                "buyer_purchase_order_id": "131",
                "invoice_creation_datetime": "2021-06-22T07:40:55.646607Z",
                "seller_id": 3,
                "seller_entity_name": "Apple",
                "seller_address_id": 1,
                "seller_contact_user_id": 2,
                "seller_contact_name": "ll",
                "seller_contact_phone": "99xxxx",
                "seller_contact_email": "apple1@gmail.com",
                "buyer_id": 1,
                "buyer_entity_name": "Factwise",
                "buyer_billing_address_id": 2,
                "buyer_shipping_address_id": 2,
                "buyer_contact_user_id": 1,
                "buyer_contact_name": "Matt ",
                "buyer_contact_phone": "91xxx91",
                "buyer_contact_email": "mt@factwise.io",
                "invoice_discount_percentage": "0.0000000000",
                "seller_comments": "",
                "status": "issued"
            },
            "invoice_item_list": [
                {
                    "item_info": {
                        "purchase_order_line_item_id": 1,
                        "item_id": 1,
                        "buyer_item_id": "20013",
                        "buyer_item_name": "20013 IPhone - White",
                        "buyer_item_description": "",
                        "seller_comments": "",
                        "measurement_unit_id": 1,
                        "rate": 5,
                        "quantity_invoiced": 50,
                        "shipping_per_unit": 5,
                        "amount_invoiced": 250,
                        "amount_due": 0,
                        "amount_paid": 0,
                        "currency_code": "USD",
                        "payment_terms_reference_date_type": "",
                        "payment_due_date": "2021-05-17T09:49:43.583737Z"
                    },
                    "item_charge": [
                        {
                            "charge_name": "SGST",
                            "charge_percentage": 5
                        },
                        {
                            "charge_name": "CGST",
                            "charge_percentage": 5
                        }
                    ],
                    "item_attribute": [
                        {
                            "attribute_id": 1,
                            "attribute_value": "6GB"
                        }
                    ]
                }
            ],
            "invoice_buyer_information": [
                {
                    "buyer_id": 1,
                    "identification_id": 1,
                    "identification_name": "SGST",
                    "identification_value": "1234557"
                }
            ],
            "invoice_seller_information": [
                {
                    "seller_id": 3,
                    "identification_id": 2,
                    "identification_name": "GST",
                    "identification_value": "1234557"
                }
            ]
        }
        response = self.client.patch(reverse("invoice:draft_invoice", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        invoice_info = response.data["invoice_info"]
        invoice_item_list = response.data["invoice_item_list"]
        invoice_buyer_information = response.data["invoice_buyer_information"]
        invoice_seller_information = response.data["invoice_seller_information"]
        
        self.assertEqual(invoice_info["invoice_id"], 1)
        self.assertEqual(invoice_info["buyer_id"], 1)
        self.assertEqual(invoice_info["seller_id"], 3)
        self.assertEqual(invoice_info["status"], "issued")
        self.assertEqual(invoice_info["seller_contact_name"], "ll")
        self.assertEqual(invoice_info["buyer_contact_email"], "mt@factwise.io")
        
        self.assertEqual(len(invoice_item_list), 1)
        self.assertEqual(invoice_item_list[0]["item_info"]["invoice_line_item_id"], 2)
        self.assertEqual(invoice_item_list[0]["item_info"]["invoice_id"], 1)
        self.assertEqual(invoice_item_list[0]["item_info"]["item_id"], 1)
        
        self.assertEqual(len(invoice_item_list[0]["item_attribute"]), 1)
        self.assertEqual(invoice_item_list[0]["item_attribute"][0]["invoice_line_item_id"], 2)
        
        self.assertEqual(len(invoice_item_list[0]["item_charge"]), 2)
        self.assertEqual(invoice_item_list[0]["item_charge"][0]["invoice_line_item_id"], 2)
        self.assertEqual(invoice_item_list[0]["item_charge"][0]["charge_name"], "SGST")
        
        self.assertEqual(len(invoice_buyer_information), 1)
        self.assertEqual(invoice_buyer_information[0]["invoice_id"], 1)
        self.assertEqual(invoice_buyer_information[0]["buyer_id"], 1)
        self.assertEqual(invoice_buyer_information[0]["identification_name"], "SGST")
        
        self.assertEqual(len(invoice_seller_information), 1)
        self.assertEqual(invoice_seller_information[0]["invoice_id"], 1)
        self.assertEqual(invoice_seller_information[0]["seller_id"], 3)
        self.assertEqual(invoice_seller_information[0]["identification_name"], "GST")
    
    def test_patch_invalid_draft_invoice(self):
        # Patching status invoice with 2 which doesn't exist
        data = {
            "invoice_info": {
                "invoice_type": "goods",
                "created_by_user_id": 1,
                "seller_invoice_id": "123",
                "provisional_invoice_id": "",
                "delivery_document_id": "",
                "purchase_order_id": 1,
                "buyer_purchase_order_id": "131",
                "invoice_creation_datetime": "2021-06-22T07:40:55.646607Z",
                "seller_id": 3,
                "seller_entity_name": "Apple",
                "seller_address_id": 1,
                "seller_contact_user_id": 2,
                "seller_contact_name": "ll",
                "seller_contact_phone": "99xxxx",
                "seller_contact_email": "apple1@gmail.com",
                "buyer_id": 1,
                "buyer_entity_name": "Factwise",
                "buyer_billing_address_id": 2,
                "buyer_shipping_address_id": 2,
                "buyer_contact_user_id": 1,
                "buyer_contact_name": "Matt ",
                "buyer_contact_phone": "91xxx91",
                "buyer_contact_email": "mt@factwise.io",
                "invoice_discount_percentage": "0.0000000000",
                "seller_comments": "",
                "status": "issued"
            },
            "invoice_item_list": [
                {
                    "item_info": {
                        "purchase_order_line_item_id": 1,
                        "buyer_item_id": "20013",
                        "buyer_item_name": "20013 IPhone - White",
                        "buyer_item_description": "",
                        "seller_comments": "",
                        "measurement_unit_id": 1,
                        "rate": 5,
                        "quantity_invoiced": 50,
                        "shipping_per_unit": 5,
                        "amount_invoiced": 250,
                        "amount_due": 0,
                        "amount_paid": 0,
                        "currency_code": "USD",
                        "payment_terms_reference_date_type": "",
                        "payment_due_date": "2021-05-17T09:49:43.583737Z"
                    },
                    "item_charge": [
                        {
                            "charge_name": "SGST",
                            "charge_percentage": 5
                        },
                        {
                            "charge_name": "CGST",
                            "charge_percentage": 5
                        }
                    ],
                    "item_attribute": [
                        {
                            "attribute_id": 1,
                            "attribute_value": "6GB"
                        }
                    ]
                }
            ],
            "invoice_buyer_information": [
                {
                    "buyer_id": 1,
                    "identification_id": 1,
                    "identification_name": "SGST",
                    "identification_value": "1234557"
                }
            ],
            "invoice_seller_information": [
                {
                    "seller_id": 3,
                    "identification_id": 2,
                    "identification_name": "GST",
                    "identification_value": "1234557"
                }
            ]
        }
        response = self.client.patch(reverse("invoice:draft_invoice", args=[2]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        # Checking if status remains the previous issued status only or has changed
        draft_invoice_info = DraftInvoice.objects.get(invoice_id=1)
        self.assertEqual(draft_invoice_info.status, "issued")

        # checking for the correct data (model validation)
        # in the given data item info is invalid (item id is missing)
        response = self.client.patch(reverse("invoice:draft_invoice", args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete_valid_draft_invoice(self):
        # Deleting a valid Draft invoice with id 1
        response = self.client.delete(reverse("invoice:draft_invoice", args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_invalid_draft_invoice(self):
        # Deleting a valid Draft invoice with id 1
        response = self.client.delete(reverse("invoice:draft_invoice", args=[1]))
        self.assertEqual(response.status_code, 200)
        # Again deleting the Draft invoice (already deleted) with id 1
        response = self.client.delete(reverse("invoice:draft_invoice", args=[1]))
        self.assertEqual(response.status_code, 404)

        # Deleting a valid Draft invoice with id 2 which does not exist
        response = self.client.delete(reverse("invoice:draft_invoice", args=[2]))
        self.assertEqual(response.status_code, 404)    