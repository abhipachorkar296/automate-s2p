from django.db import models
from enterprise.models import *
from invoice.models import *

# Create your models here.
class GoodsReceipt(models.Model):
    goods_receipt_entry_id = models.AutoField(primary_key=True, editable=False)
    document_url = models.URLField(max_length= 200, null=True, blank=True)
    invoice_line_item_id = models.OneToOneField(InvoiceItem, on_delete=models.CASCADE)
    buyer_goods_receipt_id = models.CharField(max_length=100)
    receipt_datetime = models.DateTimeField(auto_now_add=True)
    receiving_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    receiving_user_name = models.CharField(max_length=100)
    receiving_user_phone = models.CharField(max_length=100, blank=True)
    receiving_user_email = models.EmailField(max_length=100)
    measurement_unit_id = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    delivered_quantity = models.DecimalField(max_digits=25, decimal_places=10)
    receipt_quantity_rejected = models.DecimalField(max_digits=25, decimal_places=10, default=0)
    receipt_quantity_accepted = models.DecimalField(max_digits=25, decimal_places=10)
    problem_category = models.CharField(max_length=100, blank=True)
    problem_picture_id = models.IntegerField(null=True)
    comments = models.CharField(max_length=100, blank=True)
    deleted_datetime = models.DateTimeField(null=True)

