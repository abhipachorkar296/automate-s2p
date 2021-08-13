from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import *
from django.utils import timezone
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
from quality_check.serializers import *
from invoice.views.invoice import invoice_item_amount_from_quantity
from django.conf import settings

DECIMAL_COMPARISON_PRECISION = settings.DECIMAL_COMPARISON_PRECISION

class quality_check(APIView):

	def get(self, request, quality_check_id):
		try:
			quality_check = QualityCheck.objects.get(quality_check_id=quality_check_id)
		except QualityCheck.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		data_to_return = {}
		serializer = QualityCheckSerializer(quality_check)
		data_to_return["quality_check_info"] = serializer.data
		return Response(data=data_to_return, status=status.HTTP_200_OK)

def get_all_quality_check_rejections(goods_receipt_entry_id):
	# Function for getting the sum of the total previous qualtiy check rejections for this given goods receipt
	total_quality_check_rejections = round(Decimal(sum(list(QualityCheck.objects.filter(goods_receipt_entry_id=goods_receipt_entry_id).values_list("quantity_rejected", flat=True)))), DECIMAL_COMPARISON_PRECISION)
	return total_quality_check_rejections

class quality_check_list(APIView):

	def get(self, request, goods_receipt_entry_id):
		try:
			goods_receipt = GoodsReceipt.objects.get(goods_receipt_entry_id=goods_receipt_entry_id)
		except GoodsReceipt.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		quality_check_list = goods_receipt.qualitycheck_set.all()
		quality_check_list_data = QualityCheckSerializer(quality_check_list, many=True).data
		quality_check_list_data = [{"quality_check_info": data} for data in quality_check_list_data]
		return Response(data=quality_check_list_data, status=status.HTTP_200_OK)
	
	def post(self, request, goods_receipt_entry_id):
		try:
			goods_receipt = GoodsReceipt.objects.get(goods_receipt_entry_id=goods_receipt_entry_id)
		except GoodsReceipt.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Getting invoice for this goods_receipt
		invoice_line_item = goods_receipt.invoice_line_item_id
		invoice = invoice_line_item.invoice_id
		
		# Checking if the invoice type is "goods" or not
		if(invoice.invoice_type!="goods"):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		# Quality Check can only be posted if invoice status is one of the follwoing:
		# - Ongoing
		# - Termination requested by seller
		# - Complete
		invoice_check = False
		if(invoice.status=="ongoing"):
			invoice_check = True
		elif(invoice.status=="complete"):
			invoice_check = True
		elif(invoice.status=="termination_request"):
			# Checking if this termiantion request has been done by the Seller 
			# and Buyer has not accepted
			seller_termination_request_check = False
			if((not invoice.closing_user_id_buyer) and invoice.closing_user_id_seller):
				seller_termination_request_check = True
			if((not invoice.closing_datetime_buyer) and invoice.closing_datetime_seller):
				seller_termination_request_check = seller_termination_request_check & True
				# If above both two cases pass, then only seller_termination_request_check becomes True
			if(seller_termination_request_check):
				invoice_check = True
		
		if(not invoice_check):
			# Invoice status does not lie in the allowable status list for QC to be posted
			return Response(status=status.HTTP_400_BAD_REQUEST)
				
		try:
			quality_check_data = request.data["quality_check_info"]
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		# getting the total previous quality check quantity rejected
		total_previous_quality_check_rejected = get_all_quality_check_rejections(goods_receipt_entry_id)
		latest_quantity_accepted = round(goods_receipt.receipt_quantity_accepted - total_previous_quality_check_rejected, DECIMAL_COMPARISON_PRECISION)
		
		# Checking whether the latest_accepted_quantity is zero or not
		# and also Checking whether the quantity_rejected <= latest_quantity_accepted
		try:
			if(latest_quantity_accepted==0 or round(Decimal(quality_check_data["quantity_rejected"]), DECIMAL_COMPARISON_PRECISION) > latest_quantity_accepted):
				return Response(status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Checks have passed
		# quality_check_data can be posted
		quality_check_data["goods_receipt_entry_id"] = goods_receipt_entry_id
		serializer = QualityCheckSerializer(data=quality_check_data)
		if(serializer.is_valid()):
			serializer.save()
			quality_check_id = serializer.data["quality_check_id"]
			quality_check = QualityCheck.objects.get(quality_check_id=quality_check_id)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		quantity_rejected = round(Decimal(quality_check_data["quantity_rejected"]), DECIMAL_COMPARISON_PRECISION)

		# Checking if the quantity_rejected > 0 for proceeding for updating amount_due
		if(not (quantity_rejected>0)):
			return Response(status=status.HTTP_201_CREATED)
		
		# here quantity_rejected > 0
		# updating amount_due

		# Shifted all this calculation to a function invoice_item_amount_from_quantity in invoice views
		# rate = invoice_line_item.rate
		# all_taxes_percentage_sum = round(Decimal(sum(list(invoice_line_item.invoiceitemcharge_set.all().values_list("charge_percentage", flat=True)))), DECIMAL_COMPARISON_PRECISION)
		# shipping_per_unit = invoice_line_item.shipping_per_unit
		# invoice_discount_percentage = invoice.invoice_discount_percentage
		# rejection_amount = round(Decimal((1+Decimal(0.01)*all_taxes_percentage_sum-Decimal(0.01)*invoice_discount_percentage)*quantity_rejected*rate + quantity_rejected*shipping_per_unit), DECIMAL_COMPARISON_PRECISION)

		rejection_amount = invoice_item_amount_from_quantity(invoice_line_item.invoice_line_item_id, quantity_rejected)

		original_amount_due = round(Decimal(invoice_line_item.amount_due), DECIMAL_COMPARISON_PRECISION)
		amount_paid = round(Decimal(invoice_line_item.amount_paid), DECIMAL_COMPARISON_PRECISION)
		
		# When the original_amount_due <= amount_paid, decrease the amount due and
		# create a payment balance against this rejection
		if(original_amount_due<=amount_paid):
			new_amount_due = original_amount_due - rejection_amount
			# making data for posting payment balance
			data = {
				"buyer_id": invoice.buyer_id,
				"seller_id": invoice.seller_id,
				"entry_type": "rejection",
				"rejection_quality_check_id": quality_check.quality_check_id,
				"currency_code": invoice_line_item.currency_code,
				"total_amount": rejection_amount,
				"used_amount": 0,
				"available_amount": rejection_amount,
			}
			# Creating Payment Balance
			PaymentBalance.objects.create(**data)
		else:
			# here the original_amount_due > amount_paid
			new_amount_due = original_amount_due - rejection_amount
			# When the new_amount_due is still > amount_paid
			# then just decrease the amount_due
			if(new_amount_due>=amount_paid):
				# Only amount_due should be decreased because after decreasing the amount_due,
				# if it is still greater, that won't create any balance since still there are 
				# some amount to be paid, just less amount has to be paid
				pass
			else:
				# Here there is a cross over occurring (means before this quality_check,
				# the amound_due was more than amount_paid but the rejection amount made 
				# the new amount_due lower than amount_paid, so there has to be a payment
				# balance created for the extra difference (amount_paid-new_amount_due)).
				# making data for posting payment balance
				extra_difference = amount_paid - new_amount_due
				data = {
					"buyer_id": invoice.buyer_id,
					"seller_id": invoice.seller_id,
					"entry_type": "rejection",
					"rejection_quality_check_id": quality_check.quality_check_id,
					"currency_code": invoice_line_item.currency_code,
					"total_amount": extra_difference,
					"used_amount": 0,
					"available_amount": extra_difference,
				}
				# Creating Payment Balance
				PaymentBalance.objects.create(**data)
		
		# Updating amount_due in the invoice_line_item to new_amount_due
		invoice_line_item.amount_due = new_amount_due
		invoice_line_item.save()

		return Response(status=status.HTTP_201_CREATED)