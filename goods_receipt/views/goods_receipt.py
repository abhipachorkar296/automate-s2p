import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.http import HttpRequest
from django.db import transaction
from django.urls import reverse
import json
from decimal import *
from django.utils import timezone
from datetime import timedelta
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
from goods_receipt.serializers import *
from quality_check.models import *
from invoice.views.invoice import purchase_order_item_max_pending_quantity, invoice_item_amount_from_quantity
from django.conf import settings

DECIMAL_COMPARISON_PRECISION = settings.DECIMAL_COMPARISON_PRECISION

def calculate_invoice_item_payment_due_date(payment_terms_reference_date_type, payment_terms_days, dispatch_date, receipt_date):
	# Function for calculating payment_due_date using invoice_item fields
	new_payment_due_date = receipt_date
	if(payment_terms_reference_date_type=="dispatch_date"):
		new_payment_due_date = (dispatch_date if dispatch_date else receipt_date) + timedelta(days=int(payment_terms_days if payment_terms_days else 0))
	elif(payment_terms_reference_date_type=="receipt_date"):
		new_payment_due_date = receipt_date + timedelta(days=int(payment_terms_days if payment_terms_days else 0))
	
	return new_payment_due_date

class goods_receipt(APIView):

	def get(self, request, goods_receipt_entry_id):
		try:
			goods_receipt = GoodsReceipt.objects.get(goods_receipt_entry_id=goods_receipt_entry_id)
		except GoodsReceipt.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		data_to_return = {}
		data_to_return["goods_receipt_info"] = GoodsReceiptSerializer(goods_receipt).data
		return Response(data=data_to_return, status=status.HTTP_200_OK)

class goods_receipt_list(APIView):
	
	def get(self, request, invoice_id):
		try:
			invoice = Invoice.objects.get(invoice_id=invoice_id)
		except Invoice.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Get invoice_line_item_id_list of this invoice
		invoice_line_item_id_list = InvoiceItem.objects.filter(invoice_id=invoice_id).values_list("invoice_line_item_id", flat=True)
		# Get all the Goods Receipt linked with any of the invoice_line_item_id in invoice_line_item_id_list
		goods_receipt_list = GoodsReceipt.objects.filter(invoice_line_item_id__in=invoice_line_item_id_list)
		goods_receipt_list_data = GoodsReceiptSerializer(goods_receipt_list, many=True).data
		# Inserting key goods_receipt_info for every goods_receipt_info
		goods_receipt_list_data = [{"goods_receipt_info": data} for data in goods_receipt_list_data]
		return Response(data=goods_receipt_list_data, status=status.HTTP_200_OK)

	def post(self, request, user_id, invoice_line_item_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			invoice_item = InvoiceItem.objects.get(invoice_line_item_id=invoice_line_item_id)
			invoice_item_data = InvoiceItemSerializer(invoice_item).data
		except InvoiceItem.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		try:
			# Getting the goods_receipt_data which needs to be posted
			goods_receipt_incoming_data = request.data["goods_receipt_info"]
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		goods_receipt_incoming_data["invoice_line_item_id"] = invoice_line_item_id

		invoice_id = invoice_item_data["invoice_id"]
		invoice_data = InvoiceSerializer(Invoice.objects.get(invoice_id=invoice_id)).data
		buyer_id = invoice_data["buyer_id"]
		# Checking if this user has access to this buyer entity
		try:
			user_entity = UserEntity.objects.get(user_id=user_id, entity_id=buyer_id, deleted_datetime__isnull=True)
		except UserEntity.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Checking if there exists any goods receipt for this invoice_line_item_id
		existing_goods_receipt = GoodsReceipt.objects.filter(invoice_line_item_id=invoice_line_item_id).exists()
		if(existing_goods_receipt):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		# Checking if the receipt_quantity_accepted <= delivered_quantity
		try:
			if(round(Decimal(goods_receipt_incoming_data["receipt_quantity_accepted"]), DECIMAL_COMPARISON_PRECISION) > round(Decimal(goods_receipt_incoming_data["delivered_quantity"]), DECIMAL_COMPARISON_PRECISION)):
				return Response(status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		receipt_quantity_accepted = round(Decimal(goods_receipt_incoming_data["receipt_quantity_accepted"]), DECIMAL_COMPARISON_PRECISION)
		# Getting the purchase_order_line_item_id for this invoice_line_item_id
		purchase_order_line_item_id = invoice_item_data["purchase_order_line_item_id"]
		# Getting the max_pending_quantity for this invoice_item
		max_pending_quantity = purchase_order_item_max_pending_quantity(purchase_order_line_item_id)

		# This max_pending_quantity will also include the invoiced quantity for this invoice_line_item 
		# (including means this invoice_item invoiced_quantity will be subtracted from this
		# purhcase order item max quantity)
		# So before checking if the receipt_quantity_accepted <= max_pending_quantity,
		# current invoiced quantity (for which this goods receipt is being done) 
		# should be added to this max_pending_quantity
		if(receipt_quantity_accepted > max_pending_quantity+round(Decimal(invoice_item_data["quantity_invoiced"]), DECIMAL_COMPARISON_PRECISION)):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# All checks passed
		# Direct post the goods receipt
		serializer = GoodsReceiptSerializer(data=goods_receipt_incoming_data)
		if(serializer.is_valid()):
			serializer.save()
			goods_receipt = GoodsReceipt.objects.get(goods_receipt_entry_id=serializer.data["goods_receipt_entry_id"])
			goods_receipt_data = serializer.data
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Updating Invoice and Invoice Item
		invoice = invoice_item.invoice_id
		# Getting the amount from the receipt_quantity_accepted and updating invoice_line_item amount_due
		invoice_item.amount_due = invoice_item_amount_from_quantity(invoice_line_item_id, Decimal(goods_receipt_data["receipt_quantity_accepted"]))
		invoice_item.receipt_date = goods_receipt.receipt_datetime
		invoice_item.save()
		invoice.status = "ongoing"
		invoice.save()
		# Saving payment_due_date of the invoice_item
		dispatch_date = (invoice_item.dispatch_date if invoice_item.dispatch_date else 0)
		receipt_date = invoice_item.receipt_date
		payment_terms_reference_date_type = str(invoice_item.payment_terms_reference_date_type)
		payment_terms_days = (invoice_item.payment_terms_days if invoice_item.payment_terms_days else 0)
		invoice_item.payment_due_date = calculate_invoice_item_payment_due_date(payment_terms_reference_date_type, payment_terms_days, dispatch_date, receipt_date)
		invoice_item.save()

		# For just reference purpose, when there is some additional data needed from frontend side
		# First getting the data to updated
		# Structure of invoice_info expected to be coming in the request data
		'''
		{
			invoice_info: {
				"status": "ongoing",
				"payment_due_date": "2021-05-17T09:49:43.583737Z",
				"amount_due": "12"

			}
		}
		'''
		# invoice_data_to_be_updated = request.data.get("invoice_info")
		# invoice = invoice_item.invoice_id
		# try:
		# 	invoice_item_update_data = {
		# 		"payment_due_date": invoice_data_to_be_updated["payment_due_date"],
		# 		"amount_due": invoice_data_to_be_updated["amount_due"],
		# 		"receipt_date": goods_receipt_data["receipt_datetime"]
		# 	}
		# 	invoice_item_serializer = InvoiceItemSerializer(invoice_item, invoice_item_update_data, partial=True)
		# 	if(invoice_item_serializer.is_valid()):
		# 		invoice_item_serializer.save()
		# 	else:
		# 		# Data is wrong
		# 		goods_receipt.delete()
		# 		return Response(status=status.HTTP_400_BAD_REQUEST)
		# 	invoice.status = "ongoing"
		# 	invoice.save()
		# except Exception as e:
		# 	# Data is wrong
		# 	goods_receipt.delete()
		# 	return Response(status=status.HTTP_400_BAD_REQUEST) 

		return Response(status=status.HTTP_201_CREATED)

class goods_receipt_non_fw_invoice(APIView):
	'''
	API for posting goods receipt for non Factwise Invoice
	'''
	def post(self, request, user_id, purchase_order_id):
		try:
			purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
		except PurchaseOrder.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			with transaction.atomic():
				'''
				Format of request data
				{
					invoice_data: {
						the usual invoice data format
					},
					goods_receipt_data: [
						{
							purchase_order_line_item_id: {
								the usual goods_receipt format
							}
						}
					]
				}
				'''
				new_invoice_data = request.data.get("invoice_data", {})
				headers = {
					'Content-Type': 'application/json'
				}
				# Trying to post a Non Factwise Invoice
				response = requests.post(reverse("invoice:non_fw_invoice", args=[purchase_order_id]), data=json.dumps(new_invoice_data), headers=headers)
				if(response.status_code!=201):
					raise ValidationError
				
				invoice_posted_data = response.text
				# Making the map containing the purchase_order_line-item_id and invoice_line_item_id
				purchase_order_invoice_line_item_id_map = {}
				for invoice_item_data in invoice_posted_data["invoice_item_list"]:
					invoice_line_item_id = invoice_item_data["item_info"]["invoice_line_item_id"]
					purchase_order_line_item_id = invoice_item_data["item_info"]["purchase_order_line_item_id"]
					purchase_order_invoice_line_item_id_map[purchase_order_line_item_id] = invoice_line_item_id
				
				goods_receipt_data_list = request.data.get("goods_receipt_data", [])
				for goods_receipt_data in goods_receipt_data_list:
					purchase_order_line_item_id = goods_receipt_data.keys()[0]
					invoice_line_item_id = purchase_order_invoice_line_item_id_map[purchase_order_line_item_id]
					new_goods_receipt_data = goods_receipt_data[purchase_order_line_item_id]["goods_receipt_info"]
					new_goods_receipt_data["invoice_line_item_id"] = purchase_order_invoice_line_item_id_map[purchase_order_line_item_id]
					headers = {
						'Content-Type': 'application/json'
					}
					# Trying to post a Goods Receipt
					response = requests.post(reverse("goods_receipt:goods_receipt_list", args=[user_id, invoice_line_item_id]), data=json.dumps(new_goods_receipt_data), headers=headers)
					if(response.status_code!=201):
						raise ValidationError

		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		return Response(status=status.HTTP_201_CREATED)