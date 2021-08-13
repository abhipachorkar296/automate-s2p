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
from purchase_order.views.purchase_order import *

'''
Ongoing Tab = ["ongoing", "termination_requested"]
Draft tab = from draft table ["draft", "approval_pending"]
			from main table ["issued", "declined", "rescinded"]
Finised Tab = ["completed", "closed", "declined_and_reissued", "rescinded_and_reissued", "declined_and_closed", "rescinded_and_closed"]
'''

def user_buyer_side_purchase_order_list(user_id):
	'''
	Function for getting user purchase order list (buyer side) with status
	'''
	# Getting all the buyer id list
	buyer_id_list = list(Buyer.objects.filter(deleted_datetime__isnull=True).values_list("buyer_id", flat=True))
	# Getting all the current entity id list which is a buyer entity 
	# and having user with this user_id 
	user_buyer_entity_id_list = list(UserEntity.objects.filter(user_id=user_id, deleted_datetime__isnull=True, entity_id__in=buyer_id_list).values_list("entity_id", flat=True))
	# checking for all the draft purchase orders 
	draft_table_purchase_order_status_list = ["draft", "approval_pending"]
	draft_table_purchase_order_id_status_list = list(DraftPurchaseOrder.objects.filter(buyer_id__in=user_buyer_entity_id_list, status__in=draft_table_purchase_order_status_list).values_list("status", "purchase_order_id"))
	# checking for all the purchase orders 
	purchase_order_status_list = ["ongoing", "termination_requested", "issued", "declined", "rescinded", "completed", "closed", "declined_and_reissued", "rescinded_and_reissued", "declined_and_closed", "rescinded_and_closed"]
	purchase_order_id_status_list = list(PurchaseOrder.objects.filter(buyer_id__in=user_buyer_entity_id_list, status__in=purchase_order_status_list).values_list("status", "purchase_order_id"))

	user_purchase_order_status_id_list = draft_table_purchase_order_id_status_list + purchase_order_id_status_list
	return user_purchase_order_status_id_list

class buyer_purchase_order_tab_count(APIView):
	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		user_purchase_order_status_id_list = user_buyer_side_purchase_order_list(user_id)
		# Making hash map with status key and purchase_order counts as value
		status_count = defaultdict(int)
		for purchase_order_status, purchase_order_id in user_purchase_order_status_id_list:
			status_count[purchase_order_status] += 1

		status_corresponding_tab = {
			"completed": "Finished",
			"closed": "Finished",
			"declined_and_reissued": "Finished",
			"rescinded_and_reissued": "Finished",
			"declined_and_closed": "Finished",
			"rescinded_and_closed": "Finished",
			"draft": "Draft",
			"approval_pending": "Draft",
			"issued": "Draft",
			"declined": "Draft",
			"rescinded": "Draft",
			"termination_requested": "Ongoing",
			"ongoing": "Ongoing"
		}
		tab_count = defaultdict(dict)
		for purchase_order_status in status_count.keys():
			tab_count[status_corresponding_tab[purchase_order_status]][purchase_order_status] = status_count[purchase_order_status]

		return Response(data=tab_count, status=status.HTTP_200_OK)

class buyer_purchase_order_tab_info(APIView):
	def get(self, request, user_id, tab_name):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		user_purchase_order_status_id_list = user_buyer_side_purchase_order_list(user_id)
		purchase_order_status_list = []
		if(tab_name == "Ongoing"):
			purchase_order_status_list = ["ongoing", "termination_requested"]
		
		elif(tab_name == "Draft"):
			purchase_order_status_list = ["draft", "approval_pending", "issued", "declined", "rescinded"]

		elif(tab_name == "Finished"):
			purchase_order_status_list = ["completed", "closed", "declined_and_reissued", "rescinded_and_reissued", "declined_and_closed", "rescinded_and_closed"]
		
		else:
			purchase_order_status_list = ["ongoing", "termination_requested", "draft", "approval_pending", "issued", "declined", "rescinded", "completed", "closed", "declined_and_reissued", "rescinded_and_reissued", "declined_and_closed", "rescinded_and_closed"]


		purchase_order_id_list = [purchase_order_id for status, purchase_order_id in user_purchase_order_status_id_list if status in purchase_order_status_list]
		data = []
		request = HttpRequest()
		request.method = "GET"
		for purchase_order_id in purchase_order_id_list:
			response_purchase_order_info = purchase_order.as_view()(request,purchase_order_id)
			if(response_purchase_order_info.status_code == 200):
				data.append(response_purchase_order_info.data)
		
		return Response(data=data, status=status.HTTP_200_OK)

'''
Ongoing Tab = ["ongoing", "termination_requested"]
Received tab = ["issued", "declined", "rescinded"]
Finised Tab = ["completed", "closed", "declined_and_reissued", "rescinded_and_reissued", "declined_and_closed", "rescinded_and_closed"]
'''

def user_seller_side_purchase_order_list(user_id):
	'''
	Function for getting user purchase order list (seller side) with status
	'''
	# Getting all the seller id list
	seller_id_list = list(Seller.objects.filter(deleted_datetime__isnull=True).values_list("seller_id", flat=True))
	# Getting all the current entity id list which is a seller entity 
	# and having user with this user_id 
	user_seller_entity_id_list = list(UserEntity.objects.filter(user_id=user_id).filter(deleted_datetime__isnull=True).filter(entity_id__in=seller_id_list).values_list("entity_id", flat=True))
	# Checking all the real purchase orders which is ongoing
	purchase_order_status_list = ["ongoing", "termination_requested", "draft", "approval_pending", "issued", "declined", "rescinded", "completed", "closed", "declined_and_reissued", "rescinded_and_reissued", "declined_and_closed", "rescinded_and_closed"]
	purchase_order_id_status_list = list(PurchaseOrder.objects.filter(seller_id__in=user_seller_entity_id_list, status__in=purchase_order_status_list).values_list("status", "purchase_order_id"))

	user_purchase_order_status_id_list = purchase_order_id_status_list
	return user_purchase_order_status_id_list

class seller_purchase_order_tab_info(APIView):
	def get(self, request, user_id, tab_name):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		user_purchase_order_status_id_list = user_seller_side_purchase_order_list(user_id)
		purchase_order_status_list = []
		if(tab_name == "Ongoing"):
			purchase_order_status_list = ["ongoing", "termination_requested"]
		
		elif(tab_name == "Received"):
			purchase_order_status_list = ["issued", "declined", "rescinded"]

		elif(tab_name == "Finished"):
			purchase_order_status_list = ["completed", "closed", "declined_and_reissued", "rescinded_and_reissued", "declined_and_closed", "rescinded_and_closed"]
		
		else:
			purchase_order_status_list = ["ongoing", "termination_requested", "issued", "declined", "rescinded", "completed", "closed", "declined_and_reissued", "rescinded_and_reissued", "declined_and_closed", "rescinded_and_closed"]


		purchase_order_id_list = [purchase_order_id for status, purchase_order_id in user_purchase_order_status_id_list if status in purchase_order_status_list]
		data = []
		request = HttpRequest()
		request.method = "GET"
		for purchase_order_id in purchase_order_id_list:
			response_purchase_order_info = purchase_order.as_view()(request,purchase_order_id)
			if(response_purchase_order_info.status_code == 200):
				data.append(response_purchase_order_info.data)
		
		return Response(data=data, status=status.HTTP_200_OK)

class seller_purchase_order_tab_count(APIView):
	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		user_purchase_order_status_id_list = user_seller_side_purchase_order_list(user_id)
		# Making hash map with status key and purchase_order counts as value
		status_count = defaultdict(int)
		for purchase_order_status, purchase_order_id in user_purchase_order_status_id_list:
			status_count[purchase_order_status] += 1

		status_corresponding_tab = {
			"completed": "Finished",
			"closed": "Finished",
			"declined_and_reissued": "Finished",
			"rescinded_and_reissued": "Finished",
			"declined_and_closed": "Finished",
			"rescinded_and_closed": "Finished",
			"issued": "Received",
			"declined": "Received",
			"rescinded": "Received",
			"termination_requested": "Ongoing",
			"ongoing": "Ongoing"
		}
		tab_count = defaultdict(dict)
		for purchase_order_status in status_count.keys():
			tab_count[status_corresponding_tab[purchase_order_status]][purchase_order_status] = status_count[purchase_order_status]

		return Response(data=tab_count, status=status.HTTP_200_OK)