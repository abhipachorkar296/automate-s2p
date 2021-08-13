import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.http import HttpRequest
from django.db import transaction
import json
from decimal import *
from django.utils import timezone
from collections import defaultdict
from enterprise.models import * 
from enterprise.serializers import *
from event.models import *
from event.serializers import *
from purchase_order.models import *
from purchase_order.serializers import *
from invoice.models import *
from invoice.serializers import *
from payment.models import *
from goods_receipt.models import *
from quality_check.models import *
from invoice.views.draft_invoice import draft_invoice
from django.conf import settings

DECIMAL_COMPARISON_PRECISION = settings.DECIMAL_COMPARISON_PRECISION

def purchase_order_item_max_pending_quantity(purchase_order_line_item_id):
	'''
	Function for getting max_pending_quantity of a purchase order item
	'''
	purchase_order_item = PurchaseOrderItem.objects.get(purchase_order_line_item_id=purchase_order_line_item_id)
	purchase_order_item_info = PurchaseOrderItemSerializer(purchase_order_item).data

	# Now implementing the calculation of max_pending_quantity
	purchase_order_quantity = purchase_order_item_info["max_acceptable_quantity"]

	# Getting all the present invoice_line_item_id against this purchase_order_line_item
	all_invoice_line_item_id_quantity_invoiced_list = list(InvoiceItem.objects.filter(purchase_order_line_item_id=purchase_order_line_item_id).values_list("invoice_line_item_id", "quantity_invoiced"))
	# Extracting the invoice_line_item_id list 
	invoice_line_item_id_list = [x[0] for x in all_invoice_line_item_id_quantity_invoiced_list]
	
	# Getting all the goods_receipt_entry_id and receipt_quantity_rejected against each ids in invoice_line_item_id_list
	all_goods_receipt_entry_id_receipt_quantity_accepted_list = list(GoodsReceipt.objects.filter(invoice_line_item_id__in=invoice_line_item_id_list).values_list("goods_receipt_entry_id", "receipt_quantity_accepted", "invoice_line_item_id"))
	# Extracting the goods_receipt_entry_id list 
	goods_receipt_entry_id_list = [x[0] for x in all_goods_receipt_entry_id_receipt_quantity_accepted_list]
	# Getting all the receipt_quantity_accetpted for this item in grn
	total_receipt_quantity_accepted = sum([x[1] for x in all_goods_receipt_entry_id_receipt_quantity_accepted_list])
	
	# Getting all the quantity_rejected for the quality checks corresponding to 
	# goods receipt in goods_receipt_entry_id_list
	total_quality_check_quantity_rejected = sum(list(QualityCheck.objects.filter(goods_receipt_entry_id__in=goods_receipt_entry_id_list).values_list("quantity_rejected", flat=True)))

	# Getting all the invoice ids with Goods Receipt present against them
	invoice_id_with_grn_list = [x[2] for x in all_goods_receipt_entry_id_receipt_quantity_accepted_list]
	# Getting all the invoiced_quantity for invoices without grn
	total_invoiced_quantity_without_grn = sum([x[1] for x in all_invoice_line_item_id_quantity_invoiced_list if x[0] not in set(invoice_id_with_grn_list)])
	# So the max_pending_quantity will be equal to
	max_pending_quantity = round(Decimal(purchase_order_quantity)-Decimal(total_invoiced_quantity_without_grn)-Decimal(total_receipt_quantity_accepted)+Decimal(total_quality_check_quantity_rejected), DECIMAL_COMPARISON_PRECISION)
	
	return max_pending_quantity

def purchase_order_item_pending_quantity(purchase_order_line_item_id):
	'''
	Function for getting pending_quantity of a purchase order item
	'''
	purchase_order_item = PurchaseOrderItem.objects.get(purchase_order_line_item_id=purchase_order_line_item_id)
	purchase_order_item_info = PurchaseOrderItemSerializer(purchase_order_item).data

	# Now implementing the calculation of pending_quantity
	purchase_order_quantity = purchase_order_item_info["quantity"]

	# Getting all the present invoice_line_item_id against this purchase_order_line_item
	all_invoice_line_item_id_quantity_invoiced_list = list(InvoiceItem.objects.filter(purchase_order_line_item_id=purchase_order_line_item_id).values_list("invoice_line_item_id", "quantity_invoiced"))
	# Extracting the invoice_line_item_id list 
	invoice_line_item_id_list = [x[0] for x in all_invoice_line_item_id_quantity_invoiced_list]
	
	# Getting all the goods_receipt_entry_id and receipt_quantity_rejected against each ids in invoice_line_item_id_list
	all_goods_receipt_entry_id_receipt_quantity_accepted_list = list(GoodsReceipt.objects.filter(invoice_line_item_id__in=invoice_line_item_id_list).values_list("goods_receipt_entry_id", "receipt_quantity_accepted", "invoice_line_item_id"))
	# Extracting the goods_receipt_entry_id list 
	goods_receipt_entry_id_list = [x[0] for x in all_goods_receipt_entry_id_receipt_quantity_accepted_list]
	# Getting all the receipt_quantity_accetpted for this item in grn
	total_receipt_quantity_accepted = sum([x[1] for x in all_goods_receipt_entry_id_receipt_quantity_accepted_list])
	
	# Getting all the quantity_rejected for the quality checks corresponding to 
	# goods receipt in goods_receipt_entry_id_list
	total_quality_check_quantity_rejected = sum(list(QualityCheck.objects.filter(goods_receipt_entry_id__in=goods_receipt_entry_id_list).values_list("quantity_rejected", flat=True)))

	# Getting all the invoice ids with Goods Receipt present against them
	invoice_id_with_grn_list = [x[2] for x in all_goods_receipt_entry_id_receipt_quantity_accepted_list]
	# Getting all the invoiced_quantity for invoices without grn
	total_invoiced_quantity_without_grn = sum([x[1] for x in all_invoice_line_item_id_quantity_invoiced_list if x[0] not in set(invoice_id_with_grn_list)])

	# So the pending_quantity will be equal to
	pending_quantity = round(Decimal(purchase_order_quantity)-Decimal(total_invoiced_quantity_without_grn)-Decimal(total_receipt_quantity_accepted)+Decimal(total_quality_check_quantity_rejected), DECIMAL_COMPARISON_PRECISION)

	return pending_quantity

def invoice_item_amount_from_quantity(invoice_line_item_id, quantity):
	'''
	Function for calculating the amount from invoice line item given quantity
	'''
	invoice_line_item = InvoiceItem.objects.get(invoice_line_item_id=invoice_line_item_id)
	invoice = invoice_line_item.invoice_id
	rate = invoice_line_item.rate
	all_taxes_percentage_sum = round(Decimal(sum(list(invoice_line_item.invoiceitemcharge_set.all().values_list("charge_percentage", flat=True)))), DECIMAL_COMPARISON_PRECISION)
	shipping_per_unit = invoice_line_item.shipping_per_unit
	invoice_discount_percentage = invoice.invoice_discount_percentage
	amount = round(Decimal((1+Decimal("0.01")*all_taxes_percentage_sum-Decimal("0.01")*invoice_discount_percentage)*quantity*rate + quantity*shipping_per_unit), DECIMAL_COMPARISON_PRECISION)
	return amount

def invoice_item_accepted_quantity(invoice_line_item_id):
	'''
	Function for getting all the accepted quantity of the invoice line item
	'''
	# Getting all the goods_receipt_entry_id and receipt_quantity_rejected against invoice_line_item_id
	all_goods_receipt_entry_id_receipt_quantity_accepted_list = list(GoodsReceipt.objects.filter(invoice_line_item_id=invoice_line_item_id).values_list("goods_receipt_entry_id", "receipt_quantity_accepted"))
	# Extracting the goods_receipt_entry_id list 
	goods_receipt_entry_id_list = [x[0] for x in all_goods_receipt_entry_id_receipt_quantity_accepted_list]
	# Getting all the receipt_quantity_accetpted for this item in grn
	total_receipt_quantity_accepted = sum([x[1] for x in all_goods_receipt_entry_id_receipt_quantity_accepted_list])
	
	# Getting all the quantity_rejected for the quality checks corresponding to 
	# goods receipt in goods_receipt_entry_id_list
	total_quality_check_quantity_rejected = sum(list(QualityCheck.objects.filter(goods_receipt_entry_id__in=goods_receipt_entry_id_list).values_list("quantity_rejected", flat=True)))

	# Getting all the invoice item accepted quantity 
	total_accepted_invoice_item_quantity = total_receipt_quantity_accepted - total_quality_check_quantity_rejected
	return total_accepted_invoice_item_quantity

class invoice(APIView):

	def get(self, request, invoice_id):
		try:
			invoice = Invoice.objects.get(invoice_id=invoice_id)
		except Invoice.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		data_to_return = {}
		data_to_return["invoice_info"] = InvoiceSerializer(invoice).data
		invoice_item_list = invoice.invoiceitem_set.all()
		item_list = []
		# Getting all the invoice items along with their charge and attribute
		for invoice_item in invoice_item_list:
			item = {}
			item_info = InvoiceItemSerializer(invoice_item).data
			item["item_info"] = item_info
			charge_list = invoice_item.invoiceitemcharge_set.all()
			item["item_charge"] = InvoiceItemChargeSerializer(charge_list, many=True).data
			attribute_list = invoice_item.invoiceitemattribute_set.all()
			item["item_attribute"] = InvoiceItemAttributeSerializer(attribute_list, many=True).data
			item_list.append(item)

		data_to_return["invoice_item_list"] = item_list

		invoice_buyer_information = InvoiceBuyerInformation.objects.filter(invoice_id=invoice_id)
		data_to_return["invoice_buyer_information"] = InvoiceBuyerInformationSerializer(invoice_buyer_information, many=True).data

		invoice_seller_information = InvoiceSellerInformation.objects.filter(invoice_id=invoice_id)
		data_to_return["invoice_seller_information"] = InvoiceSellerInformationSerializer(invoice_seller_information, many=True).data

		return Response(data=data_to_return, status=status.HTTP_200_OK)
	
	def patch(self, request, invoice_id):
		# This method is for editing a provisional invoice
		try:
			invoice = Invoice.objects.get(invoice_id=invoice_id)
		except Invoice.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		'''
		Validating the pre conditions for PATCH request
		'''
		# Invoice Type is Goods
		if(invoice.invoice_type!="goods"):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Checking the invoice status
		if(invoice.status not in ["ongoing", "termination_requested"]):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Check whether the incoming seller_invoiced_id is blank or not
		new_invoice_info = request.data.get("invoice_info", {})
		seller_invoice_id = new_invoice_info.get("seller_invoice_id", "")
		if(seller_invoice_id==""):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		invoice_item_id_list = invoice.invoiceitem_set.all().values_list("invoice_line_item_id", flat=True) # All invoice_line_item_id list of this invoice
		new_invoice_item_list = request.data.get("invoice_item_list", [])
		new_invoice_item_id_list = set()

		# Checking if the item coming in the data is of this invoice only or not and having
		# invoiced_quantity same as the original one
		for invoice_item_data in new_invoice_item_list:
			item_info = invoice_item_data.get("item_info", {})
			if(item_info=={}):
				# Item is there but the item_info is not there in the request data coming
				# which means the data is not coming in the valid format, 
				# so it is a BAD_REQUEST
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			# Checking if the invoice_line_item_id in the incoming data exists in our original invoice or not
			curr_invoice_line_item_id = item_info.get("invoice_line_item_id")
			if(curr_invoice_line_item_id not in invoice_item_id_list):
				# This item does not exist in the original invoice
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			new_invoice_item_id_list.add(int(curr_invoice_line_item_id))
			# Checking whether the quantity_invoiced matches the original 
			# quantity_invoiced for this item
			invoice_item = InvoiceItem.objects.get(invoice_line_item_id=curr_invoice_line_item_id)
			if(round(Decimal(invoice_item.quantity_invoiced), DECIMAL_COMPARISON_PRECISION)!=round(Decimal(item_info.get("quantity_invoiced", -1)), DECIMAL_COMPARISON_PRECISION)):
				return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Check if any item is missing or not in the data coming
		# Above check determines that the invoice_line_item coming in data is 
		# present in this invoice only, So for checking the missing invoice_item,
		# only the number of unique items coming in the data needs to be checked
		if(len(invoice_item_id_list)!=len(new_invoice_item_list)):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		# Checking if no payment exists for any invoice_line_item
		for curr_invoice_line_item_id in invoice_item_id_list:
			invoice_item_payment_exists = InvoiceItemPayment.objects.filter(invoice_line_item_id=curr_invoice_line_item_id).exists()
			if(invoice_item_payment_exists):
				# Here it means that there is at least one payment existing for this item
				return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# All checks have passed
		# Now direct patch can be implemented
		# Patching Invoice Info
		try:
			with transaction.atomic():
				new_invoice_info = request.data.get("invoice_info")
				new_invoice_info["invoice_id"] = invoice_id
				serializer = InvoiceSerializer(invoice, new_invoice_info, partial=True)
				if(serializer.is_valid()):
					serializer.save()
				else:
					# return Response(status=status.HTTP_400_BAD_REQUEST)
					raise ValidationError()
				
				# Patching item_list
				for curr_invoice_item in new_invoice_item_list:
					# It has been already checked above that this item exists in the original invoice
					# Patching the item info
					new_item_info = curr_invoice_item.get("item_info")
					invoice_line_item_id = new_item_info.get("invoice_line_item_id")
					orig_item = InvoiceItem.objects.get(invoice_line_item_id=invoice_line_item_id)
					orig_item_accepted_quantity = invoice_item_accepted_quantity(invoice_line_item_id)
					serializer = InvoiceItemSerializer(orig_item, new_item_info, partial=True)
					if(serializer.is_valid()):
						serializer.save()
						curr_invoice_line_item_id = serializer.data["invoice_line_item_id"]
					else:
						# return Response(status=status.HTTP_400_BAD_REQUEST)
						raise ValidationError()
					
					new_item_attribute = curr_invoice_item.get("item_attribute")
					for attribute_data in new_item_attribute:
						attribute_data["invoice_line_item_id"] = curr_invoice_line_item_id
					orig_item_attribute = orig_item.invoiceitemattribute_set.all()
					orig_item_attribute.delete()
					serializers = InvoiceItemAttributeSerializer(data=new_item_attribute, many=True)
					if(serializers.is_valid()):
						serializers.save()
					else:
						# return Response(status=status.HTTP_400_BAD_REQUEST)
						raise ValidationError()

					new_item_charge = curr_invoice_item.get("item_charge")
					for charge_data in new_item_charge:
						charge_data["invoice_line_item_id"] = curr_invoice_line_item_id
					orig_item_charge = orig_item.invoiceitemcharge_set.all()
					orig_item_charge.delete()
					serializers = InvoiceItemChargeSerializer(data=new_item_charge, many=True)
					if(serializers.is_valid()):
						serializers.save()
					else:
						# return Response(status=status.HTTP_400_BAD_REQUEST)
						raise ValidationError()
				
					# Updating the amount_due
					orig_item = InvoiceItem.objects.get(invoice_line_item_id=invoice_line_item_id)
					orig_item.amount_due = invoice_item_amount_from_quantity(invoice_line_item_id, orig_item_accepted_quantity)
					orig_item.save()
				
				# Patching Buyer Information if needed
				new_invoice_buyer_information = request.data.get("invoice_buyer_information", [])
				orig_invoice_buyer_information = invoice.invoicebuyerinformation_set.all()
				orig_invoice_buyer_information.delete()
				for new_invoice_buyer_info_data in new_invoice_buyer_information:
					new_invoice_buyer_info_data["invoice_id"] = invoice_id
				serializers = InvoiceBuyerInformationSerializer(data=new_invoice_buyer_information, many=True)
				if(serializers.is_valid()):
					serializers.save()
				else:
					# return Response(status=status.HTTP_400_BAD_REQUEST)
					raise ValidationError()

				# Patching Seller Information if needed
				new_invoice_seller_information = request.data.get("invoice_seller_information", [])
				orig_invoice_seller_information = invoice.invoicesellerinformation_set.all()
				orig_invoice_seller_information.delete()
				for new_invoice_seller_info_data in new_invoice_seller_information:
					new_invoice_seller_info_data["invoice_id"] = invoice_id
				serializers = InvoiceSellerInformationSerializer(data=new_invoice_seller_information, many=True)
				if(serializers.is_valid()):
					serializers.save()
				else:
					# return Response(status=status.HTTP_400_BAD_REQUEST)
					raise ValidationError()
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		return Response(status=status.HTTP_200_OK)
	
	def delete(self, request, invoice_id):
		try:
			invoice = Invoice.objects.get(invoice_id=invoice_id)
		except Invoice.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if(invoice.invoice_close_datetime!=None):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		invoice.invoice_close_datetime = timezone.now()
		invoice.save()
		return Response(status=status.HTTP_200_OK)
		
class draft_invoice_shift_invoice(APIView):

	def post(self, request, invoice_id):
		# Check if this draft Invoice exists or not
		try:
			draft_invoice_object = DraftInvoice.objects.get(invoice_id=invoice_id)
		except DraftInvoice.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Getting Draft Invoice Data
		get_draft_invoice_request = HttpRequest()
		get_draft_invoice_request.method = "GET"
		get_draft_invoice_response = draft_invoice.as_view()(get_draft_invoice_request, invoice_id)
		if(get_draft_invoice_response.status_code!=200):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		data = get_draft_invoice_response.data

		#data = request.data
		data_to_return = {}

		# Posting Invoice Info
		invoice_info = data.get("invoice_info", {})
		invoice_info["status"] = "issued"
		serializer = InvoiceSerializer(data=invoice_info)
		if(serializer.is_valid()):
			serializer.save()
			data_to_return["invoice_info"] = serializer.data
			curr_invoice_id = serializer.data["invoice_id"]
			curr_invoice = Invoice.objects.get(invoice_id=curr_invoice_id)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Posting Invoice Item List
		invoice_item_list = data.get("invoice_item_list", [])
		# Checking for at least one item
		if(len(invoice_item_list)==0):
			curr_invoice.delete()
			return Response(status=status.HTTP_400_BAD_REQUEST)
			
		item_list = []
		for invoice_item in invoice_item_list:
			item = {}
			invoice_item_info = invoice_item.get("item_info", {})
			curr_purchase_order_line_item_id = invoice_item_info.get("purchase_order_line_item_id")
			# Checking if this curr_purchase_order_line_item_id exists
			try:
				purchase_order_line_item = PurchaseOrderItem.objects.get(purchase_order_line_item_id=curr_purchase_order_line_item_id)
			except PurchaseOrderItem.DoesNotExist:
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			# Checking if the invoice_quantity is less than max_pending_quantity
			curr_invoice_item_max_pending_quantity = purchase_order_item_max_pending_quantity(curr_purchase_order_line_item_id)
			if(round(Decimal(invoice_item_info.get("quantity_invoiced", Decimal("Inf"))), DECIMAL_COMPARISON_PRECISION) > curr_invoice_item_max_pending_quantity):
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)

			invoice_item_info["invoice_id"] = curr_invoice_id
			serializer = InvoiceItemSerializer(data=invoice_item_info)
			if(serializer.is_valid()):
				serializer.save()
				item["item_info"] = serializer.data
				curr_invoice_line_item_id = serializer.data["invoice_line_item_id"]
				curr_invoice_item = InvoiceItem.objects.get(invoice_line_item_id=curr_invoice_line_item_id)
			else:
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)
			item_attribute_list = []
			invoice_item_attribute_list = invoice_item.get("item_attribute", [])
			for invoice_item_attribute in invoice_item_attribute_list:
				invoice_item_attribute["invoice_line_item_id"] = curr_invoice_line_item_id
				serializer = InvoiceItemAttributeSerializer(data=invoice_item_attribute)
				if(serializer.is_valid()):
					serializer.save()
					item_attribute_list.append(serializer.data)
				else:
					curr_invoice.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
			
			item["item_attribute"] = item_attribute_list

			item_charge_list = []
			invoice_item_charge_list = invoice_item.get("item_charge", [])
			for invoice_item_charge in invoice_item_charge_list:
				invoice_item_charge["invoice_line_item_id"] = curr_invoice_line_item_id
				serializer = InvoiceItemChargeSerializer(data=invoice_item_charge)
				if(serializer.is_valid()):
					serializer.save()
					item_charge_list.append(serializer.data)
				else:
					curr_invoice.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
			
			item["item_charge"] = item_charge_list
			item_list.append(item)
		data_to_return["invoice_item_list"] = item_list

		# Posting Invoice Buyer Information
		invoice_buyer_information_list = data.get("invoice_buyer_information", [])
		buyer_information_list = []
		if(len(invoice_buyer_information_list)!=0):
			for invoice_buyer_information in invoice_buyer_information_list:
				invoice_buyer_information["invoice_id"] = curr_invoice_id
			serializers = InvoiceBuyerInformationSerializer(data=invoice_buyer_information_list, many=True)
			if(serializers.is_valid()):
				serializers.save()
				buyer_information_list = serializers.data
			else:
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)

		data_to_return["invoice_buyer_information"] = buyer_information_list
		# Posting Invoice seller Information
		invoice_seller_information_list = data.get("invoice_seller_information", [])

		seller_information_list = []
		if(len(invoice_seller_information_list)!=0):
			for invoice_seller_information in invoice_seller_information_list:
				invoice_seller_information["invoice_id"] = curr_invoice_id

			serializers = InvoiceSellerInformationSerializer(data=invoice_seller_information_list, many=True)
			if(serializers.is_valid()):
				serializers.save()
				seller_information_list = serializers.data
			else:
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)

		data_to_return["invoice_seller_information"] = seller_information_list

		# Deleting the draft invoice
		draft_invoice_object.delete()
		return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class invoice_from_purchase_order(APIView):

	def get(self, request, purchase_order_id):
		# Making invoice draft object with purchase order data
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if(purchase_order.purchase_order_close_datetime):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		data_to_return = {}
		purchase_order_info = PurchaseOrderSerializer(purchase_order).data
		self.purchase_order_id = purchase_order_id
		self.buyer_id = purchase_order_info["buyer_id"]
		self.seller_id = purchase_order_info["seller_id"]
		invoice_info = self.invoice_info_from_purchase_order_info(purchase_order_info)
		data_to_return["invoice_info"] = invoice_info

		purchase_order_item_list = PurchaseOrderItem.objects.filter(purchase_order_id=purchase_order_id)
		item_list = []
		for purchase_order_item in purchase_order_item_list:
			item = {}
			purchase_order_item_info = PurchaseOrderItemSerializer(purchase_order_item).data
			
			# Storing purchase_order_line_item_id pf the item
			self.purchase_order_line_item_id = purchase_order_item_info["purchase_order_line_item_id"]
			
			# Getting item_info 
			invoice_item_info = self.invoice_item_info_from_purchase_order_item_info(purchase_order_item_info)
			item["item_info"] = invoice_item_info
			
			# Getting item_attribute
			item["item_attribute"] = self.invoice_item_attribute_from_purchase_order_item_attribute(self.purchase_order_line_item_id)
			
			# Getting item_charge
			item["item_charge"] = self.invoice_item_charge_from_purchase_order_item_charge(self.purchase_order_line_item_id)
			item_list.append(item)

		data_to_return["invoice_item_list"] = item_list

		# Getting invoice_buyer_information
		data_to_return["invoice_buyer_information"] = self.invoice_buyer_information_from_purchase_order_buyer_information()

		# Getting invoice_seller_information
		data_to_return["invoice_seller_information"] = self.invoice_seller_information_from_purchase_order_seller_information()
	
		return Response(data=data_to_return, status=status.HTTP_200_OK)
	
	def invoice_info_from_purchase_order_info(self, purchase_order_info):
		# Making invoice_info from purchase_order_info
		invoice_info = {}
		invoice_info["purchase_order_id"] = purchase_order_info["purchase_order_id"]
		invoice_info["buyer_purchase_order_id"] = purchase_order_info["buyer_purchase_order_id"]
		invoice_info["seller_id"] = purchase_order_info["seller_id"]
		invoice_info["seller_entity_name"] = purchase_order_info["seller_entity_name"]
		invoice_info["seller_address_id"] = purchase_order_info["seller_address_id"]
		invoice_info["seller_contact_user_id"] = purchase_order_info["seller_contact_user_id"]
		invoice_info["seller_contact_name"] = purchase_order_info["seller_contact_name"]
		invoice_info["seller_contact_phone"] = purchase_order_info["seller_contact_phone"]
		invoice_info["seller_contact_email"] = purchase_order_info["seller_contact_email"]
		invoice_info["buyer_id"] = purchase_order_info["buyer_id"]
		invoice_info["buyer_entity_name"] = purchase_order_info["buyer_entity_name"]
		invoice_info["buyer_billing_address_id"] = purchase_order_info["buyer_billing_address_id"]
		invoice_info["buyer_shipping_address_id"] = purchase_order_info["buyer_shipping_address_id"]
		invoice_info["buyer_contact_user_id"] = purchase_order_info["buyer_contact_user_id"]
		invoice_info["buyer_contact_name"] = purchase_order_info["buyer_contact_name"]
		invoice_info["buyer_contact_phone"] = purchase_order_info["buyer_contact_phone"]
		invoice_info["buyer_contact_email"] = purchase_order_info["buyer_contact_email"]
		invoice_info["status"] = "draft"
		return invoice_info
	
	def invoice_item_info_from_purchase_order_item_info(self, purchase_order_item_info):
		# Making invoice_item_info from purchase_order_item_info
		invoice_item_info = {}
		invoice_item_info["purchase_order_line_item_id"] = purchase_order_item_info["purchase_order_line_item_id"]
		invoice_item_info["item_id"] = purchase_order_item_info["item_id"]
		invoice_item_info["buyer_item_id"] = purchase_order_item_info["buyer_item_id"]
		invoice_item_info["buyer_item_name"] = purchase_order_item_info["buyer_item_name"]
		invoice_item_info["buyer_item_description"] = purchase_order_item_info["buyer_item_description"]
		invoice_item_info["measurement_unit_id"] = purchase_order_item_info["measurement_unit_id"]
		invoice_item_info["rate"] = purchase_order_item_info["rate"]
		invoice_item_info["shipping_per_unit"] = purchase_order_item_info["shipping_per_unit"]
		
		# Getting pending_quantity for this item
		pending_quantity = purchase_order_item_pending_quantity(purchase_order_line_item_id=self.purchase_order_line_item_id)

		# pending_quantity here will be shown as the quantity_invoiced for the draft invoice object
		invoice_item_info["quantity_invoiced"] = pending_quantity
		invoice_item_info["amount_due"] = 0
		invoice_item_info["currency_code"] = purchase_order_item_info["currency_code"]
		return invoice_item_info
	
	def invoice_item_attribute_from_purchase_order_item_attribute(self, purchase_order_line_item_id):
		# Making invoice_item_attribute from purchase_order_item_attribute
		invoice_item_attribute = []
		purchase_order_attribute_list = PurchaseOrderItemAttribute.objects.filter(purchase_order_line_item_id=purchase_order_line_item_id)
		purchase_order_attribute_list_data = PurchaseOrderItemAttributeSerializer(purchase_order_attribute_list, many=True).data
		for attribute in purchase_order_attribute_list_data:
			attribute_data = {}
			attribute_data["attribute_id"] = attribute["attribute_id"]
			attribute_data["attribute_value"] = attribute["attribute_value"]
			invoice_item_attribute.append(attribute_data)
		return invoice_item_attribute
	
	def invoice_item_charge_from_purchase_order_item_charge(self, purchase_order_line_item_id):
		# Making invoice_item_charge from purchase_order_item_charge
		invoice_item_charge = []
		purchase_order_charge_list = PurchaseOrderItemCharge.objects.filter(purchase_order_line_item_id=purchase_order_line_item_id)
		purchase_order_charge_list_data = PurchaseOrderItemChargeSerializer(purchase_order_charge_list, many=True).data
		for charge in purchase_order_charge_list_data:
			charge_data = {}
			charge_data["charge_name"] = charge["charge_name"]
			charge_data["charge_percentage"] = charge["charge_percentage"]
			invoice_item_charge.append(charge_data)
		return invoice_item_charge
	
	def invoice_buyer_information_from_purchase_order_buyer_information(self):
		# Making invoice_buyer_information from purchase_order_buyer_information
		invoice_buyer_information = []
		purchase_order_buyer_information_list = PurchaseOrderBuyerInformation.objects.filter(purchase_order_id=self.purchase_order_id)
		purchase_order_buyer_information_list_data = PurchaseOrderBuyerInformationSerializer(purchase_order_buyer_information_list, many=True).data
		for buyer_information in purchase_order_buyer_information_list_data:
			buyer_information_data = {}
			buyer_information_data["buyer_id"] = buyer_information["buyer_id"]
			buyer_information_data["identification_id"] = buyer_information["identification_id"]
			buyer_information_data["identification_name"] = buyer_information["identification_name"]
			buyer_information_data["identification_value"] = buyer_information["identification_value"]
			invoice_buyer_information.append(buyer_information_data)
		return invoice_buyer_information
	
	def invoice_seller_information_from_purchase_order_seller_information(self):
		# Making invoice_seller_information from purchase_order_seller_information
		invoice_seller_information = []
		purchase_order_seller_information_list = PurchaseOrderSellerInformation.objects.filter(purchase_order_id=self.purchase_order_id)
		purchase_order_seller_information_list_data = PurchaseOrderSellerInformationSerializer(purchase_order_seller_information_list, many=True).data
		for seller_information in purchase_order_seller_information_list_data:
			seller_information_data = {}
			seller_information_data["seller_id"] = seller_information["seller_id"]
			seller_information_data["identification_id"] = seller_information["identification_id"]
			seller_information_data["identification_name"] = seller_information["identification_name"]
			seller_information_data["identification_value"] = seller_information["identification_value"]
			invoice_seller_information.append(seller_information_data)
		return invoice_seller_information

class invoice_list(APIView):

	entity_type="Buyer"

	def get(self, request, user_id):
		# For getting all the invoice list including draft and real 
		# for both buyer or seller side (as requested)
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# If the request is from Buyer Side
		if(self.entity_type=="Buyer"):
			# Getting all the buyer id list
			buyer_id_list = list(Buyer.objects.filter(deleted_datetime__isnull=True).values_list("buyer_id", flat=True))
			# Getting all the current entity id list which is a buyer entity 
			# and having user with this user_id 
			user_buyer_entity_id_list = list(UserEntity.objects.filter(user_id=user_id).filter(deleted_datetime__isnull=True).filter(entity_id__in=buyer_id_list).values_list("entity_id", flat=True))

			# Getting all the invoice object list
			data_to_return = self.get_all_invoice_object_list_with_buyer_id_list(user_buyer_entity_id_list)
		
		else:
			# It must be from Seller Side Request
			# Getting all the seller id list
			seller_id_list = list(Seller.objects.filter(deleted_datetime__isnull=True).values_list("seller_id", flat=True))
			# Getting all the current entity id list which is a seller entity 
			# and having user with this user_id 
			user_seller_entity_id_list = list(UserEntity.objects.filter(user_id=user_id).filter(deleted_datetime__isnull=True).filter(entity_id__in=seller_id_list).values_list("entity_id", flat=True))

			# Getting all the invoice object list
			data_to_return = self.get_all_invoice_object_list_with_seller_id_list(user_seller_entity_id_list)
		
		return Response(data=data_to_return, status=status.HTTP_200_OK)
		
	def get_all_invoice_object_list_with_buyer_id_list(self, buyer_id_list):
		# Getting all the real invoice id list
		invoice_id_list = Invoice.objects.filter(buyer_id__in=buyer_id_list).values_list("invoice_id", flat=True)
		# Getting all the draft invoice id list
		draft_invoice_id_list = Invoice.objects.filter(buyer_id__in=buyer_id_list).values_list("invoice_id", flat=True)
		# Getting all the real invoice object (basically whole data) list
		invoice_object_list = self.get_invoice_object_list_with_invoice_id_list(invoice_id_list)
		# Getting all the draft invoice object (basically whole data) list
		draft_invoice_object_list = self.get_draft_invoice_object_list_with_invoice_id_list(draft_invoice_id_list)
		
		data_to_return = invoice_object_list
		data_to_return.extend(draft_invoice_object_list)
		return data_to_return
	
	def get_all_invoice_object_list_with_seller_id_list(self, seller_id_list):
		# Getting all the real invoice id list
		invoice_id_list = Invoice.objects.filter(seller_id__in=seller_id_list).values_list("invoice_id", flat=True)
		# Getting all the draft invoice id list
		draft_invoice_id_list = Invoice.objects.filter(seller_id__in=seller_id_list).values_list("invoice_id", flat=True)
		# Getting all the real invoice object (basically whole data) list
		invoice_object_list = self.get_invoice_object_list_with_invoice_id_list(invoice_id_list)
		# Getting all the draft invoice object (basically whole data) list
		draft_invoice_object_list = self.get_draft_invoice_object_list_with_invoice_id_list(draft_invoice_id_list)
		
		data_to_return = invoice_object_list
		data_to_return.extend(draft_invoice_object_list)
		return data_to_return
	
	def get_invoice_object_list_with_invoice_id_list(self, invoice_id_list):
		# Get all the invoice object list with invoice id list
		data_to_return = []
		for invoice_id in invoice_id_list:
			# Getting Draft Invoice Data
			get_invoice_request = HttpRequest()
			get_invoice_request.method = "GET"
			get_invoice_response = invoice.as_view()(get_invoice_request, invoice_id)
			if(get_invoice_response.status_code==200):	
				data_to_return.append(get_invoice_response.data)

		return data_to_return
	
	def get_draft_invoice_object_list_with_invoice_id_list(self, draft_invoice_id_list):
		# Get all the draft invoice object list with draft invoice id list
		data_to_return = []
		for invoice_id in draft_invoice_id_list:
			# Getting Draft Invoice Data
			get_draft_invoice_request = HttpRequest()
			get_draft_invoice_request.method = "GET"
			get_draft_invoice_response = draft_invoice.as_view()(get_draft_invoice_request, invoice_id)
			if(get_draft_invoice_response.status_code==200):	
				data_to_return.append(get_draft_invoice_response.data)
		
		return data_to_return

class invoice_list_for_new_goods(APIView):

	def get(self, request, purchase_order_id):
		# Get all the invoices with with invoice_type=goods, status="issued" 
		# and no GRs exist against any invoice_line_item_id
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Get all the invoice_id list against this purchase_order with above conditions
		invoice_id_list = Invoice.objects.filter(purchase_order_id=purchase_order_id, invoice_type="goods", status="issued").values_list("invoice_id", flat=True)
		
		# Removing all the invoices having GR present against them
		invoice_id_no_gr_list = []
		for invoice_id in invoice_id_list:
			invoice_line_item_id_list = InvoiceItem.objects.filter(invoice_id=invoice_id).values_list("invoice_line_item_id", flat=True)
			goods_receipt_check = GoodsReceipt.objects.filter(invoice_line_item_id__in=invoice_line_item_id_list).exists()
			if(not goods_receipt_check):
				invoice_id_no_gr_list.append(invoice_id)
		
		# Collecting all the invoice objects present in invoice_id_no_gr_list
		data_to_return = []
		for invoice_id in invoice_id_list:
			# Getting Invoice Data
			get_invoice_request = HttpRequest()
			get_invoice_request.method = "GET"
			get_invoice_response = invoice.as_view()(get_invoice_request, invoice_id)
			if(get_invoice_response.status_code==200):	
				data_to_return.append(get_invoice_response.data)

		return Response(data=data_to_return, status=status.HTTP_200_OK)

class invoice_item_max_pending_quantity_list(APIView):

	def get(self, request, invoice_id):
		# API for getting the max_pending_quantity list for all the items of an invoice in the corresponding purchase order, will be used while making a goods receipt
		try:
			invoice = Invoice.objects.get(invoice_id=invoice_id)
		except Invoice.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Get invoice_line_item_id_list of this invoice
		invoice_line_item_list = InvoiceItem.objects.filter(invoice_id=invoice_id)
		invoice_line_item_data_list = InvoiceItemSerializer(invoice_line_item_list, many=True).data
		
		data_to_return = []
		for invoice_item_data in invoice_line_item_data_list:
			# Getting the purchase_order_line_item_id for this invoice_line_item_id
			purchase_order_line_item_id = invoice_item_data["purchase_order_line_item_id"]
			# Getting the max_pending_quantity for this invoice_item
			max_pending_quantity = purchase_order_item_max_pending_quantity(purchase_order_line_item_id)
			# This max_pending_quantity will also include the invoiced quantity for this invoice_line_item 
			# (including means this invoice_item invoiced_quantity will be subtracted from this
			# purhcase order item max quantity)
			# So before sending max_pending_quantity,
			# current invoiced quantity (for which this goods receipt is being done) 
			# should be added to this max_pending_quantity
			data_to_return.append({
				"invoice_line_item_id": invoice_item_data["invoice_line_item_id"],
				"max_pending_quantity": max_pending_quantity + round(Decimal(invoice_item_data["quantity_invoiced"]), DECIMAL_COMPARISON_PRECISION),
				"comment": "This max_pending_quantity excludes the invoiced_quantity for this invoice."
			}) # added comment just for the reference on the front-end side
		
		return Response(data=data_to_return, status=status.HTTP_200_OK)

class proforma_invoice(APIView):

	def get(self, request, invoice_id):
		try:
			proforma_invoice = ProformaInvoice.objects.get(invoice_id=invoice_id)
		except ProformaInvoice.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		serializer = ProformaInvoiceSerializer(proforma_invoice)
		return Response(data=serializer.data, status=status.HTTP_200_OK)

class proforma_invoice_list(APIView):

	def get(self, request, purchase_order_id):
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		proforma_invoice_list = purchase_order.proformainvoice_set.all()
		proforma_invoice_list_data = ProformaInvoiceSerializer(proforma_invoice_list, many=True).data
		return Response(data=proforma_invoice_list_data, status=status.HTTP_200_OK)
	
	def post(self, request, purchase_order_id):
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		proforma_invoice_data = request.data.get("invoice_info", {})
		proforma_invoice_data["purchase_order_id"] = purchase_order_id
		serializer = ProformaInvoiceSerializer(data=proforma_invoice_data)
		if(serializer.is_valid()):
			serializer.save()
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		return Response(status=status.HTTP_201_CREATED)

class invoice_status(APIView):

	def get(self, request, invoice_line_item_id):
		try:
			invoice_item = InvoiceItem.objects.get(invoice_line_item_id=invoice_line_item_id)
		except InvoiceItem.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		invoice = invoice_item.invoice_id
		invoice_status = invoice.status
		return Response(data={"status": invoice_status}, status=status.HTTP_200_OK)
	
class non_fw_invoice(APIView):
	'''
	API for posting a non factwise invoice
	'''
	def post(self, request, purchase_order_id):
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		data = request.data
		data_to_return = {}

		# Posting Invoice Info
		invoice_info = data.get("invoice_info", {})
		invoice_info["status"] = "issued"
		invoice_info["purchase_order_id"] = purchase_order_id
		serializer = InvoiceSerializer(data=invoice_info)
		if(serializer.is_valid()):
			serializer.save()
			data_to_return["invoice_info"] = serializer.data
			curr_invoice_id = serializer.data["invoice_id"]
			curr_invoice = Invoice.objects.get(invoice_id=curr_invoice_id)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Posting Invoice Item List
		invoice_item_list = data.get("invoice_item_list", [])
		# Checking for at least one item
		if(len(invoice_item_list)==0):
			curr_invoice.delete()
			return Response(status=status.HTTP_400_BAD_REQUEST)
			
		item_list = []
		for invoice_item in invoice_item_list:
			item = {}
			invoice_item_info = invoice_item.get("item_info", {})
			curr_purchase_order_line_item_id = invoice_item_info.get("purchase_order_line_item_id")
			# Checking if this curr_purchase_order_line_item_id exists
			try:
				purchase_order_line_item = PurchaseOrderItem.objects.get(purchase_order_line_item_id=curr_purchase_order_line_item_id)
			except PurchaseOrderItem.DoesNotExist:
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			# Checking if the invoice_quantity is less than max_pending_quantity
			curr_invoice_item_max_pending_quantity = purchase_order_item_max_pending_quantity(curr_purchase_order_line_item_id)
			if(round(Decimal(invoice_item_info.get("quantity_invoiced", Decimal("Inf"))), DECIMAL_COMPARISON_PRECISION) > curr_invoice_item_max_pending_quantity):
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)

			invoice_item_info["invoice_id"] = curr_invoice_id
			serializer = InvoiceItemSerializer(data=invoice_item_info)
			if(serializer.is_valid()):
				serializer.save()
				item["item_info"] = serializer.data
				curr_invoice_line_item_id = serializer.data["invoice_line_item_id"]
				curr_invoice_item = InvoiceItem.objects.get(invoice_line_item_id=curr_invoice_line_item_id)
			else:
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)
			item_attribute_list = []
			invoice_item_attribute_list = invoice_item.get("item_attribute", [])
			for invoice_item_attribute in invoice_item_attribute_list:
				invoice_item_attribute["invoice_line_item_id"] = curr_invoice_line_item_id
				serializer = InvoiceItemAttributeSerializer(data=invoice_item_attribute)
				if(serializer.is_valid()):
					serializer.save()
					item_attribute_list.append(serializer.data)
				else:
					curr_invoice.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
			
			item["item_attribute"] = item_attribute_list

			item_charge_list = []
			invoice_item_charge_list = invoice_item.get("item_charge", [])
			for invoice_item_charge in invoice_item_charge_list:
				invoice_item_charge["invoice_line_item_id"] = curr_invoice_line_item_id
				serializer = InvoiceItemChargeSerializer(data=invoice_item_charge)
				if(serializer.is_valid()):
					serializer.save()
					item_charge_list.append(serializer.data)
				else:
					curr_invoice.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
			
			item["item_charge"] = item_charge_list
			item_list.append(item)
		data_to_return["invoice_item_list"] = item_list

		# Posting Invoice Buyer Information
		invoice_buyer_information_list = data.get("invoice_buyer_information", [])
		buyer_information_list = []
		if(len(invoice_buyer_information_list)!=0):
			for invoice_buyer_information in invoice_buyer_information_list:
				invoice_buyer_information["invoice_id"] = curr_invoice_id
			serializers = InvoiceBuyerInformationSerializer(data=invoice_buyer_information_list, many=True)
			if(serializers.is_valid()):
				serializers.save()
				buyer_information_list = serializers.data
			else:
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)

		data_to_return["invoice_buyer_information"] = buyer_information_list
		# Posting Invoice seller Information
		invoice_seller_information_list = data.get("invoice_seller_information", [])

		seller_information_list = []
		if(len(invoice_seller_information_list)!=0):
			for invoice_seller_information in invoice_seller_information_list:
				invoice_seller_information["invoice_id"] = curr_invoice_id

			serializers = InvoiceSellerInformationSerializer(data=invoice_seller_information_list, many=True)
			if(serializers.is_valid()):
				serializers.save()
				seller_information_list = serializers.data
			else:
				curr_invoice.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)

		data_to_return["invoice_seller_information"] = seller_information_list

		return Response(data=data_to_return, status=status.HTTP_201_CREATED)