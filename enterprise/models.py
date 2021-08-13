from django.db import models

# Create your models here.
class Enterprise(models.Model):
    enterprise_id = models.AutoField(primary_key=True, editable=False)
    enterprise_name = models.CharField(max_length=500, unique=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return "{}, {}".format(self.enterprise_id, self.enterprise_name)

class User(models.Model):
    user_id = models.AutoField(primary_key=True, editable=False)
    user_email = models.EmailField(max_length=100)
    user_firstname = models.CharField(max_length=100)
    user_lastname = models.CharField(max_length=100)
    user_phonenumber = models.CharField(max_length=100)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)
    enterprise_id = models.ForeignKey(Enterprise, on_delete=models.CASCADE)

    def __str__(self):
        return "{} is the user at {}".format(self.user_id, self.enterprise.enterprise_name)

class Entity(models.Model):
    entity_id = models.AutoField(primary_key=True, editable=False)
    enterprise_id = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=100)
    entity_name = models.CharField(max_length=500)
    entity_primary_address = models.TextField()
    entity_primary_email = models.EmailField(max_length=100)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

class UserEntity(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_id = models.ForeignKey(Entity, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

    class Meta:
        unique_together = ("user_id", "entity_id",)

class Buyer(models.Model):
    buyer_id = models.OneToOneField(Entity, on_delete=models.CASCADE, primary_key=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

class Seller(models.Model):
    seller_id = models.OneToOneField(Entity, on_delete=models.CASCADE, primary_key=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

class BuyerSellerRelationship(models.Model):
    relationship_id = models.AutoField(primary_key=True, editable=False)
    buyer_enterprise_id = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    buyer_entity_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller_entity_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=100)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

    class Meta:
        unique_together = ("buyer_enterprise_id", "buyer_entity_id", "seller_entity_id",)

# Needs to be deleted
class Module(models.Model):
    module_id = models.AutoField(primary_key=True, editable=False)
    module_name = models.CharField(max_length=100, unique=True)

# Needs to be deleted
class UserModule(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

    class Meta:
        unique_together = ("user_id", "module_id",)

class Attribute(models.Model):
    attribute_id = models.AutoField(primary_key=True, editable=False)
    attribute_name = models.CharField(max_length=100, unique=True)
    attribute_value_type = models.CharField(max_length=100) # needs discussion

class AttributeValueOption(models.Model):
    attribute_id = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ("attribute_id", "value",)

class Item(models.Model):
    item_id = models.AutoField(primary_key=True, editable=False)
    item_name = models.CharField(max_length=500, unique=True)
    item_description = models.TextField(blank=True)

class ItemAttribute(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    attribute_id = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("item_id", "attribute_id",)

class BuyerItem(models.Model):
    entry_id = models.AutoField(primary_key=True,editable=False)
    enterprise_id = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    buyer_item_id = models.CharField(max_length=100)
    buyer_item_name = models.CharField(max_length=100)
    buyer_item_description = models.TextField(blank=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

    class Meta:
        unique_together = ("enterprise_id", "buyer_item_id",)

class BuyerItemAttributeValue(models.Model):
    buyer_item_entry_id = models.ForeignKey(BuyerItem, on_delete=models.CASCADE)
    attribute_id = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=100)

class CurrencyCode(models.Model):
    currency_code = models.CharField(max_length=3, unique=True, primary_key=True)
    
class MeasurementUnit(models.Model):
    measurement_unit_id = models.AutoField(primary_key=True, editable=False)
    measurement_unit_primary_name = models.CharField(max_length=100, unique=True)
    measurement_unit_category = models.CharField(max_length=100)
    measurement_unit_value_type = models.CharField(max_length=100) # change required to ENUM (Deciaml or Int)

class ItemMeasurementUnit(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    measurement_unit_id = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)

class Address(models.Model):
    address_id = models.AutoField(primary_key=True, editable=False)
    address_nickname = models.CharField(max_length=500, blank=True)
    country = models.CharField(max_length=100)
    full_address = models.TextField(blank=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    address3 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state_or_territory = models.CharField(max_length=100, null=True)
    postal_code = models.IntegerField()
    latitude = models.DecimalField(max_digits= 15,decimal_places= 15, null=True, blank=True)
    longitude = models.DecimalField(max_digits = 15,decimal_places= 15, null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True)

class EntityAddress(models.Model):
    entity_id = models.ForeignKey(Entity, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_billing_address = models.BooleanField(default=False)
    is_shipping_address = models.BooleanField(default=False)
    order_id = models.IntegerField(blank=True, null=True)
    
    class Meta:
        unique_together = ("entity_id", "address_id")
        ordering = ['entity_id', 'order_id', 'address_id']


class Country(models.Model):
    country = models.CharField(max_length=50)