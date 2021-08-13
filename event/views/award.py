from django.urls.base import resolve
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
from event.views import event
from purchase_order.models import *


class hello(APIView):
	'''
	For Welcoming :)
	'''
	def get(self, request):
		data = {
			"query": "Hello Ongoing World"
		}
		return Response(data=data, status=status.HTTP_200_OK)

def make_list_from_dict(status_event_id_list):
	'''
	For accumulating event_id into a list for every status
	'''
	status_corresponding_event_id_dict = defaultdict(list)
	for status, event_id in status_event_id_list:
		status_corresponding_event_id_dict[status].append(event_id)
	return status_corresponding_event_id_dict

def user_buyer_side_event_tab_status_event_id_list(user_id):
	'''
	Function for getting user event list (buyer side) with status
	'''
	# Getting all the buyer id list
	buyer_id_list = list(Buyer.objects.filter(deleted_datetime__isnull=True).values_list("buyer_id", flat=True))
	# Getting all the current entity id list which is a buyer entity 
	# and having user with this user_id 
	user_buyer_entity_id_list = list(UserEntity.objects.filter(user_id=user_id).filter(deleted_datetime__isnull=True).filter(entity_id__in=buyer_id_list).values_list("entity_id", flat=True))
	# Checking all the real event which is ongoing
	ongoing_event_id_status_list = list(Event.objects.filter(buyer_id__in=user_buyer_entity_id_list, deleted_datetime__isnull=True).values_list("status", "event_id"))

	for i in range(len(ongoing_event_id_status_list)):
		event_status, event_id = ongoing_event_id_status_list[i]
		event_object = Event.objects.get(event_id=event_id)
		# Taking the event status as "Award Pending" which has ended and no 
		# corresponding award is there
		if(event_object.event_end_datetime<=timezone.now() and not Award.objects.filter(event_id=event_id).exists()):
			ongoing_event_id_status_list[i] = ("Award Pending", event_id)

	# Checking all the real event which is finsihed
	finished_event_status_list = ["Completed", "Terminated"]
	finished_event_id_status_list = list(Event.objects.filter(buyer_id__in=user_buyer_entity_id_list, deleted_datetime__isnull=False, status__in=finished_event_status_list).values_list("status", "event_id"))
	# Checking all the draft event along with removing those draft events 
	# which is related to a paused event
	draft_event_id_in_key_mapping_list = list(KeyMapping.objects.all().values_list("draft_event_id", flat=True))
	draft_event_id_status_list = list(DraftEvent.objects.filter(buyer_id__in=user_buyer_entity_id_list).exclude(event_id__in=draft_event_id_in_key_mapping_list).values_list("status", "event_id"))
	
	'''
	STATUS NAME				:		TAB NAME

	"Draft"					: 		"Draft",
	"Ongoing"				: 		"Ongoing",
	"Event Paused"			: 		"Ongoing",
	"Award Pending"			: 		"Ongoing",
	"Award Pending Approval": 		"Ongoing",
	"PO Pending"			: 		"Ongoing"
	"Completed"				: 		"Finished",
	"Terminated"			: 		"Finished",
	'''
	# Making the has map corresponding to each tab
	tab_count = defaultdict(list)
	tab_count["Draft"] = draft_event_id_status_list
	tab_count["Ongoing"] = ongoing_event_id_status_list
	tab_count["Finished"] = finished_event_id_status_list
	
	return tab_count

class buyer_event_tab_count(APIView):

	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Calling the function for getting tab and corresponding (status, event_id) list
		user_buyer_side_event_tab_dict = user_buyer_side_event_tab_status_event_id_list(user_id)
		'''
		Structure of user_buyer_side_event_tab_dict coming from function 
		user_buyer_side_event_tab_status_event_id_list will be
		the following:
		{
			tab1: {
				[[status1, event_id_1], [status1, event_id_2], [status2, event_id_3]]
			},
			tab2: {
				[[status3, event_id_4], [status4, event_id_5]]
			}
		}
		'''

		# Converting the (status, event_id) of every tab to dict form
		'''
		Structure of user_buyer_side_event_tab_dict after below operation will become like the following:
		{
			tab1: {
				status1: [event_id_1, event_id_2],
				status2: [event_id_3]
			},
			tab2: {
				status3: [event_id_4],
				status4: [event_id_5]
			}
		}
		'''
		for tab, tab_status_id_list in user_buyer_side_event_tab_dict.items():
			user_buyer_side_event_tab_dict[tab] = make_list_from_dict(tab_status_id_list)
		
		user_buyer_tab_count = {}
		'''
		Structure of user_buyer_tab_count after below operation will become like the following:
		{
			tab1: {
				status1: 2,
				status2: 1
			},
			tab2: {
				status3: 1,
				status4: 1
			}
		}
		'''
		for tab in user_buyer_side_event_tab_dict.keys():
			tab_status_count = {}
			for tab_status, tab_status_event_id_list in user_buyer_side_event_tab_dict[tab].items():
				tab_status_count[tab_status] = len(tab_status_event_id_list)

			user_buyer_tab_count[tab] = tab_status_count

		return Response(data=user_buyer_tab_count, status=status.HTTP_200_OK)

def user_buyer_tab_event_id_list(user_id, tab):
	'''
	For getting the event_id list for buyer side correspoding to a tab
	'''
	# Getting all the tab counts of the user_id for buyer side using 
	# function user_buyer_side_event_tab_status_event_id_list
	user_buyer_side_event_tab_dict = user_buyer_side_event_tab_status_event_id_list(user_id)
	'''
	Structure of user_buyer_side_event_tab_dict coming from function 
	user_buyer_side_event_tab_status_event_id_list will be
	the following:
	{
		tab1: {
			[[status1, event_id_1], [status1, event_id_2], [status2, event_id_3]]
		},
		tab2: {
			[[status3, event_id_4], [status4, event_id_5]]
		}
	}
	'''
	tab_event_status_id_list = []
	'''
	Structure of tab_event_status_id_list after below operation
	[[status1, event_id_1], [status2, event_id_2], ....]
	'''

	if(tab=="All"):
		for tab_name, tab_value in user_buyer_side_event_tab_dict.items():
			tab_event_status_id_list.extend(tab_value)
	else:
		# Rest of the tabs
		tab_event_status_id_list = user_buyer_side_event_tab_dict.get(tab, [])
	
	# Removing status from the elements of tab_event_status_id_list
	tab_event_id_list = [event_id for status, event_id in tab_event_status_id_list]

	return tab_event_id_list

class buyer_event_draft_tab(APIView):
	'''
	Draft Tab in buyer Event Dashboard
	'''
	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Getting all the event_id list for this tab
		tab_event_id_list = user_buyer_tab_event_id_list(user_id, "Draft")

		# Fetching event review data for every event
		data_to_return = []
		for event_id in tab_event_id_list:
			request = HttpRequest()
			request.method = "GET"
			response = event.as_view()(request, event_id)
			if(response.status_code==200):
				data_to_return.append(response.data)
		
		return Response(data=data_to_return, status=status.HTTP_200_OK)

class buyer_event_ongoing_tab(APIView):
	'''
	Ongoing Tab in buyer Event Dashboard
	'''
	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Getting all the event_id list for this tab
		tab_event_id_list = user_buyer_tab_event_id_list(user_id, "Ongoing")

		# Fetching event review data for every event
		data_to_return = []
		for event_id in tab_event_id_list:
			request = HttpRequest()
			request.method = "GET"
			response = event.as_view()(request, event_id)
			if(response.status_code==200):
				data_to_return.append(response.data)
		
		return Response(data=data_to_return, status=status.HTTP_200_OK)

class buyer_event_finished_tab(APIView):
	'''
	Finished Tab in buyer Event Dashboard
	'''
	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Getting all the event_id list for this tab
		tab_event_id_list = user_buyer_tab_event_id_list(user_id, "Finished")

		# Fetching event review data for every event
		data_to_return = []
		for event_id in tab_event_id_list:
			request = HttpRequest()
			request.method = "GET"
			response = event.as_view()(request, event_id)
			if(response.status_code==200):
				data_to_return.append(response.data)
		
		return Response(data=data_to_return, status=status.HTTP_200_OK)

def remove_event_versions(event_seller_id_list):
	'''
	Function for removing event_versions from a list containing elements in the 
	form of (event_id, seller_id)
	'''
	# Using Topological sort for ordering event versioning
	# Here for the topological sort, the latest event_id
	# (event eith highest event_id in corresponding event component) will come first 
	# So for doing topological sort for the latest events, 
	# normal sorting in decreasing order will work.
	event_seller_id_list.sort(key=lambda x:x[0], reverse=True)
	visited = defaultdict(bool)
	event_latest_version_id_list = []
	for event_id, seller_id in event_seller_id_list:
		curr_event = EventSerializer(Event.objects.get(event_id=event_id)).data
		parent_event_id = curr_event.get("parent_event_id")
		# Marking the parent event version of the current event as visited
		visited[parent_event_id] = True
		if(not visited[event_id]):
			# This is the latest event version of the corresponding event component
			visited[event_id] = True
			event_latest_version_id_list.append([event_id, seller_id])

	return event_latest_version_id_list

def user_seller_side_event_tab_status_event_id_list(user_id):
	'''
	Function for getting user event list (seller side) with status for all the tabs 
	on seller side
	'''
	# Getting all the seller id list
	seller_id_list = list(Seller.objects.filter(deleted_datetime__isnull=True).values_list("seller_id", flat=True))
	# Getting all the current entity id list which is a seller entity 
	# and having user with this user_id
	user_seller_entity_id_list = list(UserEntity.objects.filter(user_id=user_id).filter(deleted_datetime__isnull=True).filter(entity_id__in=seller_id_list).values_list("entity_id", flat=True))
	# Getting all the events(ongoing+versions+finished+invited) having this seller
	user_seller_entity_event_id_list = list(set(EventItemSeller.objects.filter(seller_id__in=user_seller_entity_id_list).values_list("event_id", "seller_id")))
	# Remove the event versions from this list
	unique_event_seller_id_list = remove_event_versions(user_seller_entity_event_id_list)
	# Making a dict with key as event_id ans seller_id
	unique_event_seller_id_dict = dict(unique_event_seller_id_list)
	# Making a event_id list from these unique_event_seller_id_list
	unique_event_id_list = [event_id for event_id, seller_id in unique_event_seller_id_list]

	'''
	STATUS NAME 								: TAB NAME

	"Invited (Event Started/Yet to Start)"		: "Invited",
	"Event Paused"								: "Invited/Ongoing"(Depending on the timing action of response from seller),
	"Response Submitted"						: "Ongoing",
	"Response Due"								: "Ongoing",
	"Counterbid Received"						: "Ongoing",
	"Counterbid Accepted"						: "Ongoing",
	"Deal Awarded"								: "Ongoing",
	"Deal Accepted"								: "Ongoing/Decision",
	"Deal Rejected"								: "Ongoing",
	"Event Ended"								: "Decision",
	"Deal Lost"									: "Decision",
	"Rejected"									: "Decision",
	'''

	''' 
	Getting all the invited or rejected events for Invitation Tab
	- (invited): when not accepted and event is going on
	- (rejected): when rejected the event or event has ended and didn't accept or reject
	- (Event Ended): When the event ends
	'''

	invited_rejected_status_list = ["Invited, Rejected"]
	invited_rejected_event_status_id_list = list(set(EventItemSeller.objects.filter(event_id__in=unique_event_id_list, invitation_status__in=invited_rejected_status_list).values_list("invitation_status", "event_id")))
	event_type_seller_side_status = {
		"RFQ": "Event Started",
		"Auction": "Yet to Start"
	}
	# For storing tuple (status, event_id) corresponding to every tab
	tab_count = defaultdict(list)
	tab_count["Invited"] = []
	tab_count["Ongoing"] = []
	tab_count["Decision"] = []
	
	for event in invited_rejected_event_status_id_list:
		if(event[0]=="Invited"):
			curr_tab = "Invited"
			# For Invited Status for Seller, show the status of the corresponding Event
			if(Event.objects.filter(event_id=event[1]).exists()):
				event_object = Event.objects.get(event_id=event[1])
				# If the event has not been closed then the status will
				# be the event status depending on the event type
				event[0] = event_type_seller_side_status[event_object.type]
				# Check if the event is paused
				if(event_object.status=="Event Paused"):
					event[0] = "Event Paused"
				# Check if the event has ended
				if(event_object.event_end_datetime<=timezone.now()):
					curr_tab = "Decision"
					event[0] = "Event Ended"
		else:
			# Rejected
			curr_tab = "Decision"

		# Storing in the curr_tab Key with (status, event_id)
		tab_count[curr_tab].append([event[0], event[1]])

	'''
	Getting all the Accepted and Decision Tab Events
	This section includes all the events having invitation status as "Accepted" 
	- (Event Paused): When the event is paused
	- (Response Due): When the event is going on and seller has not submitted any bid
	- (Response Submitted): When there is a real bid submitted by seller
	- (Counterbid Received): When the buyer makes a counterbid
	- (Counterbid Accepted): When the seller accepts the counterbid
	- (Deal Awarded): When the buyer awards the seller
	- (Deal Accepted): When the seller accepts the awarded deal
	- (Deal Rejected): When the seller rejects the awarded deal
	- (Event Ended): If no bid submitted and event has ended
	- (Deal Awarded): If the deal awarded
	- (Deal Lost): If the event is completed/closed and the seller is not awarded
	- PO statuses have to be added
	'''

	# invited_rejected_event_status_id_list will be a subset of unique_event_id_list
	accepted_event_id_list = list(set(unique_event_id_list).difference(set(event_id[1] for event_id in invited_rejected_event_status_id_list)))
	for event_id in accepted_event_id_list:
		seller_id = unique_event_seller_id_dict[event_id]
		event_object = Event.objects.get(event_id=event_id)
		status = ""

		# Check if the event has completed/closed
		if(event_object.deleted_datetime!=None and  event_object.deleted_datetime<=timezone.now()):
			# Check if there is a award with deleted_datetime=Null
			existing_award_check = Award.objects.get(event_id=event_id, seller_id=seller_id, deleted_datetime_isnull=True)
			curr_tab = "Decision"
			if(existing_award_check):
				'''
				- (Deal Accepted): When the seller accepts the awarded deal
				'''
				status = "Deal Accepted"
			else:
				'''
				- (Deal Lost): If the event is completed/closed and no award is accepted
				'''
				status = "Deal Lost"
		else:
			# Event is ongoing
			curr_tab = "Ongoing"
			# Check if the event has ended
			if(event_object.event_end_datetime<=timezone.now()):
				'''
				This section checks for the event status based on the award if present.
				'''
				existing_award_check = Award.objects.filter(event_id=event_id, seller_id=seller_id).exists()
				if(existing_award_check):
					'''
					- (Deal Awarded): When the buyer awards the seller
					- (Deal Accepted): When the seller accepts the awarded deal
					- (Deal Rejected): When the seller rejects the awarded deal
					'''
					# Getting the latest award
					latest_award_id_status = max(list(Award.objects.filter(event_id=event_id, seller_id=seller_id).values_list("award_id", "deal_status")), key=lambda award: award[0])
					latest_award_status = latest_award_id_status[1]
					status = latest_award_status
				else:
					'''
					- (Event Ended): When the event ends
					'''
					status = "Event Ended"
			else:
				'''
				This section checks for the event status based on looking in Bid Table.
				'''
				existing_bid_check = Bid.objects.filter(event_id=event_id, seller_id=seller_id).exists()
				# Response Submitted (including case for counterbid rejected) + Counterbid Received + Counterbid Accepted
				if(existing_bid_check):
					latest_bid_id_status = max(list(Bid.objects.filter(event_id=event_id, seller_id=seller_id).values_list("bid_id", "status")), key=lambda bid: bid[0])
					latest_bid_object = Bid.objects.get(bid_id=latest_bid_id_status[0])
					latest_bid_status = latest_bid_id_status[1]
					if(latest_bid_status=="Counterbid Rejected"):
						'''
						- (Counterbid Rejected): When the seller rejects the counterbid
						For counterbid rejected, status shown will be "Response Submitted"
						'''
						status = "Response Submitted"
					else:
						'''
						- (Response Submitted): When there is a real bid submitted by seller
						- (Counterbid Received): When the buyer makes a counterbid
						- (Counterbid Accepted): When the seller accepts the counterbid
						'''
						status = latest_bid_status
						# Check if the latest bid is submitted by Seller side and
						# that bid is deleted
						if(latest_bid_object.deleted_datetime):
							status = "Response Due"

				# Response Due
				else:
					'''
					- (Response Due): When the event is going on and seller has not submitted any bid
					'''
					status = "Response Due"
				
				# Event Paused
				if(event_object.status=="Event Paused"):
					status = "Event Paused"
		# Storing in the curr_tab (Decision/Ongoing Tab) Key with (status, event_id)
		tab_count[curr_tab].append([status, event_id])

	return tab_count

class seller_event_tab_count(APIView):

	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Calling the function for getting tab and corresponding (status, event_id) list
		user_seller_side_event_tab_dict = user_seller_side_event_tab_status_event_id_list(user_id)
		'''
		Structure of user_seller_side_event_tab_dict coming from function 
		user_seller_side_event_tab_status_event_id_list will be
		the following:
		{
			tab1: {
				[[status1, event_id_1], [status1, event_id_2], [status2, event_id_3]]
			},
			tab2: {
				[[status3, event_id_4], [status4, event_id_5]]
			}
		}
		'''

		# Converting the (status, event_id) of every tab to dict form
		'''
		Structure of user_seller_side_event_tab_dict after below operation will become like the following:
		{
			tab1: {
				status1: [event_id_1, event_id_2],
				status2: [event_id_3]
			},
			tab2: {
				status3: [event_id_4],
				status4: [event_id_5]
			}
		}
		'''
		for tab, tab_status_id_list in user_seller_side_event_tab_dict.items():
			user_seller_side_event_tab_dict[tab] = make_list_from_dict(tab_status_id_list)
		
		user_seller_tab_count = {}
		'''
		Structure of user_seller_tab_count after below operation will become like the following:
		{
			tab1: {
				status1: 2,
				status2: 1
			},
			tab2: {
				status3: 1,
				status4: 1
			}
		}
		'''
		for tab in user_seller_side_event_tab_dict.keys():
			tab_status_count = {}
			for tab_status, tab_status_event_id_list in user_seller_side_event_tab_dict[tab].items():
				tab_status_count[tab_status] = len(tab_status_event_id_list)

			user_seller_tab_count[tab] = tab_status_count

		return Response(data=user_seller_tab_count, status=status.HTTP_200_OK)

def user_seller_tab_event_id_list(user_id, tab):
	'''
	For getting the event_id list for seller side correspoding to a tab
	'''
	# Getting all the tab counts of the user_id for seller side using 
	# function user_seller_side_event_tab_status_event_id_list
	user_seller_side_event_tab_dict = user_seller_side_event_tab_status_event_id_list(user_id)
	'''
	Structure of user_seller_side_event_tab_dict coming from function 
	user_seller_side_event_tab_status_event_id_list will be
	the following:
	{
		tab1: {
			[[status1, event_id_1], [status1, event_id_2], [status2, event_id_3]]
		},
		tab2: {
			[[status3, event_id_4], [status4, event_id_5]]
		}
	}
	'''
	tab_event_status_id_list = []
	'''
	Structure of tab_event_status_id_list after below operation
	[[status1, event_id_1], [status2, event_id_2], ....]
	'''

	if(tab=="All"):
		for tab_name, tab_value in user_seller_side_event_tab_dict.items():
			tab_event_status_id_list.extend(tab_value)
	else:
		# Rest of the tabs
		tab_event_status_id_list = user_seller_side_event_tab_dict.get(tab, [])
	
	# Removing status from the elements of tab_event_status_id_list
	tab_event_id_list = [event_id for status, event_id in tab_event_status_id_list]

	return tab_event_id_list

class seller_event_invited_tab(APIView):
	'''
	Invited Tab in Seller Event Dashboard
	'''
	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Getting all the event_id list for this tab
		tab_event_id_list = user_seller_tab_event_id_list(user_id, "Invited")

		# Fetching event review data for every event
		data_to_return = []
		for event_id in tab_event_id_list:
			request = HttpRequest()
			request.method = "GET"
			response = event.as_view()(request, event_id)
			if(response.status_code==200):
				data_to_return.append(response.data)
		
		return Response(data=data_to_return, status=status.HTTP_200_OK)

class seller_event_ongoing_tab(APIView):
	'''
	Ongoing Tab in Seller Event Dashboard
	'''
	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Getting all the event_id list for this tab
		tab_event_id_list = user_seller_tab_event_id_list(user_id, "Ongoing")

		# Fetching event review data for every event
		data_to_return = []
		for event_id in tab_event_id_list:
			request = HttpRequest()
			request.method = "GET"
			response = event.as_view()(request, event_id)
			if(response.status_code==200):
				data_to_return.append(response.data)
		
		return Response(data=data_to_return, status=status.HTTP_200_OK)

class seller_event_decision_tab(APIView):
	'''
	Decision Tab in Seller Event Dashboard
	'''
	def get(self, request, user_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Getting all the event_id list for this tab
		tab_event_id_list = user_seller_tab_event_id_list(user_id, "Decision")

		# Fetching event review data for every event
		data_to_return = []
		for event_id in tab_event_id_list:
			request = HttpRequest()
			request.method = "GET"
			response = event.as_view()(request, event_id)
			if(response.status_code==200):
				data_to_return.append(response.data)
		
		return Response(data=data_to_return, status=status.HTTP_200_OK)

class award(APIView):

	def get(self, request, award_id):
		'''
		For getting an award
		'''
		try:
			award = Award.objects.get(award_id=award_id)
		except Award.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		data_to_return = {}
		award_info = AwardSerializer(award).data
		data_to_return["award_info"] = award_info
		award_item_list = AwardItem.objects.filter(award_id=award_id)
		item_list = []
		for award_item in award_item_list:
			item = {}
			item["item_info"] = AwardItemSerializer(award_item).data
			award_line_item_id = award_item.award_line_item_id
			award_item_tax_list = AwardItemTax.objects.filter(award_line_item_id=award_line_item_id)
			item["item_tax"] = AwardItemTaxSerializer(award_item_tax_list, many=True).data
			item_list.append(item)
		data_to_return["award_item_list"] = item_list
	
		return Response(data=data_to_return, status=status.HTTP_200_OK)
	
	def patch(self, request, award_id):
		'''
		For Patching an award
		(Only Status Change is expected here)
		'''
		try:
			award = Award.objects.get(award_id=award_id)
		except Award.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		deal_status = request.data.get("deal_status", "")
		event = award.event_id
		if(not award.deleted_datetime and not event.deleted_datetime and deal_status!=""):
			award.deal_status = deal_status
			award.save()
			return Response(status=status.HTTP_200_OK)
		return Response(status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, award_id):
		'''
		For deleting an award
		'''
		try:
			award = Award.objects.get(award_id=award_id)
		except Award.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if(not award.deleted_datetime):
			award.deleted_datetime = timezone.now()
			award.save()
			return Response(status=status.HTTP_200_OK)
		return Response(status=status.HTTP_400_BAD_REQUEST)

class award_new_version(APIView):
	
	def post(self, request, parent_award_id):
		'''
		For posting a new version of the award
		'''
		try:
			award = Award.objects.get(award_id=parent_award_id)
		except Award.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		original_event = EventSerializer(award.event_id).data
		original_seller = SellerSerializer(award.seller_id).data

		if(award.deleted_datetime or original_event["deleted_datetime"]):
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		data_to_return = {}
		award_data = request.data.copy()
		award_info = award_data.get("award_info")
		award_info["parent_award_id"] = parent_award_id

		# Checking if this award involves the original event only
		if(original_event["event_id"]!=award_info.get("event_id")):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		# Checking if this award involves the original seller only
		if(original_seller["seller_id"]!=award_info.get("seller_id")):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		award_item_list = award_data.get("award_item_list")
		serializer = AwardSerializer(data=award_info)
		if(serializer.is_valid()):
			serializer.save()
			data_to_return["award_info"] = serializer.data
			curr_award_id = serializer.data.get("award_id")
			curr_award = Award.objects.get(award_id=curr_award_id)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		item_list = []
		for item in award_item_list:
			curr_item_data = {}
			item_info = item.get("item_info")
			item_tax = item.get("item_tax")
			item_info["award_id"] = curr_award_id
			serializer = AwardItemSerializer(data=item_info)
			if(serializer.is_valid()):
				serializer.save()
				curr_item_data["item_info"] = serializer.data
				award_line_item_id = serializer.data.get("award_line_item_id")
				award_item = AwardItem.objects.get(award_line_item_id=award_line_item_id)
			else:
				curr_award.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
			for tax in item_tax:
				tax["award_line_item_id"] = award_line_item_id
			
			serializers = AwardItemTaxSerializer(data=item_tax, many=True)
			if(serializers.is_valid()):
				serializers.save()
				curr_item_data["item_tax"] = serializers.data
			else:
				curr_award.delete()
				award_item.delete()
				return Response(status=status.HTTP_400_BAD_REQUEST)
			item_list.append(curr_item_data)
		data_to_return["award_item_list"] = item_list
		award.deleted_datetime = timezone.now()
		award.save()
		return Response(data=data_to_return, status=status.HTTP_201_CREATED)

def remove_award_versions(award_id_list):
	'''
	Function for removing the award versions from a award_id list
	'''
	award_id_list.sort(reverse=True)
	visited = defaultdict(bool)
	unique_award_id_list = []
	for award_id in award_id_list:
		curr_award = Award.objects.get(award_id=award_id)
		parent_award_id = AwardSerializer(curr_award).data.get("parent_award_id")
		visited[parent_award_id] = True
		if(not visited[award_id]):
			visited[award_id] = True
			unique_award_id_list.append(award_id)
	
	return unique_award_id_list

class award_list(APIView):

	def get(self, request, event_id):
		try:
			event = Event.objects.get(event_id=event_id)
		except Event.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		event_award_id_list = list(Award.objects.filter(event_id=event_id).values_list("award_id", flat=True))
		unique_award_id_list = remove_award_versions(event_award_id_list)
		data_to_return = []
		for award_id in unique_award_id_list:
			request = HttpRequest()
			request.method = "GET"
			curr_award = award.as_view()(request, award_id)
			data_to_return.append(curr_award.data)
		return Response(data=data_to_return, status=status.HTTP_200_OK)
	
	def post(self, request, event_id):
		try:
			event = Event.objects.get(event_id=event_id)
		except Event.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		if(event.deleted_datetime):
			# If event is deleted then give a bad request
			return Response(status=status.HTTP_400_BAD_REQUEST)
		data = request.data.copy()
		if(not isinstance(data, list)):
			data = [data]
		data_to_return = []
		for award_data in data:
			curr_award_data = {}
			award_info = award_data.get("award_info")
			award_item_list = award_data.get("award_item_list", [])

			# If there is no award item, then return bad request
			if(len(award_item_list)==0):
				return Response(status=status.HTTP_400_BAD_REQUEST)

			award_info["event_id"] = event_id
			serializer = AwardSerializer(data=award_info)
			if(serializer.is_valid()):
				serializer.save()
				curr_award_data["award_info"] = serializer.data
				award_id = serializer.data.get("award_id")
				award = Award.objects.get(award_id=award_id)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			item_list = []
			for item in award_item_list:
				curr_item_data = {}
				item_info = item.get("item_info")
				item_tax = item.get("item_tax", [])
				item_info["award_id"] = award_id
				serializer = AwardItemSerializer(data=item_info)
				if(serializer.is_valid()):
					serializer.save()
					curr_item_data["item_info"] = serializer.data
					award_line_item_id = serializer.data.get("award_line_item_id")
					award_item = AwardItem.objects.get(award_line_item_id=award_line_item_id)
				else:
					award.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
				for tax in item_tax:
					tax["award_line_item_id"] = award_line_item_id
				
				serializers = AwardItemTaxSerializer(data=item_tax, many=True)
				if(serializers.is_valid()):
					serializers.save()
					curr_item_data["item_tax"] = serializers.data
				else:
					award.delete()
					award_item.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
				item_list.append(curr_item_data)
			curr_award_data["award_item_list"] = item_list
			data_to_return.append(curr_award_data)

		return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class draft_award_list(APIView):
	
	def get(self, request, event_id):
		try:
			event = Event.objects.get(event_id=event_id)
		except Event.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		draft_award_list = DraftAward.objects.filter(event_id=event_id)
		data_to_return = []
		for draft_award in draft_award_list:
			draft_award_data = {}
			draft_award_data["award_info"] = DraftAwardSerializer(draft_award).data
			draft_award_id = draft_award.award_id
			draft_award_item_list = DraftAwardItem.objects.filter(award_id=draft_award_id)
			item_list = []
			for draft_award_item in draft_award_item_list:
				item = {}
				item["item_info"] = DraftAwardItemSerializer(draft_award_item).data
				draft_award_line_item_id = draft_award_item.award_line_item_id
				item_tax = DraftAwardItemTax.objects.filter(award_line_item_id=draft_award_line_item_id)
				item["item_tax"] = DraftAwardItemTaxSerializer(item_tax, many=True).data
				item_list.append(item)

			draft_award_data["award_item_list"] = item_list
			data_to_return.append(draft_award_data)
		return Response(data=data_to_return, status=status.HTTP_200_OK)
		
	def post(self, request, event_id):
		try:
			event = Event.objects.get(event_id=event_id)
		except Event.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if(event.deleted_datetime):
			# If event is deleted then give a bad request
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# # Also check if there is not any real award for the event
		# if(Award.objects.filter(event_id=event_id).exists()):
		# 	return Response(status=status.HTTP_400_BAD_REQUEST)

		draft_award_list = request.data.copy()
		if(not isinstance(draft_award_list, list)):
			draft_award_list = [draft_award_list]

		all_previous_draft_award_list = DraftAward.objects.filter(event_id=event_id)
		all_previous_draft_award_list.delete()

		data_to_return = []
		for award_data in draft_award_list:
			curr_award_data = {}
			award_info = award_data.get("award_info")
			award_item_list = award_data.get("award_item_list", [])
			award_info["event_id"] = event_id
			serializer = DraftAwardSerializer(data=award_info)
			if(serializer.is_valid()):
				serializer.save()
				curr_award_data["award_info"] = serializer.data
				award_id = serializer.data.get("award_id")
				award = DraftAward.objects.get(award_id=award_id)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			item_list = []
			for item in award_item_list:
				curr_item_data = {}
				item_info = item.get("item_info", [])
				item_tax = item.get("item_tax", [])
				item_info["award_id"] = award_id
				serializer = DraftAwardItemSerializer(data=item_info)
				if(serializer.is_valid()):
					serializer.save()
					curr_item_data["item_info"] = serializer.data
					award_line_item_id = serializer.data.get("award_line_item_id")
					award_item = DraftAwardItem.objects.get(award_line_item_id=award_line_item_id)
				else:
					award.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
				for tax in item_tax:
					tax["award_line_item_id"] = award_line_item_id

				serializers = DraftAwardItemTaxSerializer(data=item_tax, many=True)
				if(serializers.is_valid()):
					serializers.save()
					curr_item_data["item_tax"] = serializers.data
				else:
					award.delete()
					award_item.delete()
					return Response(status=status.HTTP_400_BAD_REQUEST)
				item_list.append(curr_item_data)
			curr_award_data["award_item_list"] = item_list
			data_to_return.append(curr_award_data)
		return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class draft_award_list_shift_award(APIView):

	def post(self, request, event_id):
		try:
			event = Event.objects.get(event_id=event_id)
		except Event.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		data_request = HttpRequest()
		data_request.method = "GET"
		draft_award_list_data = draft_award_list.as_view()(data_request, event_id).data
		abs_url = request.build_absolute_uri(reverse("event:award_list", args=[event_id]))
		headers = {
			'Content-Type': 'application/json'
		}
		response = requests.post(abs_url, data=json.dumps(draft_award_list_data), headers=headers)
		if(response.status_code==201):
			draft_award_list_object = DraftAward.objects.filter(event_id=event_id)
			draft_award_list_object.delete()
			return Response(data=response.text, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)

class award_history(APIView):

	def get(self, request, event_id, seller_id=None):
		try:
			event = Event.objects.get(event_id=event_id)
		except Event.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# Get all the seller of the event
		seller_id_list = list(set(EventItemSeller.objects.filter(event_id=event_id).values_list("seller_id", flat=True)))

		# Check if the seller if sent is valid or not
		if(seller_id!=None):
			try:
				seller = Seller.objects.get(seller_id=seller_id)
			except Seller.DoesNotExist:
				return Response(status=status.HTTP_404_NOT_FOUND)
		
			if(seller_id not in seller_id_list):
				# Seller doesn't exist in event
				return Response(status=status.HTTP_400_BAD_REQUEST)
			else:
				data_to_return = self.seller_event_award_history(event_id, seller_id)
		
		else:
			data_to_return = []
			for seller_id in seller_id_list:
				seller_data_to_return = self.seller_event_award_history(event_id, seller_id)
				# Checking if the seller has at least one award history or not
				if(len(seller_data_to_return)!=0):
					data_to_return.append(seller_data_to_return)

		return Response(data=data_to_return, status=status.HTTP_200_OK)

	def seller_event_award_history(self, event_id, seller_id):
		'''
		Method for getting award history of a seller for an event
		'''
		# It is preassumed that event_id and seller_id are valid
		award_id_list = list(Award.objects.filter(event_id=event_id, seller_id=seller_id).values_list("award_id", flat=True))
		# Sorting from latest award award to oldest
		award_id_list.sort(reverse=True)
		data_to_return = []
		for award_id in award_id_list:
			request = HttpRequest()
			request.method = "GET"
			award_data = award.as_view()(request, award_id)
			if(award_data.status_code==200):
				data_to_return.append(award_data.data)
		return data_to_return

class decline_award(APIView):

	def patch(self, request, user_id, award_id):
		try:
			user = User.objects.get(user_id=user_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		try:
			award = Award.objects.get(award_id=award_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		seller_id = AwardSerializer(award).data["seller_id"]
		try:
			user_entity = UserEntity.objects.get(user_id=user_id, seller_id=seller_id, deleted_datetime__isnull=True)
		except UserEntity.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		event = award.event_id
		if(not award.deleted_datetime and not event.deleted_datetime):
			award.deal_status = "declined"
			award.deleted_datetime = timezone.now()
			award.save()
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		
		# Checking if any Purchase Order exists
		latest_purchase_order = PurchaseOrder.objects.filter(event_id=event.event_id, seller_id=seller_id, purchase_order_close_datetime__isnull=True)
		if(latest_purchase_order.exists()):
			purchase_order = latest_purchase_order[0]
			purchase_order.seller_acknowledgement_user_id = user
			purchase_order.seller_acknowledgement_datetime = timezone.now()
			purchase_order.closing_user_id_seller = user
			purchase_order.closing_datetime_seller = timezone.now()
			purchase_order.status = "declined"
			purchase_order.purchase_order_close_datetime = timezone.now()
			purchase_order.save()
		
		return Response(status=status.HTTP_200_OK)