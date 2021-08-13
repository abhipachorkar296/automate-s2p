from django.urls.base import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.utils import timezone
from enterprise.models import * 
from enterprise.serializers import *

class hello(APIView):
    '''
    For Welcoming :)
    '''
    def get(self, request):
        data = {
            "query": "Hello World"
        }
        return Response(data=data, status=status.HTTP_200_OK)

class enterprise(APIView):
    '''
    Get an Enterprise Detail
    '''

    def get(self, request, enterprise_id):
        # Checking if an enterprise exists with the enterprise_id
        try:
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
        except Enterprise.DoesNotExist:
            # Sending Response of Not Found if no enterprise found
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Serializing the enterprise object
        serializer = EnterpriseSerializer(enterprise)
        # Sending the enterprise serialized object
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, enterprise_id):
        try:
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
        except Enterprise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Serializing the incoming data with the present existing data
        serializer = EnterpriseSerializer(enterprise, request.data, partial=True)
        if(serializer.is_valid()):
            # If the serialized data is valid, save it
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        # If not valid, return bad request
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, enterprise_id):
        try:
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
        except Enterprise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if(not enterprise.deleted_datetime):
            enterprise.deleted_datetime = timezone.now()
            enterprise.save()
            serializer = EnterpriseSerializer(enterprise)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class enterprise_list(APIView):

    def get(self, request):
        enterprises = Enterprise.objects.all()
        serializers = EnterpriseSerializer(enterprises, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = EnterpriseSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class enterprise_user(APIView):

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)        
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)       
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if(not user.deleted_datetime):
            user.deleted_datetime = timezone.now()
            user.save()
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class enterprise_user_list(APIView):

    def get(self, request, enterprise_id):
        try:
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
        except Enterprise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        enterprise_users = enterprise.user_set.all()
        serializers = UserSerializer(enterprise_users, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, enterprise_id):
        try:
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
        except Enterprise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        for key, value in request.data.items():
            data[key] = value
        data["enterprise_id"] = enterprise.enterprise_id

        serializer = UserSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data={"user_id": serializer.data.get("user_id")}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class enterprise_entity(APIView):

    def get(self, request, entity_id):
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = EntitySerializer(entity)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, entity_id):
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EntitySerializer(entity, request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, entity_id):
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if(not entity.deleted_datetime):
            entity.deleted_datetime = timezone.now()
            entity.save()
            serializer = EntitySerializer(entity)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class enterprise_entity_list(APIView):

    def get(self, request, enterprise_id):
        try:
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
        except Enterprise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        enterprise_entities = enterprise.entity_set.all()
        serializers = EntitySerializer(enterprise_entities, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, enterprise_id):
        try:
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
        except Enterprise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        for key, value in request.data.items():
            data[key] = value
        data["enterprise_id"] = enterprise.enterprise_id

        serializer = EntitySerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class user_entity_list(APIView):

    def get(self, request, user_id, entity_id=None):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user_entities = user.userentity_set.all()
        serializers = UserEntitySerializer(user_entities, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, user_id, entity_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = {}
        data["entity_id"] = entity.entity_id
        data["user_id"] = user.user_id
        serializer = UserEntitySerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id, entity_id):
        try:
            user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id)
        except UserEntity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if(not user_entity.deleted_datetime):
            user_entity.deleted_datetime = timezone.now()
            user_entity.save()
            serializer = UserEntitySerializer(user_entity)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class seller_list(APIView):
    
    def get(self, request, entity_id=None):
        sellers = Seller.objects.all()
        serializers = SellerSerializer(sellers, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, entity_id):
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = {}
        data["seller_id"] = entity_id
        serializer = SellerSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, reuqest, entity_id):
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            seller = Seller.objects.get(seller_id=entity_id)
        except Seller.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if(not seller.deleted_datetime):
            seller.deleted_datetime = timezone.now()
            seller.save()
            serializer = SellerSerializer(seller)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class buyer_list(APIView):
    
    def get(self, request, entity_id=None):
        buyers = Buyer.objects.all()
        serializers = BuyerSerializer(buyers, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, entity_id):
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = {}
        data["buyer_id"] = entity_id
        serializer = BuyerSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, reuqest, entity_id):
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            buyer = Buyer.objects.get(buyer_id=entity_id)
        except Buyer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if(not buyer.deleted_datetime):
            buyer.deleted_datetime = timezone.now()
            buyer.save()
            serializer = BuyerSerializer(buyer)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class current_seller_list(APIView):
    def get(self, request, enterprise_id):
        try:
            buyer_seller_relationships = BuyerSellerRelationship.objects.filter(buyer_enterprise_id=enterprise_id)
        except BuyerSellerRelationship.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = []
        for buyer_seller_relationship in buyer_seller_relationships:
            entity = buyer_seller_relationship.seller_entity_id
            data.append(entity)
        
        serializer = EntitySerializer(data, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class buyer_seller_relationship_list(APIView):

    def get(self, request, buyer_id, seller_id=None):
        try:
            buyer = Buyer.objects.get(buyer_id=buyer_id)
        except Buyer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        buyer_seller_relationships = buyer.buyersellerrelationship_set.all()
        serializers = BuyerSellerRelationshipSerializer(buyer_seller_relationships, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, buyer_id, seller_id):
        try:
            buyer = Buyer.objects.get(buyer_id=buyer_id)
        except Buyer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            seller = Seller.objects.get(seller_id=seller_id)
        except Seller.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            entity = Entity.objects.get(entity_id=buyer_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        data["buyer_entity_id"] = buyer.buyer_id
        data["buyer_enterprise_id"] = entity.enterprise_id.enterprise_id
        data["seller_entity_id"] = seller.seller_id
        try:
            data["relationship_type"] = request.data["relationship_type"]
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = BuyerSellerRelationshipSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, buyer_id, seller_id):
        try:
            relationship = BuyerSellerRelationship.objects.get(buyer_entity_id=buyer_id, seller_entity_id=seller_id)
        except BuyerSellerRelationship.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if(not relationship.deleted_datetime):
            relationship.deleted_datetime = timezone.now()
            relationship.save()
            serializer = BuyerSellerRelationshipSerializer(relationship)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class module_list(APIView):

    def get(self, request):
        modules = Module.objects.all()
        serializers = ModuleSerializer(modules, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class module(APIView):

    def get(self, reuqest, module_id):
        try:
            module = Module.objects.get(module_id=module_id)
        except Module.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ModuleSerializer(module)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, module_id):
        try:
            module = Module.objects.get(module_id=module_id)
        except Module.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ModuleSerializer(module, request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, module_id):
        try:
            module = Module.objects.get(module_id=module_id)
        except Module.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        module.delete()
        return Response(status=status.HTTP_200_OK)

class user_module_list(APIView):

    def get(self, request, user_id, module_id=None):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user_modules = user.usermodule_set.all()
        serializers = UserModuleSerializer(user_modules, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, user_id, module_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            module = Module.objects.get(module_id=module_id)
        except Module.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = {}
        data["module_id"] = module.module_id
        data["user_id"] = user.user_id
        serializer = UserModuleSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id, module_id):
        try:
            user_module = UserModule.objects.get(user_id=user_id, module_id=module_id)
        except UserModule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if(not user_module.deleted_datetime):
            user_module.deleted_datetime = timezone.now()
            user_module.save()
            serializer = UserModuleSerializer(user_module)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class attribute_list(APIView):

    def get(self, request):
        attributes = Attribute.objects.all()
        serializers = AttributeSerializer(attributes, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AttributeSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class attribute(APIView):

    def get(self, request, attribute_id):
        try:
            attribute = Attribute.objects.get(attribute_id=attribute_id)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AttributeSerializer(attribute)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, attribute_id):
        try:
            attribute = Attribute.objects.get(attribute_id=attribute_id)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AttributeSerializer(attribute, request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, attribute_id):
        try:
            attribute = Attribute.objects.get(attribute_id=attribute_id)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        attribute.delete()
        return Response(status=status.HTTP_200_OK)

class attribute_value_option_list(APIView):

    def get(self, request, attribute_id):
        try:
            attribute = Attribute.objects.get(attribute_id=attribute_id)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        attribute_value_options = attribute.attributevalueoption_set.all()
        serializers = AttributeValueOptionSerializer(attribute_value_options, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, attribute_id):
        try:
            attribute = Attribute.objects.get(attribute_id=attribute_id)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = {}
        try:
            data["value"] = request.data["value"]
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data["attribute_id"] = attribute.attribute_id
        serializer = AttributeValueOptionSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class item(APIView):

    def get(self, request, item_id):
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, item_id):
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item, request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, item_id):
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_200_OK)

    
class item_list(APIView):

    def get(self, request):
        items = Item.objects.all()
        serializers = ItemSerializer(items, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class item_attribute_list(APIView):

    def get(self, request, item_id, attribute_id=None):
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        item_attributes = item.itemattribute_set.all()
        serializers = ItemAttributeSerializer(item_attributes, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, request, item_id, attribute_id):
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            attribute = Attribute.objects.get(attribute_id=attribute_id)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = {}
        data["item_id"] = item.item_id
        data["attribute_id"] = attribute.attribute_id
        serializer = ItemAttributeSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, item_id, attribute_id):
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            attribute = Attribute.objects.get(attribute_id=attribute_id)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            item_attribute = ItemAttribute.objects.get(item_id=item_id, attribute_id=attribute_id)
        except ItemAttribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item_attribute.delete()
        return Response(status=status.HTTP_200_OK)

class buyer_item(APIView):

    def get(self, request, entry_id):
        try:
            buyer_item = BuyerItem.objects.get(entry_id=entry_id)
        except BuyerItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BuyerItemSerializer(buyer_item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, entry_id):
        try:
            buyer_item = BuyerItem.objects.get(entry_id=entry_id)
        except BuyerItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BuyerItemSerializer(buyer_item, request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, entry_id):
        try:
            buyer_item = BuyerItem.objects.get(entry_id=entry_id)
        except BuyerItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if(not buyer_item.deleted_datetime):
            buyer_item.deleted_datetime = timezone.now()
            buyer_item.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class buyer_item_list(APIView):

    def get(self, request, enterprise_id):
        try:
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
        except Enterprise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        buyer_items = enterprise.buyeritem_set.all()
        serializers = BuyerItemSerializer(buyer_items, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, enterprise_id):
        try:
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
        except Enterprise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            item_id = request.data["item_id"]
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        data = {}
        for key in request.data.keys():
            data[key] = request.data[key]
        data["enterprise_id"] = enterprise_id
        serializer = BuyerItemSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class buyer_item_attribute_value_list(APIView):

    def get(self, request, entry_id):
        try:
            buyer_item = BuyerItem.objects.get(entry_id=entry_id)
        except BuyerItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        buyer_item_attribute_value_list = buyer_item.buyeritemattributevalue_set.all()
        serializers = BuyerItemAttributeValueSerializer(buyer_item_attribute_value_list, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, entry_id):
        try:
            buyer_item = BuyerItem.objects.get(entry_id=entry_id)
        except BuyerItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            attribute_id = request.data["attribute_id"]
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            attribute = Attribute.objects.get(attribute_id=attribute_id)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = {}
        for key in request.data.keys():
            data[key] = request.data[key]

        data["buyer_item_entry_id"] = entry_id
        serializer = BuyerItemAttributeValueSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class currency_code(APIView):

    def get(self, request):
        currency_codes = CurrencyCode.objects.all()
        serializers = CurrencyCodeSerializer(currency_codes, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CurrencyCodeSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request , currency_code_name):
        try:
            currency_code = CurrencyCode.objects.get(currency_code=currency_code_name)
        except CurrencyCode.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        currency_code.delete()
        return Response(status=status.HTTP_200_OK)
        
class measurement_unit(APIView):

    def get(self, request, measurement_unit_id):
        try:
            unit = MeasurementUnit.objects.get(measurement_unit_id=measurement_unit_id)
        except MeasurementUnit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = MeasurementUnitSerializer(unit)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, reuqest, measurement_unit_id):
        try:
            unit = MeasurementUnit.objects.get(measurement_unit_id=measurement_unit_id)
        except MeasurementUnit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        unit.delete()
        return Response(status=status.HTTP_200_OK)

class measurement_unit_list(APIView):

    def get(self, request):
        units = MeasurementUnit.objects.all()
        serializers = MeasurementUnitSerializer(units, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, reuqest):
        serializer = MeasurementUnitSerializer(data=reuqest.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data = serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class item_measurement_unit(APIView):

    def get(self, request, item_id):
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        items = ItemMeasurementUnit.objects.filter(item_id=item_id)
        units = []  
        for item in items:
            unit = item.measurement_unit_id
            units.append(unit)
        # items = list(ItemMeasurementUnit.objects.filter(item_id=item_id).values_list('measurement_unit_id', flat=True))
        # units = MeasurementUnit.objects.filter(measurement_unit_id__in=items)
        serializers = MeasurementUnitSerializer(units, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
        
    def post(self, request, item_id):
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        if(not isinstance(data, list)):
            data = [data]
        for item_measure in data:
            item_measure["item_id"] = item_id

        serializer = ItemMeasurementUnitSerializer(data=data, many=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id, measurement_unit_id):
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            item = ItemMeasurementUnit.objects.get(item_id=item_id, measurement_unit_id=measurement_unit_id)
        except ItemMeasurementUnit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_200_OK)
    
class item_measurement_unit_list(APIView):
    def get(self,request):
        items = ItemMeasurementUnit.objects.all()
        serializers = ItemMeasurementUnitSerializer(items, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ItemMeasurementUnitSerializer(data=request.data, many=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data = serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class search_keyword_buyer_items_result(APIView):
    def search_keyword(self, keyword, name, id):
        # Apply Algorithm on name
        if(keyword in name):
            return True
        # Apply Algorithm on id
        if(keyword in id or id in keyword):
            return True
        # Couldn't match
        return False

    def get(self, request, user_id, keyword):
        # Trying to get user's enterprise_id
        try:
            user = User.objects.get(user_id=user_id)
            enterprise_id = UserSerializer(user).data.get("enterprise_id")
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        buyer_item_list = BuyerItem.objects.filter(enterprise_id=enterprise_id).filter(deleted_datetime=None)
        buyer_item_list_data = BuyerItemSerializer(buyer_item_list, many=True)
        data_to_return = []
        for buyer_item in buyer_item_list_data.data:
            name = buyer_item["buyer_item_name"]
            id = buyer_item["buyer_item_id"]
            if(self.search_keyword(keyword=keyword.lower(), name=str(name).lower(), id=str(id).lower())):
                data_to_return.append(buyer_item)
        return Response(data=data_to_return, status=status.HTTP_200_OK)