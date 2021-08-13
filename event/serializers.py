from rest_framework import serializers
from event.models import *
from enterprise.models import *
from enterprise.serializers import *

class DraftEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftEvent
        fields = ["event_id", "enterprise_id", "buyer_id", "event_name", "event_type", "event_start_datetime", "event_end_datetime", "buyer_billing_address_id", "buyer_shipping_address_id", "event_delivery_datetime", "payment_terms_code", "created_by_user_id", "created_by_name", "created_by_phone", "created_by_email", "status", "last_modified_by_user_id"]

class DraftEventItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftEventItem
        fields = ["event_line_item_id", "event_id", "item_id", "buyer_item_id", "description", "measurement_unit_id", "meausrement_unit", "desired_quantity", "currency_code", "desired_price", "opening_bid", "total_amount", "allow_substitutes", "insurance_required", "post_to_global_market_place"]
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["currency_code"] = CurrencyCodeSerializer(instance.currency_code).data.get("currency_code")
        return response

class DraftEventItemAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftEventItemAttribute
        fields = ["event_line_item_id", "attribute_id", "attribute_value"]

class DraftEventItemSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftEventItemSeller
        fields = ["event_line_item_id", "event_id", "seller_id", "buyer_approval_required", "approved_by_buyer", "invitation_status"]

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["event_id", "parent_event_id", "enterprise_id", "buyer_id", "event_name", "event_type", "event_start_datetime", "event_end_datetime", "buyer_billing_address_id", "buyer_shipping_address_id", "event_delivery_datetime", "payment_terms_code", "created_by_user_id", "created_by_name", "created_by_phone", "created_by_email", "status", "last_modified_by_user_id", "created_datetime", "modified_datetime", "deleted_datetime"]

class EventItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventItem
        fields = ["event_line_item_id", "event_id", "item_id", "buyer_item_id", "description", "measurement_unit_id", "meausrement_unit", "desired_quantity", "currency_code", "desired_price", "opening_bid", "total_amount", "allow_substitutes", "insurance_required", "post_to_global_market_place"]
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["currency_code"] = CurrencyCodeSerializer(instance.currency_code).data.get("currency_code")
        return response

class EventItemAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventItemAttribute
        fields = ["event_line_item_id", "attribute_id", "attribute_value"]

class EventItemSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventItemSeller
        fields = ["event_line_item_id", "event_id", "seller_id", "buyer_approval_required", "approved_by_buyer", "invitation_status"]

class KeyMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyMapping
        fields = ["event_id", "draft_event_id"]

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'

class BidItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidItem
        fields = '__all__'
    
class BidItemTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidItemTax
        fields = '__all__'
    
class DraftBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftBid
        fields = '__all__'

class DraftBidItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftBidItem
        fields = '__all__'
    
class DraftBidItemTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftBidItemTax
        fields = '__all__'

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ["award_id", "parent_award_id", "event_id", "creator_user_id", "approver_user_id", "draft_purchase_order_id", "purchase_order_id", "buyer_id", "seller_id", "seller_bid_id", "award_creation_datetime", "payment_terms_code", "currency_code", "subtotal", "taxes", "total_shipping_cost", "total_other_charges", "bulk_discount_percentage", "bulk_discount_amount", "total", "deal_status", "created_datetime", "modified_datetime", "deleted_datetime"]

class AwardItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardItem
        fields = ["award_line_item_id", "award_id", "event_line_item_id", "measurement_unit_id", "quantity_offered", "quantity_awarded", "currency_code", "price", "other_charges", "shipping_managed_by", "shipping_cost", "total_amount"]
    
class AwardItemTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardItemTax
        fields = ["award_line_item_id", "tax_name", "value"]

class DraftAwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftAward
        fields = ["award_id", "parent_award_id", "event_id", "creator_user_id", "approver_user_id", "draft_purchase_order_id", "purchase_order_id", "buyer_id", "seller_id", "seller_bid_id", "award_creation_datetime", "payment_terms_code", "currency_code", "subtotal", "taxes", "total_shipping_cost", "total_other_charges", "bulk_discount_percentage", "bulk_discount_amount", "total", "deal_status", "created_datetime", "modified_datetime", "deleted_datetime"]

class DraftAwardItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftAwardItem
        fields = ["award_line_item_id", "award_id", "event_line_item_id", "measurement_unit_id", "quantity_offered", "quantity_awarded", "currency_code", "price", "other_charges", "shipping_managed_by", "shipping_cost", "total_amount"]
    
class DraftAwardItemTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftAwardItemTax
        fields = ["award_line_item_id", "tax_name", "value"]