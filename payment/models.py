from django.db import models
from enterprise.models import *
from purchase_order.models import *
from goods_receipt.models import *
from quality_check.models import *
from event.models import *
from invoice.models import *


# Create your models here.
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True, editable=False)
    document_url = models.URLField(max_length= 200, null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    created_by_user_id = models.ForeignKey(User, related_name='created_by_user_id', on_delete=models.CASCADE)
    payment_category = models.CharField(max_length=100) # "Invoice payment / PO Prepayment / refund"
    from_entity_id = models.ForeignKey(Entity, related_name='from_entity_id', on_delete=models.CASCADE)
    to_entity_id = models.ForeignKey(Entity, related_name='to_entity_id', on_delete=models.CASCADE)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.CASCADE)
    base_payment_amount = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    payment_mode = models.CharField(max_length=100)
    payment_reference = models.CharField(max_length=100)
    applied_balance_amount = models.DecimalField(max_digits=25, decimal_places=10, default=0)
    total_amount = models.DecimalField(max_digits=25, decimal_places=10)
    comments = models.TextField(max_length=500, blank=True)

class InvoiceItemPayment(models.Model):
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    invoice_line_item_id = models.ForeignKey(InvoiceItem, on_delete=models.CASCADE)
    amount_applied = models.DecimalField(max_digits=25, decimal_places=10)

class PaymentBalance(models.Model):
    balance_id = models.AutoField(primary_key=True, editable=False)
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE) 
    entry_type = models.CharField(max_length=100) # "Prepayment / rejection / overpayment(possibly in future)"
    source_purchase_order_id = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True)
    rejection_goods_receipt_entry_id = models.ForeignKey(GoodsReceipt, on_delete=models.SET_NULL, null=True)
    rejection_quality_check_id = models.ForeignKey(QualityCheck, on_delete=models.SET_NULL, null=True)
    prepayment_payment_id = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    comments = models.CharField(max_length=100, blank=True)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=25, decimal_places=10)
    used_amount = models.DecimalField(max_digits=25, decimal_places=10, default=0)
    available_amount = models.DecimalField(max_digits=25, decimal_places=10)
    cashout_requested = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modefied_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

class PaymentBalanceUsage(models.Model):
    usage_id = models.AutoField(primary_key=True, editable=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    balance_id = models.ForeignKey(PaymentBalance, on_delete=models.CASCADE)
    usage_type = models.CharField(max_length=100)
    used_amount = models.DecimalField(max_digits=25, decimal_places=10)
    adjusted_payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    comments = models.CharField(max_length=100, blank=True)