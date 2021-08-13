from django.test import TestCase
from django.urls import reverse
import json

from enterprise.models import *
from enterprise.serializers import *
from event.models import *
from event.serializers import *

class EventViewTest(TestCase):
    def setUp(self):
        '''
        Populating test db 
        Entering a event with event_id 1
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
        self.entity2 = Entity.objects.get(entity_id=1)
        seller_data1 = {
            "seller_id" : self.entity2
        }
        Seller.objects.create(**seller_data1)
        self.seller1 = Seller.objects.get(seller_id=1)
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
        self.entity2 = Entity.objects.get(entity_id=2)
        seller_data2 = {
            "seller_id" : self.entity2
        }
        Seller.objects.create(**seller_data2)
        self.seller2 = Seller.objects.get(seller_id=2)
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


    def test_get_valid_event(self):
        '''
        Getting event with ID 1
        '''
        response = self.client.get(reverse("event:event" , args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["event_info"]["event_id"], 1)
        self.assertEqual(response.data["event_item_list"][0]["item_info"]["event_line_item_id"], 1)
        self.assertEqual(response.data["event_item_list"][0]["item_attribute"][0]["attribute_id"], 1)
        self.assertEqual(response.data["event_item_list"][0]["item_seller"][1]["seller_id"], 2)

    def test_get_invalid_event(self):
        '''
        Getting event with ID 2, which does not exist
        '''
        response = self.client.get(reverse("event:event" , args=[2]))
        self.assertEqual(response.status_code, 404)
    
    def test_patch_valid_event(self):
        # Patching event with ID 1 with end datetime
        data = {
            "event_info": {
                "event_end_datetime": "2021-05-17T09:50:43.583737Z"
            }
        }
        response = self.client.patch(reverse("event:event" , args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(event_id=1)
        event_data = EventSerializer(event).data
        self.assertEqual(event_data["event_end_datetime"], "2021-05-17T09:50:43.583737Z")

        # Making the data as before
        event.event_end_datetime = "2021-05-17T09:49:43.583737Z"
        event.save()
        # Patching event with ID 1 with quantity change in event item
        data = {
            "event_item_list": [
                {
                    "item_info": {
                        "event_line_item_id": 1,
                        "desired_quantity": 200
                    }
                    
                }
            ]
        }
        response = self.client.patch(reverse("event:event" , args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        event_item = EventItem.objects.get(event_line_item_id=1)
        event_item_data = EventItemSerializer(event_item).data
        self.assertEqual(float(event_item_data["desired_quantity"]), float(200))

        # Making the data as before
        event_item.desired_quantity = 100
        event_item.save()
        # Patching event with ID 1 with end datetime and event item quantity
        data = {
            "event_info": {
                "event_end_datetime": "2021-05-17T09:50:43.583737Z"
            },
            "event_item_list": [
                {
                    "item_info": {
                        "event_line_item_id": 1,
                        "desired_quantity": 200
                    }
                    
                }
            ]
        }
        response = self.client.patch(reverse("event:event" , args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(event_id=1)
        event_data = EventSerializer(event).data
        self.assertEqual(event_data["event_end_datetime"], "2021-05-17T09:50:43.583737Z")
        event_item = EventItem.objects.get(event_line_item_id=1)
        event_item_data = EventItemSerializer(event_item).data
        self.assertEqual(float(event_item_data["desired_quantity"]), float(200))

        # Making the data as before
        event.event_end_datetime = "2021-05-17T09:49:43.583737Z"
        event.save()
        event_item.desired_quantity = 100
        event_item.save()
        # Patching event with ID 1 with end datetime and event item with 
        # ID 2(which does not belong to this event) quantity
        # Expected to change only end datetime
        data = {
            "event_info": {
                "event_end_datetime": "2021-05-17T09:50:43.583737Z"
            },
            "event_item_list": [
                {
                    "item_info": {
                        "event_line_item_id": 2,
                        "desired_quantity": 200
                    }
                    
                }
            ]
        }
        response = self.client.patch(reverse("event:event" , args=[1]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        event = Event.objects.get(event_id=1)
        event_data = EventSerializer(event).data
        self.assertEqual(event_data["event_end_datetime"], "2021-05-17T09:50:43.583737Z")
        event_item = EventItem.objects.get(event_line_item_id=1)
        event_item_data = EventItemSerializer(event_item).data
        self.assertEqual(float(event_item_data["desired_quantity"]), float(100))

    def test_patch_invalid_event(self):
        '''
        Patching event with ID 2 which does not exist
        '''
        data = {
            "event_info": {
                "event_end_datetime": "2021-05-17T09:50:43.583737Z"
            },
            "event_item_list": [
                {
                    "item_info": {
                        "event_line_item_id": 1,
                        "desired_quantity": 200
                    }
                    
                }
            ]
        }
        response = self.client.patch(reverse("event:event" , args=[2]), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)





    