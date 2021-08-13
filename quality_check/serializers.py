from rest_framework import serializers
from quality_check.models import *

class QualityCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityCheck
        fields = ['quality_check_id', 'document_url', 'goods_receipt_entry_id', 'buyer_analytical_report_number', 'created_by_user_id', 'created_by_name', 'created_by_phone', 'created_by_email', 'quality_check_datetime', 'quality_check_category', 'quality_check_reason', 'measurement_unit_id', 'quantity_rejected', 'problem_category', 'problem_picture_id', 'problem_comments']