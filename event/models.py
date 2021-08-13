from django.utils.translation import gettext_lazy as _
from django.db import models
from enterprise.models import *
# Create your models here.

class DraftEvent(models.Model):
    event_id = models.AutoField(primary_key=True, editable=False)
    enterprise_id = models.ForeignKey(Enterprise, on_delete=models.CASCADE, null=True, blank=True) # Cannot be blank, needs discussion
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    event_name = models.CharField(max_length = 500)
    event_type = models.CharField(max_length = 500, default = "RFQ")
    event_start_datetime = models.DateTimeField(null=True, blank=True)
    event_end_datetime = models.DateTimeField(null=True, blank=True)
    buyer_billing_address_id = models.ForeignKey(Address, related_name="billing_draft", on_delete=models.SET_NULL, null=True, blank=True)
    buyer_shipping_address_id = models.ForeignKey(Address, related_name="shipping_draft", on_delete=models.SET_NULL, null=True, blank=True)
    event_delivery_datetime = models.DateTimeField(null=True, blank=True)
    payment_terms_code = models.CharField(max_length=500, null=True, blank=True)
    created_by_user_id = models.ForeignKey(User, related_name="created_draft", on_delete=models.CASCADE)
    created_by_name = models.CharField(max_length=100, null=True, blank=True)
    created_by_phone = models.CharField(max_length=100, null=True, blank=True)
    created_by_email = models.EmailField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    last_modified_by_user_id = models.ForeignKey(User, related_name="modified_draft", on_delete=models.CASCADE)

class DraftEventItem(models.Model):
    event_line_item_id = models.AutoField(primary_key=True, editable=False)
    event_id = models.ForeignKey(DraftEvent, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer_item_id = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    measurement_unit_id = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, blank=True, null=True)
    # Spelling needs to be corrected
    meausrement_unit = models.CharField(max_length=100, blank=True)
    desired_quantity = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.SET_NULL, null=True)
    desired_price = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    opening_bid = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    total_amount = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    allow_substitutes = models.BooleanField(default=False)
    insurance_required = models.BooleanField(default=False)
    post_to_global_market_place = models.BooleanField(default=False)

class DraftEventItemAttribute(models.Model):
    event_line_item_id = models.ForeignKey(DraftEventItem, on_delete=models.CASCADE)
    attribute_id = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=100)

class DraftEventItemSeller(models.Model):
    event_line_item_id = models.ForeignKey(DraftEventItem, on_delete=models.CASCADE)
    event_id = models.ForeignKey(DraftEvent, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    buyer_approval_required = models.BooleanField(default=False)
    approved_by_buyer = models.BooleanField(null=True)
    invitation_status = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ("event_line_item_id", "seller_id",)

class Event(models.Model):
    event_id = models.AutoField(primary_key=True, editable=False)
    parent_event_id = models.IntegerField(default=0)
    enterprise_id = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    event_name = models.CharField(max_length = 500)
    event_type = models.CharField(max_length = 500, default = "RFQ")
    event_start_datetime = models.DateTimeField()
    event_end_datetime = models.DateTimeField()
    buyer_billing_address_id = models.ForeignKey(Address, related_name="billing_event", on_delete=models.CASCADE)
    buyer_shipping_address_id = models.ForeignKey(Address, related_name="shipping_event", on_delete=models.CASCADE)
    event_delivery_datetime = models.DateTimeField()
    payment_terms_code = models.CharField(max_length=500, null=True, blank=True)
    created_by_user_id = models.ForeignKey(User, related_name="created_event", on_delete=models.SET_NULL, null=True)
    created_by_name = models.CharField(max_length=100)
    created_by_phone = models.CharField(max_length=100, null=True, blank=True)
    created_by_email = models.EmailField(max_length=100)
    status = models.CharField(max_length=100, default="Ongoing")
    last_modified_by_user_id = models.ForeignKey(User, related_name="modified_event", on_delete=models.SET_NULL, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

class EventItem(models.Model):
    event_line_item_id = models.AutoField(primary_key=True, editable=False)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer_item_id = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    measurement_unit_id = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    meausrement_unit = models.CharField(max_length=100, blank=True)
    desired_quantity = models.DecimalField(max_digits=25, decimal_places=10)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.CASCADE)
    desired_price = models.DecimalField(max_digits=25, decimal_places=10)
    opening_bid = models.DecimalField(max_digits=25, decimal_places=10)
    total_amount = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    allow_substitutes = models.BooleanField(default=False)
    insurance_required = models.BooleanField(default=False)
    post_to_global_market_place = models.BooleanField(default=False)

class EventItemAttribute(models.Model):
    event_line_item_id = models.ForeignKey(EventItem, on_delete=models.CASCADE)
    attribute_id = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=100, default="")

class EventItemSeller(models.Model):
    event_line_item_id = models.ForeignKey(EventItem, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    buyer_approval_required = models.BooleanField(default=False)
    approved_by_buyer = models.BooleanField(null=True)
    invitation_status = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ("event_line_item_id", "seller_id",)

class KeyMapping(models.Model):
    event_id = models.OneToOneField(Event, on_delete=models.CASCADE, unique=True)
    draft_event_id = models.OneToOneField(DraftEvent, on_delete=models.CASCADE, unique=True)

class ChooseBuyerSeller(models.TextChoices):
    # Refer here for enum https://docs.djangoproject.com/en/3.2/ref/models/fields/#field-choices-enum-types
    BUYER = 'B', _('Buyer')
    SELLER = 'S', _('Seller')

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True, editable=False)
    parent_bid_id = models.IntegerField(default=0)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    bid_creator_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_creator_entity_type = models.CharField(max_length=100, choices=ChooseBuyerSeller.choices)
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    seller_bid_id = models.CharField(max_length=100)
    bid_creation_datetime = models.DateTimeField()
    bid_valid_till_datetime = models.DateTimeField()
    payment_terms_code = models.CharField(max_length=100)
    seller_comments = models.TextField(max_length=500, blank=True)
    rebid_request_comments = models.TextField(max_length=500, blank=True)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=25, decimal_places=10)
    taxes = models.DecimalField(max_digits=25, decimal_places=10)
    total_shipping_cost = models.DecimalField(max_digits=25, decimal_places=10)
    total_other_charges = models.DecimalField(max_digits=25, decimal_places=10)
    bulk_discount_percentage = models.DecimalField(max_digits=25, decimal_places=10)
    bulk_discount_amount = models.DecimalField(max_digits=25, decimal_places=10)
    total = models.DecimalField(max_digits=25, decimal_places=10)
    status = models.CharField(max_length=100, default="Response Submitted")  
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

class BidItem(models.Model):
    bid_line_item_id = models.AutoField(primary_key=True, editable=False)
    bid_id = models.ForeignKey(Bid, on_delete=models.CASCADE)
    event_line_item_id = models.ForeignKey(EventItem, on_delete=models.CASCADE)
    measurement_unit_id = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    quantity_offered = models.DecimalField(max_digits=25, decimal_places=10)
    quantity_awarded = models.DecimalField(max_digits=25, decimal_places=10)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=25, decimal_places=10)
    other_charges = models.DecimalField(max_digits=25, decimal_places=10)
    shipping_managed_by = models.CharField(max_length=100, choices=ChooseBuyerSeller.choices)
    shipping_cost = models.DecimalField(max_digits=25, decimal_places=10)
    total_amount = models.DecimalField(max_digits=25, decimal_places=10)
    seller_comments = models.TextField(max_length=500, blank=True)

class BidItemTax(models.Model):
    bid_line_item_id = models.ForeignKey(BidItem, on_delete=models.CASCADE)
    tax_name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=25, decimal_places=10)

    class Meta:
        unique_together = ('bid_line_item_id', 'tax_name')

class DraftBid(models.Model):
    bid_id = models.AutoField(primary_key=True, editable=False)
    parent_bid_id = models.IntegerField(default=0)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    bid_creator_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_creator_entity_type = models.CharField(max_length=100, choices=ChooseBuyerSeller.choices)
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    seller_bid_id = models.CharField(max_length=100, blank=True)
    bid_creation_datetime = models.DateTimeField(null=True)
    bid_valid_till_datetime = models.DateTimeField(null=True)
    payment_terms_code = models.CharField(max_length=100, null=True)
    seller_comments = models.TextField(max_length=500, blank=True)
    rebid_request_comments = models.TextField(max_length=500, blank=True)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    taxes = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    total_shipping_cost = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    total_other_charges = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    bulk_discount_percentage = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    bulk_discount_amount = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    total = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    status = models.CharField(max_length=100, default="Response Due")  
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

class DraftBidItem(models.Model):
    bid_line_item_id = models.AutoField(primary_key=True, editable=False)
    bid_id = models.ForeignKey(DraftBid, on_delete=models.CASCADE)
    event_line_item_id = models.ForeignKey(EventItem, on_delete=models.CASCADE)
    measurement_unit_id = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, null=True)
    quantity_offered = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    quantity_awarded = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    other_charges = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    shipping_managed_by = models.CharField(max_length=100, choices=ChooseBuyerSeller.choices, blank=True)
    shipping_cost = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    total_amount = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    seller_comments = models.TextField(max_length=500, blank=True)

class DraftBidItemTax(models.Model):
    bid_line_item_id = models.ForeignKey(DraftBidItem, on_delete=models.CASCADE)
    tax_name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=25, decimal_places=10, null=True)

    class Meta:
        unique_together = ('bid_line_item_id', 'tax_name')

class Award(models.Model):
    award_id = models.AutoField(primary_key=True, editable=False)
    parent_award_id = models.IntegerField(default=0)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    creator_user_id = models.ForeignKey(User, related_name="award_creator", on_delete=models.CASCADE)
    approver_user_id = models.ForeignKey(User, related_name="award_approver", on_delete=models.CASCADE)
    draft_purchase_order_id = models.IntegerField(default=0) # Needs to be changed
    purchase_order_id = models.IntegerField(default=0) # Needs to be changed
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    seller_bid_id = models.CharField(max_length=100)
    award_creation_datetime = models.DateTimeField()
    payment_terms_code = models.CharField(max_length=500)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=25, decimal_places=10)
    taxes = models.DecimalField(max_digits=25, decimal_places=10)
    total_shipping_cost = models.DecimalField(max_digits=25, decimal_places=10)
    total_other_charges = models.DecimalField(max_digits=25, decimal_places=10)
    bulk_discount_percentage = models.DecimalField(max_digits=25, decimal_places=10)
    bulk_discount_amount = models.DecimalField(max_digits=25, decimal_places=10)
    total = models.DecimalField(max_digits=25, decimal_places=10)
    deal_status = models.CharField(max_length=100, default="Deal Awarded")
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

class AwardItem(models.Model):
    award_line_item_id = models.AutoField(primary_key=True, editable=False)
    award_id = models.ForeignKey(Award, on_delete=models.CASCADE)
    event_line_item_id = models.ForeignKey(EventItem, on_delete=models.CASCADE)
    measurement_unit_id = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    quantity_offered = models.DecimalField(max_digits=25, decimal_places=10)
    quantity_awarded = models.DecimalField(max_digits=25, decimal_places=10)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=25, decimal_places=10)
    other_charges = models.DecimalField(max_digits=25, decimal_places=10)
    shipping_managed_by = models.CharField(max_length=100, choices=ChooseBuyerSeller.choices)
    shipping_cost = models.DecimalField(max_digits=25, decimal_places=10)
    total_amount = models.DecimalField(max_digits=25, decimal_places=10)

class AwardItemTax(models.Model):
    award_line_item_id = models.ForeignKey(AwardItem, on_delete=models.CASCADE)
    tax_name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=25, decimal_places=10)

    class Meta:
        unique_together = ('award_line_item_id', 'tax_name')

class DraftAward(models.Model):
    award_id = models.AutoField(primary_key=True, editable=False)
    parent_award_id = models.IntegerField(default=0)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    creator_user_id = models.ForeignKey(User, related_name="draft_award_creator", on_delete=models.CASCADE)
    approver_user_id = models.ForeignKey(User, related_name="draft_award_approver", on_delete=models.CASCADE, null=True)
    draft_purchase_order_id = models.IntegerField(default=0) # Needs to be changed
    purchase_order_id = models.IntegerField(default=0) # Needs to be changed
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    seller_bid_id = models.CharField(max_length=100, blank=True)
    award_creation_datetime = models.DateTimeField(auto_now_add=True)
    payment_terms_code = models.CharField(max_length=500, blank=True)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.CASCADE, null=True)
    subtotal = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    taxes = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    total_shipping_cost = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    total_other_charges = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    bulk_discount_percentage = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    bulk_discount_amount = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    total = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    deal_status = models.CharField(max_length=100, default="Deal Awarded")
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

class DraftAwardItem(models.Model):
    award_line_item_id = models.AutoField(primary_key=True, editable=False)
    award_id = models.ForeignKey(DraftAward, on_delete=models.CASCADE)
    event_line_item_id = models.ForeignKey(EventItem, on_delete=models.CASCADE)
    measurement_unit_id = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, null=True)
    quantity_offered = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    quantity_awarded = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    other_charges = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    shipping_managed_by = models.CharField(max_length=100, choices=ChooseBuyerSeller.choices, blank=True)
    shipping_cost = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    total_amount = models.DecimalField(max_digits=25, decimal_places=10, null=True)

class DraftAwardItemTax(models.Model):
    award_line_item_id = models.ForeignKey(DraftAwardItem, on_delete=models.CASCADE)
    tax_name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=25, decimal_places=10, null=True)

    class Meta:
        unique_together = ('award_line_item_id', 'tax_name')
        