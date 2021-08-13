from rest_framework import serializers
from payment.models import *

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["payment_id", "document_url", "created_datetime", "created_by_user_id", "payment_category", "from_entity_id", "to_entity_id", "currency_code", "base_payment_amount", "payment_mode", "payment_reference", "applied_balance_amount", "total_amount", "comments"]

class InvoiceItemPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItemPayment
        fields = ["payment_id", "invoice_line_item_id", "amount_applied"]

class PaymentBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentBalance
        fields = ["balance_id", "buyer_id", "seller_id", "entry_type", "source_purchase_order_id", "rejection_goods_receipt_entry_id", "rejection_quality_check_id", "prepayment_payment_id", "comments", "currency_code", "total_amount", "used_amount", "available_amount", "cashout_requested"]

class PaymentBalanceUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentBalanceUsage
        fields = ["usage_id", "created_datetime", "balance_id", "usage_type", "used_amount", "adjusted_payment_id", "comments"]