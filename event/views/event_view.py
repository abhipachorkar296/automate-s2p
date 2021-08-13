from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import requests
from django.urls import reverse
from django.utils import timezone
from enterprise.models import * 
from enterprise.serializers import *
from event.models import * 
from event.serializers import *

def get_absolute_uri(request, path_name, parameters_list):
    '''
    Get the Absolute URI from path_name and parameters_list
    '''
    return request.build_absolute_uri(reverse(path_name, args=parameters_list))

class draft_event(APIView):
    def get(self, request, event_id):
        try:
            event = DraftEvent.objects.get(event_id=event_id)
        except DraftEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DraftEventSerializer(event)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, event_id):
        try:
            event = DraftEvent.objects.get(event_id=event_id)
        except DraftEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = DraftEventSerializer(event, request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, event_id):
        try:
            event = DraftEvent.objects.get(event_id=event_id)
        except DraftEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response(status=status.HTTP_200_OK)

class draft_event_list(APIView):
    def get(self, request):
        events = DraftEvent.objects.all()
        serializer = DraftEventSerializer(events, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DraftEventSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data = serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class draft_event_item_info(APIView):
    def get(self, request, event_line_item_id):
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = DraftEventItemSerializer(draft_event_item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, event_line_item_id):
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = DraftEventItemSerializer(draft_event_item, request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, event_line_item_id):
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        draft_event_item.delete()
        return Response(status=status.HTTP_200_OK)

class draft_event_item_attribute(APIView):
    def get(self, request, event_line_item_id):
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        draft_event_item_attributes = draft_event_item.drafteventitemattribute_set.all()
        serializers = DraftEventItemAttributeSerializer(draft_event_item_attributes, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, event_line_item_id):
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        # Making the data in list format
        if(not isinstance(data, list)):
            data = [data]
        for attributes in data:
            attributes["event_line_item_id"] = event_line_item_id
        serializers = DraftEventItemAttributeSerializer(data=data, many=True)
        # Deleting all the previous attributes
        DraftEventItemAttribute.objects.filter(event_line_item_id=event_line_item_id).delete()
        if(serializers.is_valid()):
            # Saving with new attributes
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, event_line_item_id):
        # Same as POST method
        return self.post(request, event_line_item_id)

class draft_event_item_seller(APIView):
    def get(self, request, event_line_item_id):
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        draft_event_sellers = draft_event_item.drafteventitemseller_set.all()
        serializers = DraftEventItemSellerSerializer(draft_event_sellers, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, event_line_item_id):
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        # Making the data in list format
        if(not isinstance(data, list)):
            data = [data]
        for attributes in data:
            attributes["event_line_item_id"] = event_line_item_id
            attributes["event_id"] = draft_event_item.event_id.event_id
        serializers = DraftEventItemSellerSerializer(data=data, many=True)
        # Deleting all the previous sellers
        DraftEventItemSeller.objects.filter(event_line_item_id=event_line_item_id).delete()
        if(serializers.is_valid()):
            # Saving with new sellers
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, event_line_item_id):
        # Same as POST method
        return self.post(request, event_line_item_id)

class draft_event_item(APIView):
    def get(self, request, event_line_item_id):
        data = {}
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Getting Draft Event Item Info data
        serializer = DraftEventItemSerializer(draft_event_item)
        data["item_info"] = serializer.data

        # Getting Draft Event Item Attribute data
        draft_event_item_attributes = draft_event_item.drafteventitemattribute_set.all()
        serializers = DraftEventItemAttributeSerializer(draft_event_item_attributes, many=True)
        data["item_attribute"] = serializers.data

        return Response(data=data, status=status.HTTP_200_OK)
    
    def patch(self, request, event_line_item_id):
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        check = False # For checking if atleast one of item_info or item_attribute is present in request.data
        # Checking presence of item_info in request data
        try:
            event_item_info_data = request.data["item_info"]
            # If this line gets passed, means it is present
            # If present, it has to be able to patched, else Bad Request(meaning Bad Data)
            check = True
            response = requests.patch(get_absolute_uri(request, "event:draft_event_item_info", [event_line_item_id]), data=event_item_info_data)
            if(response.status_code != 200):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # item info not present, skip to item attribute
            pass

        # Checking presence of item_attribute in request.data
        try:
            event_item_attribute_data = request.data["item_attribute"]
            # If this line gets passed, means it is present
            # If present, it has to be able to patched, else Bad Request(meaning Bad Data)
            response = requests.patch(get_absolute_uri(request, "event:draft_event_item_attribute", [event_line_item_id]), json.dumps(event_item_attribute_data), headers = {'Content-type':'application/json'})
            if(response.status_code != 201):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            check = True
        except Exception as e:
            # item attribute not present
            pass
            
        if(check):
            # If atleast one of item_info or item_attribute present, return whole draft_event data
            # for getting the draft_event data, calling the get method
            response = self.get(request, event_line_item_id)
            return Response(data=response.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_line_item_id):
        try:
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
        except DraftEventItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        draft_event_item.delete()
        return Response(status=status.HTTP_200_OK)

class draft_event_item_list(APIView):
    def get(self, request, event_id):
        try:
            draft_event = DraftEvent.objects.get(event_id=event_id)
        except DraftEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        draft_event_items = draft_event.drafteventitem_set.all()
        serializers = DraftEventItemSerializer(draft_event_items, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, event_id):
        try:
            draft_event = DraftEvent.objects.get(event_id=event_id)
        except DraftEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Posting Draft Event Item Info
        try:
            event_item_info_data = request.data["item_info"]
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event_item_info_data["event_id"] = event_id
        data_to_return = {}
        serializer = DraftEventItemSerializer(data=event_item_info_data)
        if(serializer.is_valid()):
            serializer.save()
            # Getting the event_line_item_id for posting item attribute
            event_line_item_id = serializer.data.get("event_line_item_id")
            data_to_return["item_info"] = serializer.data
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Updating Draft Event Item Attribute
        try:
            event_item_attribute_data = request.data["item_attribute"]
        except Exception as e:
            return Response(data=data_to_return, status=status.HTTP_201_CREATED)
        response = requests.post(get_absolute_uri(request, path_name="event:draft_event_item_attribute", parameters_list=[event_line_item_id]), json.dumps(event_item_attribute_data), headers = {'Content-type':'application/json'})
        if(response.status_code==201):
            data_to_return["item_attribute"] = response.text
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class key_mapping(APIView):
    def get(self, reuqest):
        mappings = KeyMapping.objects.all()
        serializer = KeyMappingSerializer(mappings, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class draft_event_shift_event(APIView):
    def post(self, request, event_id):
        try:
            draft_event = DraftEvent.objects.get(event_id=event_id)
        except DraftEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        draft_event_info = DraftEventSerializer(draft_event).data
        draft_event_info["status"] = "ongoing"

        # Checking for the entry in keymapping for this event id
        try:
            key_mapping = KeyMapping.objects.get(draft_event_id=event_id)
            key_mapping_info = KeyMappingSerializer(key_mapping).data
            parent_event_id = key_mapping_info["event_id"]
            draft_event_info["parent_event_id"] = parent_event_id
        except KeyMapping.DoesNotExist:
            key_mapping = None

        # Shifting Draft Event Info to Event Info
        serializer = EventSerializer(data=draft_event_info)
        data_to_return = {}
        if(serializer.is_valid()):
            serializer.save()
            # Getting the actual event_id
            data_to_return["event_info"] = serializer.data
            actual_event_id = serializer.data.get("event_id")
            # Getting the actual event object with event_id
            actual_event = Event.objects.get(event_id=actual_event_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # Shifting Draft Event Item Info to Event Items Info
        draft_event_item_id_list = DraftEventItem.objects.filter(event_id=event_id).values_list("event_line_item_id", flat=True)
        item_list = []
        for event_line_item_id in draft_event_item_id_list:
            item = {}
            # Getting Draft Event Item and shifting to Actual Event Item
            draft_event_item = DraftEventItem.objects.get(event_line_item_id=event_line_item_id)
            draft_event_item_info = DraftEventItemSerializer(draft_event_item).data
            draft_event_item_info["event_id"] = actual_event_id
            serializer = EventItemSerializer(data=draft_event_item_info)
            if(serializer.is_valid()):
                serializer.save()
                item["item_info"] = serializer.data
                # Getting the actual event_line_item_id 
                actual_event_line_item_id = serializer.data.get("event_line_item_id")
            else:
                # Deleting the actual event created because the data is not satisfying constraints
                actual_event.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            # Getting Draft Event Item Attribute and shifting to Actual Event Item Attribute
            draft_event_item_attributes = DraftEventItemAttribute.objects.filter(event_line_item_id=event_line_item_id)
            draft_event_item_attributes_data = DraftEventItemAttributeSerializer(draft_event_item_attributes, many=True).data
            for attribute in draft_event_item_attributes_data:
                attribute["event_line_item_id"] = actual_event_line_item_id
            serializers = EventItemAttributeSerializer(data=draft_event_item_attributes_data, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_attribute"] = serializers.data
            else:
                actual_event.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)

            # Getting Draft Event Item Seller and shifting to Actual Event Item Seller    
            draft_event_item_sellers = DraftEventItemSeller.objects.filter(event_line_item_id=event_line_item_id)
            draft_event_item_sellers_data = DraftEventItemSellerSerializer(draft_event_item_sellers, many=True).data
            for seller in draft_event_item_sellers_data:
                seller["event_line_item_id"] = actual_event_line_item_id
                seller["event_id"] = actual_event_id
            serializers = EventItemSellerSerializer(data=draft_event_item_sellers_data, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_seller"] = serializers.data
            else:
                actual_event.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            item_list.append(item)
        
        data_to_return["event_item_list"] = item_list
        draft_event.delete()
        # Deleting the key_mapping obeject
        if(key_mapping != None):
            key_mapping.delete()
            parent_event = Event.objects.get(event_id=parent_event_id)
            parent_event.deleted_datetime = timezone.now()
            parent_event.save()
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class event_review_page(APIView):
    def get(self, request, event_id):
        request = HttpRequest()
        request.method = "GET"
        data = {}
        response_event_info = draft_event.as_view()(request,event_id)
        if(response_event_info.status_code == 200):
            data["event_info"] = response_event_info.data
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            event = DraftEvent.objects.get(event_id=event_id)
        except DraftEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        draft_event_items = event.drafteventitem_set.all()
        event_line_item_id_list = draft_event_items.values_list("event_line_item_id", flat=True)
        
        item_info_list = []
        for event_line_item_id in event_line_item_id_list:
            item_info = {}
            response_event_item_info = draft_event_item_info.as_view()(request, event_line_item_id)
            if(response_event_item_info.status_code == 200):
                item_info["item_info"] = response_event_item_info.data
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            response_event_item_attribute = draft_event_item_attribute.as_view()(request, event_line_item_id)
            if(response_event_item_attribute.status_code == 200):
                item_info["item_attribute"] = response_event_item_attribute.data
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            response_event_item_seller = draft_event_item_seller.as_view()(request, event_line_item_id)
            if(response_event_item_seller.status_code == 200):
                item_info["item_seller"] = response_event_item_seller.data
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            item_info_list.append(item_info)

        data["event_item_list"] = item_info_list
        return Response(data=data, status=status.HTTP_200_OK)

class event(APIView):
    
    def get(self, request, event_id):
        
        try:
            event_info = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        data["event_info"] = EventSerializer(event_info).data

        event_items = event_info.eventitem_set.all()
        event_line_item_id_list = event_items.values_list("event_line_item_id", flat=True)
        
        item_info_list = []
        for event_line_item_id in event_line_item_id_list:
            item_info = {}
            try:
                event_item_info = EventItem.objects.get(event_line_item_id=event_line_item_id)
            except EventItem.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer_item_info = EventItemSerializer(event_item_info)
            item_info["item_info"] = serializer_item_info.data

            
            event_item_attribute = EventItemAttribute.objects.filter(event_line_item_id=event_line_item_id)
            serializer_item_attribute = EventItemAttributeSerializer(event_item_attribute, many=True)
            item_info["item_attribute"] = serializer_item_attribute.data
            
            event_item_seller = EventItemSeller.objects.filter(event_line_item_id=event_line_item_id)
            serializer_item_seller = EventItemSellerSerializer(event_item_seller, many=True)
            item_info["item_seller"] = serializer_item_seller.data

            item_info_list.append(item_info)

        data["event_item_list"] = item_info_list
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        try:
            event_info_data = data["event_info"]
            serializer = EventSerializer(event, event_info_data, partial=True)
            if(serializer.is_valid()):
                serializer.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            pass
        event_line_item_id_list = list(event.eventitem_set.all().values_list("event_line_item_id", flat=True))
        try:
            event_item_list = data["event_item_list"]
        except Exception as e: 
            return Response(status=status.HTTP_200_OK)
        for event_item in event_item_list:
            item_info = event_item["item_info"]
            if(item_info["event_line_item_id"] not in event_line_item_id_list):
                break
            event_item = EventItem.objects.get(event_line_item_id=item_info["event_line_item_id"])
            serializer = DraftEventItemSerializer(event_item, item_info, partial=True)
            if(serializer.is_valid()):
                serializer.save()
                
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK)

class event_seller_status_change(APIView):
    def patch(self, request, event_id, seller_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            seller = Seller.objects.get(seller_id=seller_id)
        except Seller.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        time_now = timezone.now()
        if(event.deleted_datetime or event.event_end_datetime < time_now):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        event_item_seller_list = EventItemSeller.objects.filter(event_id=event_id, seller_id=seller_id)
        
        if(len(event_item_seller_list) == 0):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for event_item_seller in event_item_seller_list:
            invitation_status = request.data.get("invitation_status")
            event_item_seller.invitation_status = invitation_status
            event_item_seller.save()
        
        return Response(status=status.HTTP_200_OK)

class shift_event_draft_event(APIView):
    def post(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Checking whether draft event exists for this event
        try:
            key_mapping = KeyMapping.objects.get(event_id=event_id)
            return Response(data="draft event already exists")
        except KeyMapping.DoesNotExist:
            pass

        #shifting Event ot draft Event
        event_info = EventSerializer(event).data
        event_info["status"] = "paused"
        draft_serializer = DraftEventSerializer(data=event_info)
        data_to_return = {}
        
        if(draft_serializer.is_valid()):
            draft_serializer.save()
            data_to_return["draft_event_info"] = draft_serializer.data
            # Getting the draft Event id
            draft_event_id = draft_serializer.data.get("event_id")
            # Getting the Draft Event Object
            draft_event = DraftEvent.objects.get(event_id=draft_event_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # Shifting Event Item info to Draft Event Item info
        event_line_item_id_list = EventItem.objects.filter(event_id=event_id).values_list("event_line_item_id", flat=True)
        item_list = []
        for event_line_item_id in event_line_item_id_list:
            item = {}
            # Getting Event Item and shifting it to Draft Event Item
            event_item = EventItem.objects.get(event_line_item_id=event_line_item_id)
            event_item_info = EventItemSerializer(event_item).data
            event_item_info["event_id"] = draft_event_id
            serializer = DraftEventItemSerializer(data=event_item_info)
            if(serializer.is_valid()):
                serializer.save()
                item["draft_item_info"] = serializer.data
                # print(item)
                # Getting the draft event_line_item_id 
                draft_event_line_item_id = serializer.data.get("event_line_item_id")
            else:
                # Deleting the draft event created because the data is invalid
                draft_event.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            # Getting Event Item Attribute and shifting to Draft Event Item Attribute
            event_item_attributes = EventItemAttribute.objects.filter(event_line_item_id=event_line_item_id)
            event_item_attributes_data = EventItemAttributeSerializer(event_item_attributes, many=True).data
            for attribute in event_item_attributes_data:
                attribute["event_line_item_id"] = draft_event_line_item_id
            serializers = DraftEventItemAttributeSerializer(data=event_item_attributes_data, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_attribute"] = serializers.data
            else:
                draft_event.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)

            # Getting Event Item Seller and shifting to Draft Event Item Seller    
            event_item_sellers = EventItemSeller.objects.filter(event_line_item_id=event_line_item_id)
            event_item_sellers_data = EventItemSellerSerializer(event_item_sellers, many=True).data
            for seller in event_item_sellers_data:
                seller["event_line_item_id"] = draft_event_line_item_id
                seller["event_id"] = draft_event_id
            serializers = DraftEventItemSellerSerializer(data=event_item_sellers_data, many=True)
            if(serializers.is_valid()):
                serializers.save()
                item["item_seller"] = serializers.data
            else:
                draft_event.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)

            item_list.append(item)
        data_to_return["event_item_list"] = item_list
        
        # Saving data to KeyMapping table
        data = {}
        data["event_id"] = event_id
        data["draft_event_id"] = draft_event_id
        serializer = KeyMappingSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        #changing actual event status to paused
        event.status = "paused"
        event.save()

        return Response(data=data_to_return, status=status.HTTP_201_CREATED)
