from rest_framework.views import APIView
from django.http import HttpRequest
import requests
from rest_framework.response import Response
from rest_framework import status
import json
from django.utils import timezone
from django.urls import reverse
from collections import defaultdict
from enterprise.models import * 
from enterprise.serializers import *
from event.models import *
from event.serializers import *
from purchase_order.models import *
from purchase_order.serializers import *
from invoice.models import *
from invoice.serializers import *
from goods_receipt.models import *
from goods_receipt.serializers import *

class draft_invoice(APIView):
    def get(self, request, invoice_id):
        try:
            invoice = DraftInvoice.objects.get(invoice_id=invoice_id)
        except DraftInvoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data_to_return = {}
        data_to_return["invoice_info"] = DraftInvoiceSerializer(invoice).data
        buyer_information = DraftInvoiceBuyerInformation.objects.filter(invoice_id=invoice_id)
        data_to_return["invoice_buyer_information"] = DraftInvoiceBuyerInformationSerializer(buyer_information, many=True).data

        seller_information = DraftInvoiceSellerInformation.objects.filter(invoice_id=invoice_id)
        data_to_return["invoice_seller_information"] = DraftInvoiceSellerInformationSerializer(seller_information, many=True).data
        
        invoice_items = invoice.draftinvoiceitem_set.all()
        invoice_line_item_id_list = invoice_items.values_list("invoice_line_item_id", flat=True)

        item_list = []
        for invoice_line_item_id in invoice_line_item_id_list:
            item = {}
            invoice_item = DraftInvoiceItem.objects.get(invoice_line_item_id=invoice_line_item_id)
            item["item_info"] = DraftInvoiceItemSerializer(invoice_item).data
            invoice_item_charge = DraftInvoiceItemCharge.objects.filter(invoice_line_item_id=invoice_line_item_id)
            item_charge = DraftInvoiceItemChargeSerializer(invoice_item_charge, many=True).data
            item["item_charge"] = item_charge
            invoice_item_attribute = DraftInvoiceItemAttribute.objects.filter(invoice_line_item_id=invoice_line_item_id)
            item["item_attribute"] = DraftInvoiceItemAttributeSerializer(invoice_item_attribute, many=True).data
            item_list.append(item)
        
        data_to_return["invoice_item_list"] = item_list
        return Response(data=data_to_return, status=status.HTTP_200_OK)

    def patch(self, request, invoice_id):
        try:
            invoice = DraftInvoice.objects.get(invoice_id=invoice_id)
        except DraftInvoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data_to_return = {}
        data = request.data
        invoice_info_data = data["invoice_info"]
        serializer = DraftInvoiceSerializer(invoice, data=invoice_info_data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["invoice_info"] = serializer.data
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        buyer_information_list = data.get("invoice_buyer_information",[])
        for buyer_info in buyer_information_list:
            buyer_info["invoice_id"] = invoice_id
        buyer_information_object = DraftInvoiceBuyerInformation.objects.filter(invoice_id=invoice_id)
        buyer_information_object.delete()
        if(len(buyer_information_list) > 0):
            serializers = DraftInvoiceBuyerInformationSerializer(data=buyer_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["invoice_buyer_information"] = serializers.data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["invoice_buyer_information"] = []
        seller_information_list = data.get("invoice_seller_information",[])
        for seller_info in seller_information_list:
            seller_info["invoice_id"] = invoice_id
        seller_information_object = DraftInvoiceSellerInformation.objects.filter(invoice_id=invoice_id)
        seller_information_object.delete()
        if(len(seller_information_list) > 0):
            serializers = DraftInvoiceSellerInformationSerializer(data=seller_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["invoice_seller_information"] = serializers.data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["invoice_seller_information"] = []
        #deleting previous items and charges
        invoice_items = invoice.draftinvoiceitem_set.all()
        invoice_items.delete()
        
        #posting new data
        invoice_item_list = data["invoice_item_list"]
        item_list = []
        for item_data in invoice_item_list:
            item = {}
            item_info_data = item_data["item_info"]
            item_info_data["invoice_id"] = invoice_id
            serializer = DraftInvoiceItemSerializer(data=item_info_data)
            if(serializer.is_valid()):
                serializer.save()
                item["item_info"] = serializer.data
                invoice_line_item_id = serializer.data.get("invoice_line_item_id")
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_charge_list = item_data["item_charge"]
            for item_charge in item_charge_list:
                item_charge["invoice_line_item_id"] = invoice_line_item_id
            serializers = DraftInvoiceItemChargeSerializer(data=item_charge_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_charge"] = serializers.data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_attribute_list = item_data["item_attribute"]
            for item_attribute in item_attribute_list:
                item_attribute["invoice_line_item_id"] = invoice_line_item_id
            serializers = DraftInvoiceItemAttributeSerializer(data=item_attribute_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_attribute"] = serializers.data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_list.append(item)
        
        data_to_return["invoice_item_list"] = item_list
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)
    
    def delete(self, request, invoice_id):
        try:
            invoice = DraftInvoice.objects.get(invoice_id=invoice_id)
        except DraftInvoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        invoice.delete()
        return Response(status=status.HTTP_200_OK)

class draft_invoice_list(APIView):
    def get(self, request, user_id, purchase_order_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Check weather this purchase order is related to given user or not
        is_exist = UserEntity.objects.filter(user_id=user_id, entity_id=purchase_order.buyer_id_id).exists()
        if(not is_exist):
            is_exist = UserEntity.objects.filter(user_id=user_id, entity_id=purchase_order.seller_id_id).exists()
        if(not is_exist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        invoice_list = DraftInvoice.objects.filter(purchase_order_id=purchase_order_id)
        request = HttpRequest()
        request.method = "GET"
        data = []
        for invoice in invoice_list:   
            response_draft_invoice = draft_invoice.as_view()(request,invoice.invoice_id)
            if(response_draft_invoice.status_code == 200):
                data.append(response_draft_invoice.data)
        
        return Response(data=data, status=status.HTTP_200_OK)


    def post(self, request, user_id, purchase_order_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Check whether this purchase order is related to given user or not
        is_exist = UserEntity.objects.filter(user_id=user_id, entity_id=purchase_order.buyer_id_id).exists()
        if(not is_exist):
            is_exist = UserEntity.objects.filter(user_id=user_id, entity_id=purchase_order.seller_id_id).exists()
        if(not is_exist):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        seller_id = purchase_order.seller_id_id
        buyer_id = purchase_order.buyer_id_id

        data_to_return = {}
        data = request.data
        invoice_info_data = data["invoice_info"]
        invoice_info_data["created_by_user_id"] = user_id
        invoice_info_data["purchase_order_id"] = purchase_order_id
        invoice_info_data["buyer_id"] = buyer_id
        invoice_info_data["seller_id"] = seller_id
        serializer = DraftInvoiceSerializer(data=invoice_info_data)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["invoice_info"] = serializer.data
            invoice_id = serializer.data.get("invoice_id")
            invoice = DraftInvoice.objects.get(invoice_id=invoice_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        buyer_information_list = data.get("invoice_buyer_information",[])
        if(len(buyer_information_list) > 0):
            for buyer_information in buyer_information_list:
                buyer_information["invoice_id"] = invoice_id
                buyer_information["buyer_id"] = buyer_id
            serializers = DraftInvoiceBuyerInformationSerializer(data=buyer_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["invoice_buyer_information"] = serializers.data
            else:
                invoice.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["invoice_seller_information"] = []
        seller_information_list = data.get("invoice_seller_information",[])
        if(len(seller_information_list) > 0):
            for seller_information in seller_information_list:
                seller_information["invoice_id"] = invoice_id
                seller_information["seller_id"] = seller_id
            serializers = DraftInvoiceSellerInformationSerializer(data=seller_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["invoice_seller_information"] = serializers.data
            else:
                invoice.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["invoice_seller_information"] = []
        
        invoice_item_list = data["invoice_item_list"]
        item_list = []
        for item_data in invoice_item_list:
            item = {}
            item_info_data = item_data["item_info"]
            item_info_data["invoice_id"] = invoice_id
            serializer = DraftInvoiceItemSerializer(data=item_info_data)
            if(serializer.is_valid()):
                serializer.save()
                item["item_info"] = serializer.data
                invoice_line_item_id = serializer.data.get("invoice_line_item_id")
            else:
                invoice.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_charge_list = item_data["item_charge"]
            for item_charge in item_charge_list:
                item_charge["invoice_line_item_id"] = invoice_line_item_id
            serializers = DraftInvoiceItemChargeSerializer(data=item_charge_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_charge"] = serializers.data
            else:
                invoice.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_attribute_list = item_data["item_attribute"]
            for item_attribute in item_attribute_list:
                item_attribute["invoice_line_item_id"] = invoice_line_item_id
            serializers = DraftInvoiceItemAttributeSerializer(data=item_attribute_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_attribute"] = serializers.data
            else:
                invoice.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_list.append(item)
        
        data_to_return["invoice_item_list"] = item_list
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class invoice_termination_request(APIView):
    def patch(self, request, user_id, entity_id, invoice_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id, deleted_datetime__isnull=True)
        except UserEntity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            invoice = Invoice.objects.get(invoice_id=invoice_id)
            serializer = InvoiceSerializer(invoice)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # allowing buyer to request termination if status is issued
        if(invoice.status == "issued"):
            if(entity_id == serializer.data["buyer_id"]):
                invoice.closing_user_id_buyer = user
                invoice.closing_comment_buyer =  request.data.get("closing_comment_buyer","")
                invoice.closing_datetime_buyer = timezone.now()
                invoice.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            invoice.status = "termination_request"
            invoice.save()
            return Response(status=status.HTTP_200_OK)
        # checking if status is already termination request or not
        # checking if Invoice status is Ongoing 
        if(invoice.status != "ongoing"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # if buyer is requesting termination
        if(entity_id == serializer.data["buyer_id"]):
            invoice.closing_user_id_buyer = user
            invoice.closing_comment_buyer =  request.data.get("closing_comment_buyer","")
            invoice.closing_datetime_buyer = timezone.now()
            invoice.save()
        # if seller is requesting termination
        elif(entity_id == serializer.data["seller_id"]):
            invoice.closing_user_id_seller = user
            invoice.closing_comment_seller =  request.data.get("closing_comment_seller","")
            invoice.closing_datetime_seller = timezone.now()
            invoice.save()
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        #changing status to termination request
        invoice.status = "termination_request"
        invoice.save()
        return Response(status=status.HTTP_200_OK)

class invoice_undo_termination_request(APIView):
    def patch(self, request, user_id, entity_id, invoice_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id, deleted_datetime__isnull=True)
        except UserEntity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        try:
            invoice = Invoice.objects.get(invoice_id=invoice_id)
            serializer = InvoiceSerializer(invoice)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            purchase_order = PurchaseOrder.objects.get(purchase_order_id=invoice.purchase_order_id_id)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if(purchase_order.status == "closed" or invoice.status != "termination_request"):
            return Response(data = "Not allowed", status=status.HTTP_400_BAD_REQUEST)
        # if buyer is requesting undo termination
        if(entity_id == serializer.data["buyer_id"]):
            if(not(invoice.closing_user_id_seller)):
                invoice.closing_user_id_buyer = None
                invoice.closing_comment_buyer =  ""
                invoice.closing_datetime_buyer = None
                invoice.save()
            else:
                return Response(data="Not allowed", status=status.HTTP_400_BAD_REQUEST)
        # if seller is requesting undo termination
        elif(entity_id == serializer.data["seller_id"]):
            if(not(invoice.closing_user_id_buyer)):
                invoice.closing_user_id_seller = None
                invoice.closing_comment_seller =  ""
                invoice.closing_datetime_seller = None
                invoice.save()
            else:
                return Response(data="Not allowed", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # changing status
        invoice_items = invoice.invoiceitem_set.all()
        invoice_line_item_id_list = invoice_items.values_list("invoice_line_item_id", flat=True)
        is_exist = GoodsReceipt.objects.filter(invoice_line_item_id__in=invoice_line_item_id_list).exists()
        #If goods_receipt is present, invoice status "ongoing"
        if(is_exist):
            invoice.status = "ongoing"
        #If goods_receipt is not present then invoice status "issued"
        else:
            invoice.status = "issued"
        invoice.save()

        return Response(status=status.HTTP_200_OK)

class rescind_invoice(APIView):
    def patch(self, request, user_id, invoice_id):
        try:
            invoice_user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            invoice = Invoice.objects.get(invoice_id=invoice_id)
            serializer = InvoiceSerializer(invoice)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            user_entity = UserEntity.objects.get(user_id=user_id, entity_id=invoice.seller_id_id, deleted_datetime__isnull=True)
        except UserEntity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if(invoice.status != "issued"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        invoice.status = "rescind"
        invoice.closing_user_id_seller = invoice_user
        invoice.closing_comment_seller = request.data.get("closing_comment_seller", "")
        invoice.closing_datetime_seller = timezone.now()
        invoice.invoice_close_datetime = timezone.now()
        invoice.save()
        return Response(status=status.HTTP_200_OK)

class invoice_accept_termination(APIView):
	def patch(self, request, user_id, entity_id, invoice_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			entity = Entity.objects.get(entity_id=entity_id)
		except Entity.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			invoice = Invoice.objects.get(invoice_id=invoice_id)
			invoice_data = InvoiceSerializer(invoice).data
		except Invoice.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id, deleted_datetime__isnull=True)
		except UserEntity.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Checking if the Invoice has already been closed
		if(invoice.invoice_close_datetime or invoice.status != "termination_request"):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		# Checking if the acceptance is being done by Buyer or Seller
		buyer = False
		seller = False
		if(invoice_data["buyer_id"]==entity_id):
			# Checking if the entity is the buyer
			buyer = True
		elif(invoice_data["seller_id"]==entity_id):
			# Now checking if the entity is the seller
			seller = True
		
		if(buyer and not seller):
			# Checking the fields
			closing_user_seller_id = invoice_data["closing_user_id_seller"]
			try:
				closing_user_seller_id = User.objects.get(user_id=closing_user_seller_id)
			except User.DoesNotExist:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			closing_datetime_seller = invoice_data["closing_datetime_seller"]
			if(not closing_datetime_seller):
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			# All checks passed
			invoice.closing_user_id_buyer = user
			invoice.closing_comment_buyer = request.data.get("closing_comment_buyer", "")
			invoice.closing_datetime_buyer = timezone.now()
			invoice.save()
		
		elif(not buyer and seller):
			# Checking the fields
			closing_user_buyer_id = invoice_data["closing_user_id_buyer"]
			try:
				closing_user_buyer_id = User.objects.get(user_id=closing_user_buyer_id)
			except User.DoesNotExist:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			closing_datetime_buyer = invoice_data["closing_datetime_buyer"]
			if(not closing_datetime_buyer):
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			# All checks passed
			invoice.closing_user_id_seller = user
			invoice.closing_comment_seller = request.data.get("closing_comment_seller", "")
			invoice.closing_datetime_seller = timezone.now()
			invoice.save()

		else:
			# The entity is neither this Invoice's seller nor buyer
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# All checks have passed and now the Invoice should be closed
		invoice.status = "closed"
		invoice.invoice_close_datetime = timezone.now()
		invoice.save()
		return Response(status=status.HTTP_200_OK)