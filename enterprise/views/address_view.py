from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.utils import timezone
from enterprise.models import * 
from enterprise.serializers import *
from enterprise.views.models_view import *

class address(APIView):
    def get(self, request, address_id):
        try:
            address = Address.objects.get(address_id=address_id)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, address_id):
        try:
            address = Address.objects.get(address_id=address_id)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if(not address.deleted_datetime):
            address.deleted_datetime = timezone.now()
            address.save()
            serializer = AddressSerializer(address)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class address_list(APIView):
    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        if(not isinstance(data, list)):
            data = [data]
        serializers = AddressSerializer(data=data, many=True)
        if(serializers.is_valid()):
            serializers.save()
            return Response(data = serializers.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class country_list(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CountrySerializer(data=request.data, many=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data = serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class entity_address(APIView):
    def get(self, request, entity_id):
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        entity_addresses = EntityAddress.objects.filter(entity_id=entity_id)
        addresses = []
        for entity_address in entity_addresses:
            address = entity_address.address_id
            if(not address.deleted_datetime):
                addresses.append(address)
        address_serializer = AddressSerializer(addresses, many=True)
        entity_address_serializer = EntityAddressSerializer(entity_addresses, many=True)
        combine_addresses = {}
        combine_addresses["addresses"] = address_serializer.data
        combine_addresses["entity_addresses"] = entity_address_serializer.data
        return Response(data=combine_addresses, status=status.HTTP_200_OK)

    def post(self, request, entity_id):
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data["entity_id"] = entity_id
        serializer = EntityAddressSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class entity_address_list(APIView):
    def get(self, request):
        entity_addresses = EntityAddress.objects.all()
        serializer = EntityAddressSerializer(entity_addresses, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EntityAddressSerializer(data=request.data, many=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)