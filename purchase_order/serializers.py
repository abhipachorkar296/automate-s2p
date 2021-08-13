from rest_framework import serializers
from .models import *

class PurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ['purchase_order_id', 'event_id', 'purchase_order_creation_datetime', 'buyer_id', 'buyer_purchase_order_id', 'buyer_entity_name', 'buyer_billing_address_id', 'buyer_shipping_address_id', 'buyer_approver_user_id', 'buyer_approver_name', 'buyer_contact_user_id', 'buyer_contact_name', 'buyer_contact_phone', 'buyer_contact_email', 'is_freight_purchase_order', 'seller_id', 'seller_entity_name', 'seller_address_id', 'seller_contact_user_id', 'seller_contact_name', 'seller_contact_phone', 'seller_contact_email', 'seller_acknowledgement_user_id', 'seller_acknowledgement_datetime', 'delivery_schedule_type', 'payment_terms_code', 'purchase_order_discount_percentage', 'buyer_comments', 'status', 'reissue_draft_purchase_order_id', 'reissue_purchase_order_id', 'closing_user_id_buyer', 'closing_comment_buyer', 'closing_datetime_buyer', 'closing_user_id_seller', 'closing_comment_seller', 'closing_datetime_seller', 'modified_datetime', 'purchase_order_close_datetime']

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['purchase_order_line_item_id', 'purchase_order_id', 'item_id', 'buyer_item_id', 'buyer_item_name', 'buyer_item_description', 'due_date', 'currency_code', 'measurement_unit_id', 'rate', 'quantity', 'max_acceptable_quantity', 'measurement_unit_alternate_id', 'rate_alternate', 'quantity_alternate', 'taxes_and_charges_percentage', 'taxes_and_charges_value', 'total_order_value', 'shipping_per_unit']

class PurchaseOrderItemChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItemCharge
        fields = ['purchase_order_line_item_id', 'charge_name', 'charge_type', 'charge_percentage']

class PurchaseOrderItemAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItemAttribute
        fields = ['purchase_order_line_item_id', 'attribute_id', 'attribute_value']

class EntityIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityIdentification
        fields = ['identification_id', 'entity_id', 'identification_name', 'identification_category', 'identification_value', 'created_datetime', 'modified_datetime', 'deleted_datetime']

class EntityPurchaseOrderDefaultIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityPurchaseOrderDefaultIdentification
        fields = ['entity_id', 'identification_id']

class PurchaseOrderBuyerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderBuyerInformation
        fields = ['purchase_order_id', 'buyer_id', 'identification_id', 'identification_name', 'identification_value']

class PurchaseOrderSellerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderSellerInformation
        fields = ['purchase_order_id', 'seller_id', 'identification_id', 'identification_name', 'identification_value']

class DraftPurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPurchaseOrder
        fields = ['purchase_order_id', 'event_id', 'purchase_order_creation_datetime', 'buyer_id', 'buyer_purchase_order_id', 'buyer_entity_name', 'buyer_billing_address_id', 'buyer_shipping_address_id', 'buyer_approver_user_id', 'buyer_approver_name', 'buyer_contact_user_id', 'buyer_contact_name', 'buyer_contact_phone', 'buyer_contact_email', 'is_freight_purchase_order', 'seller_id', 'seller_entity_name', 'seller_address_id', 'seller_contact_user_id', 'seller_contact_name', 'seller_contact_phone', 'seller_contact_email', 'seller_acknowledgement_user_id', 'seller_acknowledgement_datetime', 'delivery_schedule_type', 'payment_terms_code', 'purchase_order_discount_percentage', 'buyer_comments', 'status', 'reissue_draft_purchase_order_id', 'reissue_purchase_order_id', 'closing_user_id_buyer', 'closing_comment_buyer', 'closing_datetime_buyer', 'closing_user_id_seller', 'closing_comment_seller', 'closing_datetime_seller', 'purchase_order_close_datetime']

class DraftPurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPurchaseOrderItem
        # fields = ['purchase_order_line_item_id', 'purchase_order_id', 'item_id', 'buyer_item_id', 'buyer_item_name', 'buyer_item_description', 'due_date', 'currency_code', 'measurement_unit_id', 'rate', 'quantity', 'max_acceptable_quantity', 'measurement_unit_alternate_id', 'rate_alternate', 'quantity_alternate', 'taxes_and_charges_percentage', 'taxes_and_charges_value', 'total_order_value']
        fields = '__all__'

class DraftPurchaseOrderItemChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPurchaseOrderItemCharge
        fields = ['purchase_order_line_item_id', 'charge_name', 'charge_type', 'charge_percentage']
        
class DraftPurchaseOrderItemAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPurchaseOrderItemAttribute
        fields = ['purchase_order_line_item_id', 'attribute_id', 'attribute_value']

class DraftPurchaseOrderBuyerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPurchaseOrderBuyerInformation
        fields = ['purchase_order_id', 'buyer_id', 'identification_id', 'identification_name', 'identification_value']

class DraftPurchaseOrderSellerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPurchaseOrderSellerInformation
        fields = ['purchase_order_id', 'seller_id', 'identification_id', 'identification_name', 'identification_value']

class PurchaseOrderKeyMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderKeyMapping
        fields = ["purchase_order_id", "draft_purchase_order_id"]
