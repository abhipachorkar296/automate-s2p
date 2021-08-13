from rest_framework import serializers
from enterprise.models import *

class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ["enterprise_id", "enterprise_name", "created_datetime", "modified_datetime", "deleted_datetime"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "user_email", "user_firstname", "user_lastname", "user_phonenumber", "enterprise_id", "created_datetime", "modified_datetime", "deleted_datetime"]

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ["entity_id", "enterprise_id", "entity_type", "entity_name", "entity_name", "entity_primary_address", "entity_primary_email", "created_datetime", "modified_datetime", "deleted_datetime"]

class UserEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEntity
        fields = ["user_id", "entity_id", "created_datetime", "modified_datetime", "deleted_datetime"]

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ["buyer_id", "created_datetime", "modified_datetime", "deleted_datetime"]

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["seller_id", "created_datetime", "modified_datetime", "deleted_datetime"]

class BuyerSellerRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerSellerRelationship
        fields = ["relationship_id", "buyer_enterprise_id", "buyer_entity_id", "seller_entity_id", "relationship_type", "created_datetime", "modified_datetime", "deleted_datetime"]

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["module_id", "module_name"]

class UserModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModule
        fields = ["user_id", "module_id", "created_datetime", "modified_datetime", "deleted_datetime"]

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["attribute_id", "attribute_name", "attribute_value_type"]

class AttributeValueOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValueOption
        fields = ["attribute_id", "value"]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["item_id", "item_name", "item_description"]

class ItemAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAttribute
        fields = ["item_id", "attribute_id"]

class BuyerItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerItem
        fields = ["entry_id", "enterprise_id", "buyer_item_id", "buyer_item_name", "buyer_item_description", "item_id", "created_datetime", "modified_datetime", "deleted_datetime"]

class BuyerItemAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerItemAttributeValue
        fields = ["buyer_item_entry_id", "attribute_id", "attribute_value"]

class CurrencyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyCode
        fields = ["currency_code"]

class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = ["measurement_unit_id", "measurement_unit_primary_name", "measurement_unit_category", "measurement_unit_value_type"]

class ItemMeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMeasurementUnit
        fields = ["item_id", "measurement_unit_id"]

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["address_id", "address_nickname", "country", "full_address", "address1", "address2", "address3", "city", "state_or_territory", "postal_code", "latitude", "longitude", "created_datetime", "modified_datetime", "deleted_datetime"]

class EntityAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityAddress
        fields = ["entity_id", "address_id", "is_billing_address", "is_shipping_address", "order_id"]

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["country"]