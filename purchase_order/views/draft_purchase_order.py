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

class draft_purchase_order(APIView):
    def get(self, request, purchase_order_id):
        try:
            purchase_order = DraftPurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
        except DraftPurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data_to_return = {}
        data_to_return["purchase_order_info"] = DraftPurchaseOrderSerializer(purchase_order).data

        buyer_information = DraftPurchaseOrderBuyerInformation.objects.filter(purchase_order_id=purchase_order_id)
        data_to_return["purchase_order_buyer_information"] = DraftPurchaseOrderBuyerInformationSerializer(buyer_information, many=True).data

        seller_information = DraftPurchaseOrderSellerInformation.objects.filter(purchase_order_id=purchase_order_id)
        data_to_return["purchase_order_seller_information"] = DraftPurchaseOrderSellerInformationSerializer(seller_information, many=True).data
        
        purchase_order_items = purchase_order.draftpurchaseorderitem_set.all()
        purchase_order_line_item_id_list = purchase_order_items.values_list("purchase_order_line_item_id", flat=True)

        item_list = []
        for purchase_order_line_item_id in purchase_order_line_item_id_list:
            item = {}
            purchase_order_item = DraftPurchaseOrderItem.objects.get(purchase_order_line_item_id=purchase_order_line_item_id)
            item["item_info"] = DraftPurchaseOrderItemSerializer(purchase_order_item).data
            purchase_order_item_charge = DraftPurchaseOrderItemCharge.objects.filter(purchase_order_line_item_id=purchase_order_line_item_id)
            item_charge = DraftPurchaseOrderItemChargeSerializer(purchase_order_item_charge, many=True).data
            item["item_charge"] = item_charge
            purchase_order_item_attribute = DraftPurchaseOrderItemAttribute.objects.filter(purchase_order_line_item_id=purchase_order_line_item_id)
            item["item_attribute"] = DraftPurchaseOrderItemAttributeSerializer(purchase_order_item_attribute, many=True).data
            item_list.append(item)
        
        data_to_return["purchase_order_item_list"] = item_list
        return Response(data=data_to_return, status=status.HTTP_200_OK)
    
    def patch(self, request, purchase_order_id):
        try:
            purchase_order = DraftPurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
        except DraftPurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data_to_return = {}
        data = request.data
        purchase_order_info_data = data["purchase_order_info"]
        serializer = DraftPurchaseOrderSerializer(purchase_order, data=purchase_order_info_data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["purchase_order_info"] = serializer.data
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        buyer_information_list = data.get("purchase_order_buyer_information",[])
        for buyer_info in buyer_information_list:
            buyer_info["purchase_order_id"] = purchase_order_id
        buyer_information_object = DraftPurchaseOrderBuyerInformation.objects.filter(purchase_order_id=purchase_order_id)
        buyer_information_object.delete()
        if(len(buyer_information_list) > 0):
            serializers = DraftPurchaseOrderBuyerInformationSerializer(data=buyer_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["purchase_order_buyer_information"] = serializers.data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["purchase_order_buyer_information"] = []
        seller_information_list = data.get("purchase_order_seller_information",[])
        for seller_info in seller_information_list:
            seller_info["purchase_order_id"] = purchase_order_id
        seller_information_object = DraftPurchaseOrderSellerInformation.objects.filter(purchase_order_id=purchase_order_id)
        seller_information_object.delete()
        if(len(seller_information_list) > 0):
            serializers = DraftPurchaseOrderSellerInformationSerializer(data=seller_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["purchase_order_seller_information"] = serializers.data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["purchase_order_seller_information"] = []
        #deleting previous items and charges
        purchase_order_items = purchase_order.draftpurchaseorderitem_set.all()
        purchase_order_items.delete()
        
        #posting new data
        purchase_order_item_list = data["purchase_order_item_list"]
        item_list = []
        for item_data in purchase_order_item_list:
            item = {}
            item_info_data = item_data["item_info"]
            item_info_data["purchase_order_id"] = purchase_order_id
            serializer = DraftPurchaseOrderItemSerializer(data=item_info_data)
            if(serializer.is_valid()):
                serializer.save()
                item["item_info"] = serializer.data
                purchase_order_line_item_id = serializer.data.get("purchase_order_line_item_id")
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_charge_list = item_data["item_charge"]
            for item_charge in item_charge_list:
                item_charge["purchase_order_line_item_id"] = purchase_order_line_item_id
            serializers = DraftPurchaseOrderItemChargeSerializer(data=item_charge_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_charge"] = serializers.data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_attribute_list = item_data["item_attribute"]
            for item_attribute in item_attribute_list:
                item_attribute["purchase_order_line_item_id"] = purchase_order_line_item_id
            serializers = DraftPurchaseOrderItemAttributeSerializer(data=item_attribute_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_attribute"] = serializers.data
            else:
                purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_list.append(item)
        
        data_to_return["purchase_order_item_list"] = item_list
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)
    
    def delete(self, request, purchase_order_id):
        try:
            purchase_order = DraftPurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
        except DraftPurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        purchase_order.delete()
        return Response(status=status.HTTP_200_OK)

class draft_purchase_order_list(APIView):
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

        try:
            purchase_order = DraftPurchaseOrder.objects.get(event_id=event_id, seller_id=seller_id)
        except DraftPurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request = HttpRequest()
        request.method = "GET"
        data = {}
        response_draft_purchase_order = draft_purchase_order.as_view()(request,purchase_order.purchase_order_id)
        if(response_draft_purchase_order.status_code == 200):
            data = response_draft_purchase_order.data
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(data=data, status=status.HTTP_200_OK)


    def post(self, request, event_id, seller_id):
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

        # Getting the latest award for checking weather its status is decline or not 
        existing_award_check = Award.objects.filter(event_id=event_id, seller_id=seller_id)
        if(existing_award_check):
            latest_award_id_status = max(list(Award.objects.filter(event_id=event_id, seller_id=seller_id).values_list("award_id", "deal_status")), key=lambda award: award[0])
            latest_award_status = latest_award_id_status[1]
            if(latest_award_status == "decline"):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        data_to_return = {}
        data = request.data
        purchase_order_info_data = data["purchase_order_info"]
        purchase_order_info_data["event_id"] = event_id
        purchase_order_info_data["seller_id"] = seller_id
        serializer = DraftPurchaseOrderSerializer(data=purchase_order_info_data)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["purchase_order_info"] = serializer.data
            purchase_order_id = serializer.data.get("purchase_order_id")
            purchase_order = DraftPurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        buyer_information_list = data.get("purchase_order_buyer_information",[])
        if(len(buyer_information_list) > 0):
            for buyer_information in buyer_information_list:
                buyer_information["purchase_order_id"] = purchase_order_id
            serializers = DraftPurchaseOrderBuyerInformationSerializer(data=buyer_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["purchase_order_buyer_information"] = serializers.data
            else:
                purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["purchase_order_seller_information"] = []
        seller_information_list = data.get("purchase_order_seller_information",[])
        if(len(seller_information_list) > 0):
            for seller_information in seller_information_list:
                seller_information["purchase_order_id"] = purchase_order_id
                seller_information["seller_id"] = seller_id
            serializers = DraftPurchaseOrderSellerInformationSerializer(data=seller_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["purchase_order_seller_information"] = serializers.data
            else:
                purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["purchase_order_seller_information"] = []
        
        purchase_order_item_list = data["purchase_order_item_list"]
        item_list = []
        for item_data in purchase_order_item_list:
            item = {}
            item_info_data = item_data["item_info"]
            item_info_data["purchase_order_id"] = purchase_order_id
            serializer = DraftPurchaseOrderItemSerializer(data=item_info_data)
            if(serializer.is_valid()):
                serializer.save()
                item["item_info"] = serializer.data
                purchase_order_line_item_id = serializer.data.get("purchase_order_line_item_id")
            else:
                purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_charge_list = item_data["item_charge"]
            for item_charge in item_charge_list:
                item_charge["purchase_order_line_item_id"] = purchase_order_line_item_id
            serializers = DraftPurchaseOrderItemChargeSerializer(data=item_charge_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_charge"] = serializers.data
            else:
                purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_attribute_list = item_data["item_attribute"]
            for item_attribute in item_attribute_list:
                item_attribute["purchase_order_line_item_id"] = purchase_order_line_item_id
            serializers = DraftPurchaseOrderItemAttributeSerializer(data=item_attribute_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_attribute"] = serializers.data
            else:
                purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_list.append(item)
        
        data_to_return["purchase_order_item_list"] = item_list
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class shift_purchase_order_to_draft_purchase_order(APIView):
    def makeNUll(self, data):
        data["closing_user_id_buyer"] = None
        data["closing_comment_buyer"] = ""
        data["closing_datetime_buyer"] = None
        data["closing_user_id_seller"] = None
        data["closing_comment_seller"] = ""
        data["closing_datetime_seller"] = None
        data["modified_datetime"] = None
        data["purchase_order_close_datetime"] = None
        data["buyer_comments"] = ""
        data["seller_acknowledgement_user_id"] = None
        data["seller_acknowledgement_datetime"] = None

    def post(self, request, purchase_order_id):
        try:
            purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data_to_return = {}
        purchase_order_info_data = PurchaseOrderSerializer(purchase_order).data
        purchase_order_info_data["status"] = "draft"
        self.makeNUll(purchase_order_info_data)
        serializer = DraftPurchaseOrderSerializer(data=purchase_order_info_data)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["purchase_order_info"] = serializer.data
            draft_purchase_order_id = serializer.data.get("purchase_order_id")
            draft_purchase_order = DraftPurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        purchase_order_buyer_information = PurchaseOrderBuyerInformation.objects.filter(purchase_order_id=purchase_order_id)
        buyer_information_list = PurchaseOrderBuyerInformationSerializer(purchase_order_buyer_information, many=True).data
        if(len(buyer_information_list) > 0):
            for buyer_information in buyer_information_list:
                buyer_information["purchase_order_id"] = draft_purchase_order_id
            serializers = DraftPurchaseOrderBuyerInformationSerializer(data=buyer_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["purchase_order_buyer_information"] = serializers.data
            else:
                draft_purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["purchase_order_seller_information"] = []
        
        purchase_order_seller_information = PurchaseOrderSellerInformation.objects.filter(purchase_order_id=purchase_order_id)
        seller_information_list = PurchaseOrderSellerInformationSerializer(purchase_order_seller_information, many=True).data
        if(len(seller_information_list) > 0):
            for seller_information in seller_information_list:
                seller_information["purchase_order_id"] = draft_purchase_order_id
            serializers = DraftPurchaseOrderSellerInformationSerializer(data=seller_information_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["purchase_order_seller_information"] = serializers.data
            else:
                draft_purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            data_to_return["purchase_order_seller_information"] = []
        
        purchase_order_items = PurchaseOrderItem.objects.filter(purchase_order_id=purchase_order_id)
        purchase_order_item_list = PurchaseOrderItemSerializer(purchase_order_items, many=True).data
        item_list = []
        for item_info_data in purchase_order_item_list:
            item = {}
            item_info_data["purchase_order_id"] = draft_purchase_order_id
            serializer = DraftPurchaseOrderItemSerializer(data=item_info_data)
            if(serializer.is_valid()):
                serializer.save()
                item["item_info"] = serializer.data
                draft_purchase_order_line_item_id = serializer.data.get("purchase_order_line_item_id")
            else:
                draft_purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_charges = PurchaseOrderItemCharge.objects.filter(purchase_order_line_item_id=item_info_data["purchase_order_line_item_id"])
            item_charge_list = PurchaseOrderItemChargeSerializer(item_charges, many=True).data
            for item_charge in item_charge_list:
                item_charge["purchase_order_line_item_id"] = draft_purchase_order_line_item_id
            serializers = DraftPurchaseOrderItemChargeSerializer(data=item_charge_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_charge"] = serializers.data
            else:
                draft_purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_attributes = PurchaseOrderItemAttribute.objects.filter(purchase_order_line_item_id=item_info_data["purchase_order_line_item_id"])
            item_attribute_list = PurchaseOrderItemAttributeSerializer(item_attributes, many=True).data
            for item_attribute in item_attribute_list:
                item_attribute["purchase_order_line_item_id"] = draft_purchase_order_line_item_id
            serializers = DraftPurchaseOrderItemAttributeSerializer(data=item_attribute_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_attribute"] = serializers.data
            else:
                draft_purchase_order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_list.append(item)
        data = {}
        data["purchase_order_id"] = purchase_order_id
        data["draft_purchase_order_id"] = draft_purchase_order_id
        serializer = PurchaseOrderKeyMappingSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
        else:
            draft_purchase_order.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data_to_return["purchase_order_item_list"] = item_list
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)