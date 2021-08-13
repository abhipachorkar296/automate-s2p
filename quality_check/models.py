from django.utils.translation import gettext_lazy as _
from django.db import models
from goods_receipt.models import *

# Create your models here.
class ChooseQualityCheckCategory(models.TextChoices):
    # Refer here for enum https://docs.djangoproject.com/en/3.2/ref/models/fields/#field-choices-enum-types
    REGULAR = 'regular', _('regular')
    PRODUCTIONLINE = 'production line', _('production line')

class QualityCheck(models.Model):
    quality_check_id = models.AutoField(primary_key=True, editable=False)
    document_url = models.URLField(max_length=100, null=True, blank=True)
    goods_receipt_entry_id = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE)
    buyer_analytical_report_number = models.CharField(max_length=100, blank=True)
    created_by_user_id = models.ForeignKey(User, related_name="quality_check_created_by_user_id", on_delete=models.CASCADE)
    created_by_name = models.CharField(max_length=100)
    created_by_phone = models.CharField(max_length=100, blank=True)
    created_by_email = models.EmailField(max_length=100)
    quality_check_datetime = models.DateTimeField(auto_now_add=True)
    quality_check_category = models.CharField(max_length=100, choices=ChooseQualityCheckCategory.choices, default=ChooseQualityCheckCategory.REGULAR)
    quality_check_reason = models.CharField(max_length=100, blank=True)
    measurement_unit_id = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    quantity_rejected = models.DecimalField(max_digits=25, decimal_places=10, default=0)
    problem_category = models.CharField(max_length=100, blank=True)
    problem_picture_id = models.IntegerField(null=True)
    problem_comments = models.TextField(max_length=500, blank=True)