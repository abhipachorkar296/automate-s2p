from django.urls import path
from payment import views

app_name = 'payment'
urlpatterns = [
    # path("hello", views.hello.as_view(), name="hello"),
    path("payment/<int:payment_id>", views.payment.as_view(), name="payment"),
    path("payment_from_invoice/<int:invoice_id>", views.payment_from_invoice.as_view(), name="payment_from_invoice"),
    path("payment_list_buyer/<int:user_id>", views.payment_list.as_view(entity_type="Buyer"), name="buyer_payment_list"),
    path("payment_list_seller/<int:user_id>", views.payment_list.as_view(entity_type="Seller"), name="seller_payment_list"),
    path("payment_list/<int:user_id>/<int:entity_id>", views.payment_list.as_view(), name="post_payment"),
    path("invoice_item_payment_list/<int:invoice_line_item_id>", views.invoice_item_payment_list.as_view(), name="invoice_item_payment_list"),
    path("payment_balance_list_from_purchase_order/<int:purchase_order_id>", views.payment_balance_list_from_purchase_order.as_view(), name="payment_balance_list_from_purchase_order"),
    path("payment_balance_list/<int:buyer_id>/<int:seller_id>", views.payment_balance_list.as_view(), name="payment_balance_list"),
    path("proforma_prepayment/<int:user_id>/<int:entity_id>/<int:invoice_id>", views.proforma_prepayment.as_view(), name="proforma_prepayment"),
]