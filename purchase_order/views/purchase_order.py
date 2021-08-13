import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest
from django.urls import reverse
import json
from django.utils import timezone
from collections import defaultdict
from enterprise.models import * 
from enterprise.serializers import *
from event.models import *
from event.serializers import *
from purchase_order.models import *
from purchase_order.serializers import *
from purchase_order.views.draft_purchase_order import *


class hello(APIView):
	'''
	For Welcoming :)
	'''
	def get(self, request):
		data = {
			"query": "Hello Purchase Order World"
		}
		return Response(data=data, status=status.HTTP_200_OK)

class entity_default_identification_list(APIView):

	def get(self, request):
		entity_default_identification_list = EntityPurchaseOrderDefaultIdentification.objects.all()
		serializers = EntityPurchaseOrderDefaultIdentificationSerializer(entity_default_identification_list, many=True)
		return Response(data=serializers.data, status=status.HTTP_200_OK)
	
	def post(self, request):
		data_list = request.data
		if(not isinstance(data_list, list)):
			data_list = [data_list]
		
		check = False
		for data in data_list:
			serializer = EntityPurchaseOrderDefaultIdentificationSerializer(data=data)
			if(serializer.is_valid()):
				serializer.save()
				check = True
		if(check):
			return Response(status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)
			
class entity_identification_list(APIView):

	def get(self, request):
		entity_identification_list = EntityIdentification.objects.all()
		serializers = EntityIdentificationSerializer(entity_identification_list, many=True)
		return Response(data=serializers.data, status=status.HTTP_200_OK)
	
	def post(self, request):
		data = request.data
		if(not isinstance(data, list)):
			data = [data]
		serializers = EntityIdentificationSerializer(data=data, many=True)
		if(serializers.is_valid()):
			serializers.save()
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		return Response(status=status.HTTP_201_CREATED)
		
class purchase_order(APIView):

	def get(self, request, purchase_order_id):
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		data_to_return = {}
		data_to_return["purchase_order_info"] = PurchaseOrderSerializer(purchase_order).data
		purchase_order_item_list = purchase_order.purchaseorderitem_set.all()
		item_list = []
		for purchase_order_item in purchase_order_item_list:
			item = {}
			item_info = PurchaseOrderItemSerializer(purchase_order_item).data
			item["item_info"] = item_info
			charge_list = purchase_order_item.purchaseorderitemcharge_set.all()
			item["item_charge"] = PurchaseOrderItemChargeSerializer(charge_list, many=True).data
			attribute_list = purchase_order_item.purchaseorderitemattribute_set.all()
			item["item_attribute"] = PurchaseOrderItemAttributeSerializer(attribute_list, many=True).data
			item_list.append(item)

		data_to_return["purchase_order_item_list"] = item_list

		purchase_order_buyer_information = PurchaseOrderBuyerInformation.objects.filter(purchase_order_id=purchase_order_id)
		data_to_return["purchase_order_buyer_information"] = PurchaseOrderBuyerInformationSerializer(purchase_order_buyer_information, many=True).data

		purchase_order_seller_information = PurchaseOrderSellerInformation.objects.filter(purchase_order_id=purchase_order_id)
		data_to_return["purchase_order_seller_information"] = PurchaseOrderSellerInformationSerializer(purchase_order_seller_information, many=True).data

		return Response(data=data_to_return, status=status.HTTP_200_OK)
	
	def patch(self, request, purchase_order_id):
		# Shouldn't be used anywhere for direct patching in real time
		# it is included just for testing purpose
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if(purchase_order.purchase_order_close_datetime):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		try:
			purchase_order_status = request.data["status"]
			purchase_order.status = purchase_order_status
			purchase_order.save()
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		return Response(status=status.HTTP_200_OK)
	
	def delete(self, request, purchase_order_id):
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if(purchase_order.purchase_order_close_datetime):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		purchase_order.purchase_order_close_datetime = timezone.now()
		purchase_order.save()
		return Response(status=status.HTTP_200_OK)	

class seller_purchase_order_response(APIView):
	'''
	For Seller to Accept or Decline the Purchase Order
	'''
	def patch(self, request, user_id, entity_id, purchase_order_id):
		self.user_id = user_id
		self.purchase_order_id = purchase_order_id

		try:
			self.user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		try:
			entity = Entity.objects.get(entity_id=entity_id)
		except Entity.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			self.purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
			purchase_order_data = PurchaseOrderSerializer(self.purchase_order).data
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id, deleted_datetime__isnull=True)
		except UserEntity.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Checking if the entity is a Seller
		if(purchase_order_data["seller_id"]!=entity_id):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Getting status from request data
		try:
			response_status = request.data["status"]
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# If current status is other than "issued" or the Purchase Order is closed
		if(self.purchase_order.status!="issued" or self.purchase_order.purchase_order_close_datetime):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Checking what type of seller response is

		# For declining
		if(response_status=="declined" and not self.purchase_order.closing_datetime_seller):
			self.seller_decline_purchase_order(request.data)
		
		# For accepting
		elif(response_status=="ongoing"):
			self.seller_accept_purchase_order()
		
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		return Response(status=status.HTTP_200_OK)
	
	def seller_accept_purchase_order(self):
		self.purchase_order.seller_acknowledgement_user_id = self.user
		self.purchase_order.seller_acknowledgement_datetime = timezone.now()
		self.purchase_order.status = "ongoing"
		self.purchase_order.save()

	def seller_decline_purchase_order(self, data):
		self.purchase_order.seller_acknowledgement_user_id = self.user
		self.purchase_order.seller_acknowledgement_datetime = timezone.now()
		self.purchase_order.closing_user_id_seller = self.user
		self.purchase_order.closing_comment_seller = data.get("closing_comment_seller", "")
		self.purchase_order.closing_datetime_seller = timezone.now()
		self.purchase_order.status = "declined"
		self.purchase_order.purchase_order_close_datetime = timezone.now()
		self.purchase_order.save()

class draft_purchase_order_shift_purchase_order(APIView):

	def post(self, request, purchase_order_id):
		#Check if this draft PO exists or not
		try:
			draft_purchase_order_object = DraftPurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except DraftPurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Getting Draft PO Data
		get_draft_purchase_order_request = HttpRequest()
		get_draft_purchase_order_request.method = "GET"
		get_draft_purchase_order_response = draft_purchase_order.as_view()(get_draft_purchase_order_request, purchase_order_id)
		if(get_draft_purchase_order_response.status_code!=200):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		data = get_draft_purchase_order_response.data

		# data = request.data
		data_to_return = {}

		# Checking if the shifting results in a reissued PO
		try:
			purchase_order_key_mapping_object = PurchaseOrderKeyMapping.objects.get(draft_purchase_order_id=purchase_order_id)
			parent_purchase_order_object_id = PurchaseOrderKeyMappingSerializer(purchase_order_key_mapping_object).data["purchase_order_id"]
			parent_purchase_order_object = PurchaseOrder.objects.get(draft_purchase_order_id=parent_purchase_order_object_id)

		except PurchaseOrderKeyMapping.DoesNotExist:
			purchase_order_key_mapping_object = None


		# Posting Purchase Order Info
		purchase_order_info = data.get("purchase_order_info")
		purchase_order_info["status"] = "issued"
		serializer = PurchaseOrderSerializer(data=purchase_order_info)
		if(serializer.is_valid()):
			serializer.save()
			data_to_return["purchase_order_info"] = serializer.data
			curr_purchase_order_id = serializer.data["purchase_order_id"]
			curr_purchase_order = PurchaseOrder.objects.get(purchase_order_id=curr_purchase_order_id)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Posting Purchase Order Item List
		purchase_order_item_list = data.get("purchase_order_item_list", [])
		# Checking for at least one item
		if(len(purchase_order_item_list)==0):
			curr_purchase_order.delete()
			return Response(status=status.HTTP_400_BAD_REQUEST)
		item_list = []
		for purchase_order_item in purchase_order_item_list:
			item = {}
			purchase_order_item_info = purchase_order_item.get("item_info", [])
			purchase_order_item_info["purchase_order_id"] = curr_purchase_order_id
			serializer = PurchaseOrderItemSerializer(data=purchase_order_item_info)
			if(serializer.is_valid()):
				serializer.save()
				item["item_info"] = serializer.data
				curr_purchase_order_line_item_id = serializer.data["purchase_order_line_item_id"]
				curr_purchase_order_item = PurchaseOrderItem.objects.get(purchase_order_line_item_id=curr_purchase_order_line_item_id)
			else:
				curr_purchase_order.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)
			item_attribute_list = []
			purchase_order_item_attribute_list = purchase_order_item.get("item_attribute", [])
			for purchase_order_item_attribute in purchase_order_item_attribute_list:
				purchase_order_item_attribute["purchase_order_line_item_id"] = curr_purchase_order_line_item_id
				serializer = PurchaseOrderItemAttributeSerializer(data=purchase_order_item_attribute)
				if(serializer.is_valid()):
					serializer.save()
					item_attribute_list.append(serializer.data)
				else:
					curr_purchase_order.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
			
			item["item_attribute"] = item_attribute_list

			item_charge_list = []
			purchase_order_item_charge_list = purchase_order_item.get("item_charge", [])
			for purchase_order_item_charge in purchase_order_item_charge_list:
				purchase_order_item_charge["purchase_order_line_item_id"] = curr_purchase_order_line_item_id
				serializer = PurchaseOrderItemChargeSerializer(data=purchase_order_item_charge)
				if(serializer.is_valid()):
					serializer.save()
					item_charge_list.append(serializer.data)
				else:
					curr_purchase_order.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
			
			item["item_charge"] = item_charge_list
			item_list.append(item)
		data_to_return["purchase_order_item_list"] = item_list

		# Posting Purchase Order Buyer Information
		purchase_order_buyer_information_list = data.get("purchase_order_buyer_information", [])
		buyer_information_list = []
		if(len(purchase_order_buyer_information_list)!=0):
			for purchase_order_buyer_information in purchase_order_buyer_information_list:
				purchase_order_buyer_information["purchase_order_id"] = curr_purchase_order_id
			serializers = PurchaseOrderBuyerInformationSerializer(data=purchase_order_buyer_information_list, many=True)
			if(serializers.is_valid()):
				serializers.save()
				buyer_information_list = serializers.data
			else:
				curr_purchase_order.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)

		data_to_return["purchase_order_buyer_information"] = buyer_information_list
		# Posting Purchase Order seller Information
		purchase_order_seller_information_list = data.get("purchase_order_seller_information", [])

		seller_information_list = []
		if(len(purchase_order_seller_information_list)!=0):
			for purchase_order_seller_information in purchase_order_seller_information_list:
				purchase_order_seller_information["purchase_order_id"] = curr_purchase_order_id

			serializers = PurchaseOrderSellerInformationSerializer(data=purchase_order_seller_information_list, many=True)
			if(serializers.is_valid()):
				serializers.save()
				seller_information_list = serializers.data
			else:
				curr_purchase_order.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)

		data_to_return["purchase_order_seller_information"] = seller_information_list

		if(purchase_order_key_mapping_object!=None):
			draft_purchase_order_object.delete()
			purchase_order_key_mapping_object.delete()
			parent_purchase_order_object.reissue_purchase_order_id = curr_purchase_order_id
			parent_purchase_order_object.reissue_draft_purchase_order_id = None
			parent_purchase_order_object.status = parent_purchase_order_object.status+"_and_reissued"
			parent_purchase_order_object.save()

		return Response(data=data_to_return, status=status.HTTP_201_CREATED)
	
class purchase_order_from_award(APIView):

	def get(self, request, award_id):
		try:
			award = Award.objects.get(award_id=award_id)
		except Award.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if(award.deleted_datetime):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		data_to_return = {}
		award_info = AwardSerializer(award).data
		self.buyer_id = award_info["buyer_id"]
		self.seller_id = award_info["seller_id"]
		purchase_order_info = self.po_info_from_award_info(award_info)
		data_to_return["purchase_order_info"] = purchase_order_info

		award_item_list = AwardItem.objects.filter(award_id=award_id)
		item_list = []
		for award_item in award_item_list:
			item = {}
			award_item_info = AwardItemSerializer(award_item).data
			
			# Storing event_line_item_id pf the item
			self.event_line_item_id = award_item_info["event_line_item_id"]
			
			# Getting item_info 
			purchase_order_item_info = self.po_item_info_from_award_item_info(award_item_info)
			item["item_info"] = purchase_order_item_info
			
			# Getting item_attribute
			item["item_attribute"] = self.po_item_attribute_from_award_item_attribute()
			
			# Getting item_charge
			award_line_item_id = award_item.award_line_item_id
			award_item_tax_list = AwardItemTax.objects.filter(award_line_item_id=award_line_item_id)
			award_item_charge_list_data = AwardItemTaxSerializer(award_item_tax_list, many=True).data
			item["item_charge"] = self.po_item_charge_from_award_item_charge(award_item_charge_list_data)
			item_list.append(item)

		data_to_return["purchase_order_item_list"] = item_list

		# Getting po_buyer_information
		data_to_return["purchase_order_buyer_information"] = self.po_entity_information(entity_type="buyer", entity_id=self.buyer_id)

		# Getting po_seller_information
		data_to_return["purchase_order_seller_information"] = self.po_entity_information(entity_type="seller", entity_id=self.seller_id)
	
		return Response(data=data_to_return, status=status.HTTP_200_OK)
	
	def po_info_from_award_info(self, award_info):
		# Making purchase_order_info from award_info
		purchase_order_info = {}
		purchase_order_info["event_id"] = award_info["event_id"]
		purchase_order_info["buyer_id"] = award_info["buyer_id"]
		purchase_order_info["buyer_entity_name"] = Entity.objects.get(entity_id=award_info["buyer_id"]).entity_name
		purchase_order_info["seller_id"] = award_info["seller_id"]
		purchase_order_info["seller_entity_name"] = Entity.objects.get(entity_id=award_info["seller_id"]).entity_name
		purchase_order_info["purchase_order_discount_percentage"] = award_info["bulk_discount_percentage"]
		return purchase_order_info
	
	def po_item_info_from_award_item_info(self, award_item_info):
		# Making purchase_order_item_info from award_item_info
		purchase_order_item_info = {}
		event_item = EventItem.objects.get(event_line_item_id=self.event_line_item_id)
		event = event_item.event_id
		enterprsie = event.enterprise_id
		event_item_data = EventItemSerializer(event_item).data
		purchase_order_item_info["item_id"] = event_item_data["item_id"]
		purchase_order_item_info["buyer_item_description"] = event_item.description
		purchase_order_item_info["buyer_item_id"] = event_item_data["buyer_item_id"]
		try:
			buyer_item = BuyerItem.objects.get(enterprise_id=enterprsie.enterprise_id, buyer_item_id=event_item_data["buyer_item_id"])
			purchase_order_item_info["buyer_item_name"] = buyer_item.buyer_item_name
		except BuyerItem.DoesNotExist:
			pass
		purchase_order_item_info["currency_code"] = award_item_info["currency_code"]
		purchase_order_item_info["measurement_unit_id"] = award_item_info["measurement_unit_id"]
		purchase_order_item_info["rate"] = award_item_info["price"]
		purchase_order_item_info["quantity"] = award_item_info["quantity_awarded"]
		purchase_order_item_info["total_order_value"] = award_item_info["total_amount"]
		return purchase_order_item_info
	
	def po_item_attribute_from_award_item_attribute(self):
		# Making po_item_attribute from event_item
		po_item_attribute = []
		event_item_attribute_list = EventItemAttribute.objects.filter(event_line_item_id=self.event_line_item_id)
		event_item_attribute_list_data = EventItemAttributeSerializer(event_item_attribute_list, many=True).data
		for attribute in event_item_attribute_list_data:
			attribute_data = {}
			attribute_data["attribute_id"] = attribute["attribute_id"]
			attribute_data["attribute_value"] = attribute["attribute_value"]
			po_item_attribute.append(attribute_data)
		return po_item_attribute
	
	def po_item_charge_from_award_item_charge(self, award_item_charge_list_data):
		# Making po_item_charge from award_item_charge_list_data
		po_item_charge = []
		for award_item_charge in award_item_charge_list_data:
			purchase_order_item_charge = {}
			purchase_order_item_charge["charge_name"] = award_item_charge["tax_name"]
			purchase_order_item_charge["charge_percentage"] = award_item_charge["value"]
			po_item_charge.append(purchase_order_item_charge)
		return po_item_charge
	
	def po_entity_information(self, entity_type, entity_id):
		# Getting default EntityPurchaseOrderDefaultIdentification for Entity
		entity_purchase_default_identification_id_list = EntityPurchaseOrderDefaultIdentification.objects.filter(entity_id=entity_id).values_list("identification_id", flat=True)
		po_entity_info_list = []
		for identification_id in entity_purchase_default_identification_id_list:
			identification_data = {}
			entity_identification_object = EntityIdentification.objects.get(identification_id=identification_id)
			identification_data[entity_type+"_id"] = entity_id
			identification_data["identification_id"] = entity_identification_object.identification_id
			identification_data["identification_name"] = entity_identification_object.identification_name
			identification_data["identification_value"] = entity_identification_object.identification_value
			po_entity_info_list.append(identification_data)

		return po_entity_info_list
			
class purchase_order_accept_termination(APIView):

	def patch(self, request, user_id, entity_id, purchase_order_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			entity = Entity.objects.get(entity_id=entity_id)
		except Entity.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
			purchase_order_data = PurchaseOrderSerializer(purchase_order).data
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id, deleted_datetime__isnull=True)
		except UserEntity.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Checking if the Purchase Order has already been closed
		if(purchase_order.purchase_order_close_datetime or purchase_order.status != "termination_request"):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		# Checking if the acceptance is being done by Buyer or Seller
		buyer = False
		seller = False
		if(purchase_order_data["buyer_id"]==entity_id):
			# Checking if the entity is the buyer
			buyer = True
		elif(purchase_order_data["seller_id"]==entity_id):
			# Now checking if the entity is the seller
			seller = True
		
		if(buyer and not seller):
			# Checking the fields
			closing_user_seller_id = purchase_order_data["closing_user_id_seller"]
			try:
				closing_user_seller_id = User.objects.get(user_id=closing_user_seller_id)
			except User.DoesNotExist:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			closing_datetime_seller = purchase_order_data["closing_datetime_seller"]
			if(not closing_datetime_seller):
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			# All checks passed
			purchase_order.closing_user_id_buyer = user
			purchase_order.closing_comment_buyer = request.data.get("closing_comment_buyer", "")
			purchase_order.closing_datetime_buyer = timezone.now()
			purchase_order.save()
		
		elif(not buyer and seller):
			# Checking the fields
			closing_user_buyer_id = purchase_order_data["closing_user_id_buyer"]
			try:
				closing_user_buyer_id = User.objects.get(user_id=closing_user_buyer_id)
			except User.DoesNotExist:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			closing_datetime_buyer = purchase_order_data["closing_datetime_buyer"]
			if(not closing_datetime_buyer):
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			# All checks passed
			purchase_order.closing_user_id_seller = user
			purchase_order.closing_comment_seller = request.data.get("closing_comment_seller", "")
			purchase_order.closing_datetime_seller = timezone.now()
			purchase_order.save()

		else:
			# The entity is neither this PO's seller nor buyer
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# All checks have passed and now the PO should be closed
		purchase_order.status = "closed"
		purchase_order.purchase_order_close_datetime = timezone.now()
		purchase_order.save()
		return Response(status=status.HTTP_200_OK)

class award_status_from_purchase_order(APIView):
	
	def get(self, request, purchase_order_id):
		# For getting the award status from purchase_order_id
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		purchase_order_data = PurchaseOrderSerializer(purchase_order).data
		seller_id = purchase_order_data["seller_id"]
		event_id = purchase_order_data["event_id"]
		# Getting all the awards for this seller and event
		award_id_list = list(Award.objects.filter(event_id=event_id, seller_id=seller_id).values_list("award_id", flat=True))

		# Checking if there is atleast one award or not
		if(len(award_id_list)==0):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		# Here atleast one award exists

		# Getting latest award (basically award with max award_id)
		lateast_award_id = max(award_id_list)
		latest_award = Award.objects.get(award_id=lateast_award_id)
		data_to_return = {}
		data_to_return["deal_status"] = latest_award.deal_status
		return Response(data=data_to_return, status=status.HTTP_200_OK)

# Getting all Latest POs for an event of all sellers 
class purchase_order_list(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        purchase_order_list = PurchaseOrder.objects.filter(event_id=event_id, purchase_order_close_datetime__isnull=True)
        seller_id_list = defaultdict(lambda : 0)
        for current_purchase_order in purchase_order_list:
            seller_id_list[current_purchase_order.seller_id] = max(seller_id_list[current_purchase_order.seller_id], current_purchase_order.purchase_order_id)
        purchase_order_list = []
        for seller in seller_id_list.keys():
            current_purchase_order_id = PurchaseOrder.objects.get(purchase_order_id = seller_id_list[seller])
            purchase_order_list.append(current_purchase_order_id)
        
        data = []
        for current_purchase_order in purchase_order_list:
            purchase_request = HttpRequest()
            purchase_request.method = "GET"
            response_purchase_order = purchase_order.as_view()(purchase_request,current_purchase_order.purchase_order_id)
            if(response_purchase_order.status_code == 200):
                data.append(response_purchase_order.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(data=data, status=status.HTTP_200_OK)

class latest_purchase_order(APIView):
    def get(self, request, event_id, seller_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            seller = Seller.objects.get(seller_id=seller_id)
        except Seller.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            event_item_seller = EventItemSeller.objects.get(event_id=event_id, seller_id=seller_id)
        except EventItemSeller.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        purchase_order_list = PurchaseOrder.objects.filter(event_id=event_id, seller_id=seller_id)
        purchase_order_list_info = PurchaseOrderSerializer(purchase_order_list,many=True).data
        max_purchase_order_id = 0
        for current_purchase_order in purchase_order_list_info:
            max_purchase_order_id = max(max_purchase_order_id, current_purchase_order["purchase_order_id"])
        
        request = HttpRequest()
        request.method = "GET"
        data = {}
        response_purchase_order_info = purchase_order.as_view()(request,max_purchase_order_id)
        if(response_purchase_order_info.status_code == 200):
            data = response_purchase_order_info.data
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(data=data, status=status.HTTP_200_OK)

class purchase_order_termination_request(APIView):
    def patch(self, request, user_id, entity_id, purchase_order_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id)
        except UserEntity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
            serializer = PurchaseOrderSerializer(purchase_order)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # checking if PO status is Ongoing 
        if(purchase_order.status != "ongoing" or purchase_order.status == "termination_request"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # if buyer is requesting termination
        if(entity_id == serializer.data["buyer_id"]):
            purchase_order.closing_user_id_buyer = user
            purchase_order.closing_comment_buyer =  request.data.get("closing_comment_buyer","")
            purchase_order.closing_datetime_buyer = timezone.now()
            purchase_order.save()
        # if seller is requesting termination
        elif(entity_id == serializer.data["seller_id"]):
            purchase_order.closing_user_id_seller = user
            purchase_order.closing_comment_seller =  request.data.get("closing_comment_seller","")
            purchase_order.closing_datetime_seller = timezone.now()
            purchase_order.save()
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        #changing status to termination request
        purchase_order.status = "termination_request"
        purchase_order.save()
        return Response(status=status.HTTP_200_OK)

class purchase_order_undo_termination_request(APIView):
    def patch(self, request, user_id, entity_id, purchase_order_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id)
        except UserEntity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        try:
            purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
            serializer = PurchaseOrderSerializer(purchase_order)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
		# checking if termionation request is accepted or not
        if(purchase_order.status == "closed"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # if buyer is requesting termination
        if(entity_id == serializer.data["buyer_id"]):
            if(not(purchase_order.closing_user_id_seller)):
                purchase_order.closing_user_id_buyer = None
                purchase_order.closing_comment_buyer =  ""
                purchase_order.closing_datetime_buyer = None
                purchase_order.save()
            else:
                return Response(data="Not allowed", status=status.HTTP_400_BAD_REQUEST)
        # if seller is requesting termination
        elif(entity_id == serializer.data["seller_id"]):
            if(not(purchase_order.closing_user_id_buyer)):
                purchase_order.closing_user_id_seller = None
                purchase_order.closing_comment_seller =  ""
                purchase_order.closing_datetime_seller = None
                purchase_order.save()
            else:
                return Response(data="Not allowed", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # changing status to ongonig
        purchase_order.status = "ongoing"
        purchase_order.save()

        return Response(status=status.HTTP_200_OK)

class rescind_purchase_order(APIView):
    def patch(self, request, user_id, purchase_order_id):
        try:
            purchase_order_user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
            serializer = PurchaseOrderSerializer(purchase_order)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            user_entity = UserEntity.objects.get(user_id=user_id, entity_id=purchase_order.buyer_id_id)
        except UserEntity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if(purchase_order.status != "issued"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        purchase_order.status = "rescind"
        purchase_order.closing_user_id_buyer = purchase_order_user
        purchase_order.closing_comment_buyer = request.data.get("closing_comment_buyer", "")
        purchase_order.closing_datetime_buyer = timezone.now()
        purchase_order.purchase_order_close_datetime = timezone.now()
        purchase_order.save()
        return Response(status=status.HTTP_200_OK)

class event_purchase_order_list(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        purchase_order_list = PurchaseOrder.objects.filter(event_id=event_id)        
        request = HttpRequest()
        request.method = "GET"
        data = []
        for current_purchase_order in purchase_order_list:
            response_purchase_order = purchase_order.as_view()(request,current_purchase_order.purchase_order_id)
            if(response_purchase_order.status_code == 200):
                data.append(response_purchase_order.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=data, status=status.HTTP_200_OK)