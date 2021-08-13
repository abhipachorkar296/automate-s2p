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

class draft_bid_info(APIView):
    def get(self, request, bid_id):
        try:
            bid = DraftBid.objects.get(bid_id=bid_id)
        except DraftBid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DraftBidSerializer(bid)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, bid_id):
        try:
            bid = DraftBid.objects.get(bid_id=bid_id)
        except DraftBid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        bid.delete()
        return Response(status=status.HTTP_200_OK)

class draft_bid_info_list(APIView):
    def get(self, request):
        bids = DraftBid.objects.all()
        serializer = DraftBidSerializer(bids, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class draft_bid_item(APIView):

    def get(self, request, bid_line_item_id):
        try:
            draft_bid_item = DraftBidItem.objects.get(bid_line_item_id=bid_line_item_id)
        except DraftBidItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = DraftBidItemSerializer(draft_bid_item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class draft_bid_item_tax(APIView):
    def get(self, request, bid_line_item_id):
        bid_item_taxes = DraftBidItemTax.objects.filter(bid_line_item_id=bid_line_item_id)
        serializer = DraftBidItemTaxSerializer(bid_item_taxes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class draft_bid(APIView):
    def get(self, request, bid_id):
        request = HttpRequest()
        request.method = "GET"
        data = {}
        response_bid_info = draft_bid_info.as_view()(request,bid_id)
        if(response_bid_info.status_code==200):
            data["bid_info"] = response_bid_info.data

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            draft_bid = DraftBid.objects.get(bid_id=bid_id)
        except DraftBid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        draft_bid_items = draft_bid.draftbiditem_set.all()
        bid_line_item_id_list = draft_bid_items.values_list("bid_line_item_id", flat=True)
        
        item_info_list = []
        for bid_line_item_id in bid_line_item_id_list:
            item_info = {}
            response_bid_item = draft_bid_item.as_view()(request, bid_line_item_id)
            if(response_bid_item.status_code == 200):
                item_info["item_info"] = response_bid_item.data
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            response_event_item_tax = draft_bid_item_tax.as_view()(request, bid_line_item_id)
            if(response_event_item_tax.status_code == 200):
                item_info["item_tax"] = response_event_item_tax.data
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            item_info_list.append(item_info)

        data["bid_item_list"] = item_info_list
        return Response(data=data, status=status.HTTP_200_OK)
    
    def patch(self, request, bid_id):
        try:
            draft_bid = DraftBid.objects.get(bid_id=bid_id)
        except DraftBid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        abs_url = request.build_absolute_uri(reverse("event:post_draft_bid_list", args=[draft_bid.event_id.event_id]))
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(abs_url, data=json.dumps(request.data), headers=headers)
        if(response.status_code == 201):
            draft_bid.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=response.text, status=status.HTTP_201_CREATED)
        
class draft_bid_list(APIView):
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
            bid = DraftBid.objects.get(event_id=event_id, seller_id=seller_id)
        except DraftBid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request = HttpRequest()
        request.method = "GET"
        data = {}
        response_bid = draft_bid.as_view()(request,bid.bid_id)
        if(response_bid.status_code==200):
            data = response_bid.data
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, event_id, seller_id=None):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data_to_return = {}
        item_data = data["bid_info"]
        item_data["event_id"] = event_id
        serializer = DraftBidSerializer(data=item_data)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["bid_info"] = serializer.data
            bid_id = serializer.data.get("bid_id")
            draft_bid = DraftBid.objects.get(bid_id=bid_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        item_info_list = data["bid_item_list"]
        bid_item_list = []

        for item_info in item_info_list:
            bid_item = {}
            item = item_info["item_info"]
            item["bid_id"] = bid_id
            serializer = DraftBidItemSerializer(data=item)
            if(serializer.is_valid()):
                serializer.save()
                bid_item["item_info"] = serializer.data
                bid_line_item_id = serializer.data.get("bid_line_item_id")
            else:
                draft_bid.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            item_tax = item_info["item_tax"]
            for tax in item_tax:
                tax["bid_line_item_id"] = bid_line_item_id
            serializer = DraftBidItemTaxSerializer(data=item_tax, many=True)
            if(serializer.is_valid()):
                serializer.save()
                bid_item["item_tax"] = serializer.data
            else:
                draft_bid.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            bid_item_list.append(bid_item)
        
        data_to_return["bid_item_list"] = bid_item_list        
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class draft_bid_shift_bid(APIView):
    def post(self, request, bid_id):
        try:
            draft_bid = DraftBid.objects.get(bid_id=bid_id)
        except DraftBid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data_to_return = {}
        draft_bid_info = DraftBidSerializer(draft_bid).data
        serializer = BidSerializer(data=draft_bid_info)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["bid_info"] = serializer.data
            acutal_bid_id = serializer.data.get("bid_id")
            bid = Bid.objects.get(bid_id=bid_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        bid_item_list = []
        draft_bid_line_item_list = DraftBidItem.objects.filter(bid_id=bid_id).values_list("bid_line_item_id", flat=True)

        for bid_line_item_id in draft_bid_line_item_list:
            bid_item = {}
            draft_bid_item = DraftBidItem.objects.get(bid_line_item_id=bid_line_item_id)
            draft_bid_item_info = DraftBidItemSerializer(draft_bid_item).data
            draft_bid_item_info["bid_id"] = acutal_bid_id
            serializer = BidItemSerializer(data=draft_bid_item_info)
            if(serializer.is_valid()):
                serializer.save()
                bid_item["item_info"] = serializer.data
                actual_bid_line_item_id = serializer.data.get("bid_line_item_id")
            else:
                bid.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            draft_bid_item_tax = DraftBidItemTax.objects.filter(bid_line_item_id=bid_line_item_id)
            draft_bid_item_tax_list = DraftBidItemTaxSerializer(draft_bid_item_tax, many=True).data
            for draft_bid_item_tax in draft_bid_item_tax_list:
                draft_bid_item_tax["bid_line_item_id"] = actual_bid_line_item_id
            serializer = BidItemTaxSerializer(data=draft_bid_item_tax_list, many=True)
            if(serializer.is_valid()):
                serializer.save()
                bid_item["item_tax"] = serializer.data
            else:
                bid.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)

            bid_item_list.append(bid_item)
        
        data_to_return["bid_item_list"] = bid_item_list
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class bid_info(APIView):
    def get(self, request, bid_id):
        try:
            bid = Bid.objects.get(bid_id=bid_id)
        except Bid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BidSerializer(bid)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class bid_info_list(APIView):
    def get(self, request):
        bids = Bid.objects.all()
        serializer = BidSerializer(bids, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class bid_item(APIView):
    def get(self, request, bid_line_item_id):
        try:
            bid_item = BidItem.objects.get(bid_line_item_id=bid_line_item_id)
        except BidItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BidItemSerializer(bid_item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class bid_item_list(APIView):
    def get(self, request, bid_id):
        bid_items = BidItem.objects.filter(bid_id=bid_id)
        serializer = BidItemSerializer(bid_items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class bid_item_tax(APIView):
    def get(self, request, bid_line_item_id):
        bid_item_taxes = BidItemTax.objects.filter(bid_line_item_id=bid_line_item_id)
        serializer = BidItemTaxSerializer(bid_item_taxes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class bid(APIView):
    def get(self, request, bid_id):
        request = HttpRequest()
        request.method = "GET"
        data = {}
        response_bid_info = bid_info.as_view()(request,bid_id)
        if(response_bid_info.status_code == 200):
            data["bid_info"] = response_bid_info.data
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            bid = Bid.objects.get(bid_id=bid_id)
        except Bid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        bid_items = bid.biditem_set.all()
        bid_line_item_id_list = bid_items.values_list("bid_line_item_id", flat=True)
        
        item_info_list = []
        for bid_line_item_id in bid_line_item_id_list:
            item_info = {}
            response_bid_item = bid_item.as_view()(request, bid_line_item_id)
            if(response_bid_item.status_code == 200):
                item_info["item_info"] = response_bid_item.data
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            response_event_item_tax = bid_item_tax.as_view()(request, bid_line_item_id)
            if(response_event_item_tax.status_code == 200):
                item_info["item_tax"] = response_event_item_tax.data
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            item_info_list.append(item_info)

        data["bid_item_list"] = item_info_list
        return Response(data=data, status=status.HTTP_200_OK)
    
    def patch(self, request, bid_id):
        try:
            bid = Bid.objects.get(bid_id=bid_id)
        except Bid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        stat = request.data.get("status")
        if(not bid.deleted_datetime):
            bid.status = stat
            bid.save()
            return Response(status=status.HTTP_200_OK)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, bid_id):
        try:
            bid = Bid.objects.get(bid_id=bid_id)
        except Bid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if(not bid.deleted_datetime):
            bid.deleted_datetime = timezone.now()
            bid.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class bid_list(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        bid_list = Bid.objects.filter(event_id=event_id, bid_creator_entity_type ='S', deleted_datetime__isnull=True)
        seller_id_list = defaultdict(lambda : 0)
        for current_bid in bid_list:
            seller_id_list[current_bid.seller_id] = max(seller_id_list[current_bid.seller_id], current_bid.bid_id)
        bid_list = []
        for seller in seller_id_list.keys():
            current_bid = Bid.objects.get(bid_id = seller_id_list[seller])
            bid_list.append(current_bid)
        
        request = HttpRequest()
        request.method = "GET"
        data = []
        for current_bid in bid_list:
            response_bid_info = bid.as_view()(request,current_bid.bid_id)
            if(response_bid_info.status_code == 200):
                data.append(response_bid_info.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(data=data, status=status.HTTP_200_OK)
    
    def post(self, request, event_id):
        big_data = request.data
        if(not isinstance(big_data, list)):
            big_data = [big_data]
        return_data = []
        for data in big_data:
            data_to_return = {}
            item_data = data["bid_info"]
            item_data["event_id"] = event_id
            serializer = BidSerializer(data=item_data)
            if(serializer.is_valid()):
                serializer.save()
                data_to_return["bid_info"] = serializer.data
                bid_id = serializer.data.get("bid_id")
                bid = Bid.objects.get(bid_id=bid_id)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            item_info_list = data["bid_item_list"]
            bid_item_list = []

            for item_info in item_info_list:
                bid_item = {}
                item = item_info["item_info"]
                item["bid_id"] = bid_id
                serializer = BidItemSerializer(data=item)
                if(serializer.is_valid()):
                    serializer.save()
                    bid_item["item_info"] = serializer.data
                    bid_line_item_id = serializer.data.get("bid_line_item_id")
                else:
                    bid.delete()
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                item_tax = item_info["item_tax"]
                for tax in item_tax:
                    tax["bid_line_item_id"] = bid_line_item_id
                serializer = BidItemTaxSerializer(data=item_tax, many=True)
                if(serializer.is_valid()):
                    serializer.save()
                    bid_item["item_tax"] = serializer.data
                else:
                    bid.delete()
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                bid_item_list.append(bid_item)
            
            data_to_return["bid_item_list"] = bid_item_list
            return_data.append(data_to_return)

        return Response(data=return_data, status=status.HTTP_201_CREATED)

class lastest_bid(APIView):
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
            event_item_seller = EventItemSeller.objects.get(seller_id=seller_id)
        except EventItemSeller.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        bid_list = Bid.objects.filter(event_id=event_id, seller_id=seller_id, deleted_datetime__isnull=True)
        bid_list_info = BidSerializer(bid_list,many=True).data
        max_bid_id = 0
        for bid_object in bid_list_info:
            max_bid_id = max(max_bid_id, bid_object["bid_id"])
        
        request = HttpRequest()
        request.method = "GET"
        response_bid_info = bid.as_view()(request,max_bid_id)
        if(response_bid_info.status_code == 200):
            data = response_bid_info.data
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(data=data, status=status.HTTP_200_OK)

class seller_bid_history(APIView):
    def get(self, request, event_id, seller_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            seller = Seller.objects.get(seller_id=seller_id)
        except Seller.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        bid_list = Bid.objects.filter(event_id=event_id, seller_id=seller_id)
        if(len(bid_list)==0):
            return Response(status=status.HTTP_404_NOT_FOUND)
        data_to_return = []
        request = HttpRequest()
        request.method = "GET"
        for current_bid in bid_list:
            response_bid_info = bid.as_view()(request,current_bid.bid_id)
            if(response_bid_info.status_code == 200):
                data_to_return.append(response_bid_info.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        return Response(data=data_to_return, status=status.HTTP_200_OK)

class buyer_bid_history(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item_seller_list = EventItemSeller.objects.filter(event_id=event_id)
        seller_id_list = defaultdict(lambda : 0)
        for seller in item_seller_list:
            seller_id_list[seller.seller_id] = 1
        
        data_to_return = []
        request = HttpRequest()
        request.method = "GET"
        for seller_id in seller_id_list:
            response_bid_info = seller_bid_history.as_view()(request,event_id,seller_id)
            if(response_bid_info.status_code == 200):
                data_to_return.append(response_bid_info.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        return Response(data=data_to_return, status=status.HTTP_200_OK)