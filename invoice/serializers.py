from rest_framework import serializers
from invoice.models import *

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["invoice_id", "document_url", "invoice_type", "created_by_user_id", "seller_invoice_id", "provisional_invoice_id", "delivery_document_id", "provisional_document_url", "purchase_order_id", "buyer_purchase_order_id", "invoice_creation_datetime", "seller_id", "seller_entity_name", "seller_address_id", "seller_contact_user_id", "seller_contact_name", "seller_contact_phone", "seller_contact_email", "buyer_id", "buyer_entity_name", "buyer_billing_address_id", "buyer_shipping_address_id", "buyer_contact_user_id", "buyer_contact_name", "buyer_contact_phone", "buyer_contact_email", "invoice_discount_percentage", "seller_comments", "status", "closing_user_id_seller", "closing_comment_seller", "closing_datetime_seller", "closing_user_id_buyer", "closing_comment_buyer", "closing_datetime_buyer", "modified_datetime", "invoice_close_datetime"]

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ["invoice_line_item_id", "invoice_id", "purchase_order_line_item_id", "item_id", "buyer_item_id", "buyer_item_name", "buyer_item_description", "seller_comments", "measurement_unit_id", "rate", "quantity_invoiced", "shipping_per_unit", "amount_invoiced", "amount_due", "amount_paid", "currency_code", "payment_terms_reference_date_type", "payment_terms_days", "dispatch_date", "receipt_date", "payment_due_date"]

class InvoiceItemAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItemAttribute
        fields = ["invoice_line_item_id", "attribute_id", "attribute_value"]

class InvoiceItemChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItemCharge
        fields = ["invoice_line_item_id", "charge_name", "charge_type", "charge_percentage"]

class InvoiceBuyerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceBuyerInformation
        fields = ["invoice_id", "buyer_id", "identification_id", "identification_name", "identification_value"]

class InvoiceSellerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceSellerInformation
        fields = ["invoice_id", "seller_id", "identification_id", "identification_name", "identification_value"]

class DraftInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftInvoice
        fields = ["invoice_id", "document_url", "invoice_type", "created_by_user_id", "seller_invoice_id", "provisional_invoice_id", "delivery_document_id", "provisional_document_url", "purchase_order_id", "buyer_purchase_order_id", "invoice_creation_datetime", "seller_id", "seller_entity_name", "seller_address_id", "seller_contact_user_id", "seller_contact_name", "seller_contact_phone", "seller_contact_email", "buyer_id", "buyer_entity_name", "buyer_billing_address_id", "buyer_shipping_address_id", "buyer_contact_user_id", "buyer_contact_name", "buyer_contact_phone", "buyer_contact_email", "invoice_discount_percentage", "seller_comments", "status", "closing_user_id_seller", "closing_comment_seller", "closing_datetime_seller", "closing_user_id_buyer", "closing_comment_buyer", "closing_datetime_buyer", "modified_datetime", "invoice_close_datetime"]

class DraftInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftInvoiceItem
        fields = ["invoice_line_item_id", "invoice_id", "purchase_order_line_item_id", "item_id", "buyer_item_id", "buyer_item_name", "buyer_item_description", "seller_comments", "measurement_unit_id", "rate", "quantity_invoiced", "shipping_per_unit", "amount_invoiced", "amount_due", "amount_paid", "currency_code", "payment_terms_reference_date_type", "payment_terms_days", "dispatch_date", "receipt_date", "payment_due_date"]

class DraftInvoiceItemAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftInvoiceItemAttribute
        fields = ["invoice_line_item_id", "attribute_id", "attribute_value"]

class DraftInvoiceItemChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftInvoiceItemCharge
        fields = ["invoice_line_item_id", "charge_name", "charge_type", "charge_percentage"]

class DraftInvoiceBuyerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftInvoiceBuyerInformation
        fields = ["invoice_id", "buyer_id", "identification_id", "identification_name", "identification_value"]

class DraftInvoiceSellerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftInvoiceSellerInformation
        fields = ["invoice_id", "seller_id", "identification_id", "identification_name", "identification_value"]

class ProformaInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProformaInvoice
        fields = ["invoice_id", "purchase_order_id", "buyer_purchase_order_id", "document_url", "created_by_user_id", "invoice_creation_datetime", "seller_id", "buyer_id", "seller_comments", "status", "currency_code", "amount_invoiced", "amount_paid", "closing_user_id_seller", "closing_comment_seller", "closing_datetime_seller", "closing_user_id_buyer", "closing_comment_buyer", "closing_datetime_buyer", "invoice_close_datetime"]
