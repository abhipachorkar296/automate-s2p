from rest_framework import serializers
from goods_receipt.models import *

class GoodsReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsReceipt
        fields = ["goods_receipt_entry_id", "document_url", "invoice_line_item_id", "buyer_goods_receipt_id", "receipt_datetime", "receiving_user_id", "receiving_user_name", "receiving_user_phone", "receiving_user_email", "measurement_unit_id", "delivered_quantity", "receipt_quantity_rejected", "receipt_quantity_accepted", "problem_category", "problem_picture_id", "comments"]