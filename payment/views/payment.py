from rest_framework.views import APIView
from django.http import HttpRequest
import requests
from rest_framework.response import Response
from rest_framework import status
import json
from django.utils import timezone
from django.urls import reverse
from collections import defaultdict
from enterprise.models import * 
from enterprise.serializers import *
from event.models import *
from event.serializers import *
from purchase_order.models import *
from purchase_order.serializers import *
from invoice.models import *
from invoice.serializers import *
from goods_receipt.models import *
from goods_receipt.serializers import *
from payment.models import *
from payment.serializers import *
from decimal import *
from django.conf import settings

DECIMAL_COMPARISON_PRECISION = settings.DECIMAL_COMPARISON_PRECISION


class payment(APIView):
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(payment_id=payment_id)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data_to_return = PaymentSerializer(payment).data
        return Response(data=data_to_return, status=status.HTTP_200_OK)

class payment_from_invoice(APIView):
    def get(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(invoice_id=invoice_id)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        invoice_line_item_id_list = list(InvoiceItem.objects.filter(invoice_id=invoice_id).values_list("invoice_line_item_id", flat=True))
        payment_id_list = list(set(InvoiceItemPayment.objects.filter(invoice_line_item_id__in = invoice_line_item_id_list).values_list("payment_id", flat=True)))
        
        data_to_return = []
        request = HttpRequest()
        request.method = "GET"
        for payment_id in payment_id_list:
            response_payment = payment.as_view()(request,payment_id)
            if(response_payment.status_code == 200):
                data_to_return.append(response_payment.data)
        return Response(data=data_to_return, status=status.HTTP_200_OK)

class payment_list(APIView):
    
    entity_type = ""
    
    def get(self, request, user_id, entity_id=""):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data_to_return = []
        if(self.entity_type == "Buyer"):
            # Getting all the buyer id list
            buyer_id_list = list(Buyer.objects.filter(deleted_datetime__isnull=True).values_list("buyer_id", flat=True))
            # Getting all the current entity id list which is a buyer entity 
            # and having user with this user_id 
            user_buyer_entity_id_list = list(UserEntity.objects.filter(user_id=user_id, deleted_datetime__isnull=True, entity_id__in=buyer_id_list).values_list("entity_id", flat=True))
            # finding payment id list from payment table using from_entity_id
            for user_buyer_entity_id in user_buyer_entity_id_list:
                payment = Payment.objects.filter(from_entity_id = user_buyer_entity_id)
                serializers = PaymentSerializer(payment, many=True)
                data_to_return.append(serializers.data)
        elif(self.entity_type == "Seller"):
            # Getting all the seller id list
            seller_id_list = list(Seller.objects.filter(deleted_datetime__isnull=True).values_list("seller_id", flat=True))
            # Getting all the current entity id list which is a seller entity
            # and having user with this user_id 
            user_seller_entity_id_list = list(UserEntity.objects.filter(user_id=user_id).filter(deleted_datetime__isnull=True).filter(entity_id__in=seller_id_list).values_list("entity_id", flat=True))
            # finding payment id list from payment table using to_entity_id
            for user_seller_entity_id in user_seller_entity_id_list:
                payment = Payment.objects.filter(to_entity_id = user_seller_entity_id)
                serializers = PaymentSerializer(payment, many=True)
                data_to_return.append(serializers.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=data_to_return, status=status.HTTP_200_OK)

    def post(self, request, user_id, entity_id):
        #can be done by buyer only
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id, deleted_datetime__isnull=True)
        except UserEntity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data_to_return = {}
        payment_data = request.data["payment_info"]
        payment_data["created_by_user_id"] = user_id
        payment_data["from_entity_id"] = entity_id
        serializer = PaymentSerializer(data=payment_data)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["payment_info"] = serializer.data
            payment_id = serializer.data.get("payment_id")
            payment = Payment.objects.get(payment_id=payment_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        #posting into the invoice item payments
        invoice_item_payment_list = request.data.get("invoice_item_list", [])
        for invoice_item_payment in invoice_item_payment_list:
            invoice_item_payment["payment_id"] = payment_id
        serializers = InvoiceItemPaymentSerializer(data=invoice_item_payment_list, many=True)
        if(serializers.is_valid()):
            serializers.save()
            data_to_return["invoice_item_list"] = serializers.data
        else:
            payment.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if(payment_data["payment_category"] == "prepayment"):
            data={}
            if(len(invoice_item_payment_list) != 0):
                payment.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            purchase_order_id = payment_data["purchase_order_id"]
            try:
                purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
            except PurchaseOrder.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if(purchase_order.buyer_id_id != entity_id):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            data["source_purchase_order_id"] = purchase_order_id
            data["seller_id"] = payment_data["to_entity_id"]
            data["buyer_id"] = entity_id
            data["entry_type"] = "prepayment"
            data["prepayment_payment_id"] = payment_id
            data["currency_code"] = payment_data["currency_code"]
            data["total_amount"] = payment_data["total_amount"]
            data["available_amount"] = payment_data["total_amount"]
            serializer = PaymentBalanceSerializer(data=data)
            if(serializer.is_valid()):
                serializer.save()
                data_to_return["payment_balance"] = serializer.data
            else:
                payment.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)

        elif(payment_data["payment_category"] == "invoice_payment"):
            if(len(invoice_item_payment_list) == 0):
                payment.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            payment_usage_list = request.data.get("balance_usage",[])
            # creating payment balance usage
            for payment_usage in payment_usage_list:
                try:
                    payment_balance = PaymentBalance.objects.get(balance_id=payment_usage.get("balance_id",0))
                except PaymentBalance.DoesNotExist:
                    payment.delete()
                    return Response(status=status.HTTP_404_NOT_FOUND)
                payment_usage["usage_type"] = "payment_adjustment"
                payment_usage["adjusted_payment_id"] = payment_id
            serializers = PaymentBalanceUsageSerializer(data=payment_usage_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                data_to_return["payment_balance_usage"] = serializer.data
            else:
                payment.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # updating the payment balance 
            balance_list = []
            for payment_usage in payment_usage_list:
                try:
                    balance_id = payment_usage["balance_id"]
                    payment_balance.used_amount = payment_usage["used_amount"]
                    payment_balance.available_amount = payment_usage["available_amount"]
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                payment_balance.comments = payment_usage.get("comments","")
                payment_balance.save()
                balance_list.append(PaymentBalanceSerializer(payment_balance).data)
            data_to_return["payment_balance"] = balance_list
        else:
            payment.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class proforma_prepayment(APIView):
    def post(self, request, user_id, entity_id, invoice_id):
        #can be done by buyer only
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        try:
            entity = Entity.objects.get(entity_id=entity_id)
        except Entity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            user_entity = UserEntity.objects.get(user_id=user_id, entity_id=entity_id, deleted_datetime__isnull=True)
        except UserEntity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            invoice = ProformaInvoice.objects.get(invoice_id=invoice_id)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if(invoice.buyer_id_id != entity_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data_to_return = {}
        payment_data = request.data.get("payment_info",{})
        payment_data["created_by_user_id"] = user_id
        payment_data["from_entity_id"] = entity_id
        serializer = PaymentSerializer(data=payment_data)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["payment_info"] = serializer.data
            payment_id = serializer.data.get("payment_id")
            payment = Payment.objects.get(payment_id=payment_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        purchase_order_id = invoice.purchase_order_id_id
        
        if(payment_data["payment_category"] != "prepayment"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data={}
        data["source_purchase_order_id"] = purchase_order_id
        data["seller_id"] = payment_data["to_entity_id"]
        data["buyer_id"] = entity_id
        data["entry_type"] = "prepayment"
        data["prepayment_payment_id"] = payment_id
        data["currency_code"] = payment_data["currency_code"]
        data["total_amount"] = payment_data["total_amount"]
        data["available_amount"] = payment_data["total_amount"]
        serializer = PaymentBalanceSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            data_to_return["payment_balance"] = serializer.data
        else:
            payment.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        invoice.amount_paid = (round(Decimal(invoice.amount_paid), DECIMAL_COMPARISON_PRECISION)) + (round(Decimal(payment_data["total_amount"]), DECIMAL_COMPARISON_PRECISION))
        if(invoice.amount_paid >= (round(Decimal(invoice.amount_invoiced), DECIMAL_COMPARISON_PRECISION))):
            invoice.status = "complete"
        invoice.save()
        
        return Response(data=data_to_return, status=status.HTTP_201_CREATED)

class invoice_item_payment_list(APIView):
    def get(self,request, invoice_line_item_id):
        invoice_item_payment = InvoiceItemPayment.objects.filter(invoice_line_item_id=invoice_line_item_id)
        serializers = InvoiceItemPaymentSerializer(invoice_item_payment, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

class payment_balance_list_from_purchase_order(APIView):
    #  list of payment balances with po_id      
    def get(self, request, purchase_order_id):
        try:
            purchase_order = PurchaseOrder.objects.get(purchase_order_id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        payment_balance_list = PaymentBalance.objects.filter(source_purchase_order_id=purchase_order_id)
        serializers = PaymentBalanceSerializer(payment_balance_list, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

class payment_balance_list(APIView):    
    # payment balance list with buyer_id and seller_id (where available amount >0)
    def get(self, request, buyer_id, seller_id):
        try:
            buyer = Buyer.objects.get(buyer_id=buyer_id)
        except Buyer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            seller = Seller.objects.get(seller_id=seller_id)
        except Seller.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        payment_balance_list =PaymentBalance.objects.filter(buyer_id=buyer_id, seller_id=seller_id)
        serializers_data = PaymentBalanceSerializer(payment_balance_list, many=True).data
        data = []
        for serializer_data in serializers_data:
            if(float(serializer_data["available_amount"]) > 0):
                data.append(serializer_data)
        return Response(data=data, status=status.HTTP_200_OK)