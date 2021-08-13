from django.urls import path
from invoice import views

app_name = 'invoice'
urlpatterns = [
    path("draft_invoice/<int:invoice_id>", views.draft_invoice.as_view(), name="draft_invoice"),
    path("draft_invoice_list/<int:user_id>/<int:purchase_order_id>", views.draft_invoice_list.as_view(), name="draft_invoice_list"),
    path("invoice_termination_request/<int:user_id>/<int:entity_id>/<int:invoice_id>", views.invoice_termination_request.as_view(), name="invoice_termination_request"),
    path("invoice_undo_termination_request/<int:user_id>/<int:entity_id>/<int:invoice_id>", views.invoice_undo_termination_request.as_view(), name="invoice_undo_termination_request"),
    path("rescind_invoice/<int:user_id>/<int:invoice_id>", views.rescind_invoice.as_view(), name="rescind_invoice"),
    path("invoice_accept_termination/<int:user_id>/<int:entity_id>/<int:invoice_id>", views.invoice_accept_termination.as_view(), name="invoice_accept_termination"),
    path("invoice/<int:invoice_id>", views.invoice.as_view(), name="invoice"),
    path("draft_invoice_shift_invoice/<int:invoice_id>", views.draft_invoice_shift_invoice.as_view(), name="draft_invoice_shift_invoice"),
    path("invoice_from_purchase_order/<int:purchase_order_id>", views.invoice_from_purchase_order.as_view(), name="invoice_from_purchase_order"),
    path("buyer_side_invoice_list/<int:user_id>", views.invoice_list.as_view(entity_type="Buyer"), name="buyer_side_invoice_list"),
    path("seller_side_invoice_list/<int:user_id>", views.invoice_list.as_view(entity_type="Seller"), name="seller_side_invoice_list"),
    path("invoice_list_for_new_goods/<int:purchase_order_id>", views.invoice_list_for_new_goods.as_view(), name="invoice_list_for_new_goods"),
    path("invoice_item_max_pending_quantity_list/<int:invoice_id>", views.invoice_item_max_pending_quantity_list.as_view(), name="invoice_item_max_pending_quantity_list"),
    path("proforma_invoice/<int:invoice_id>", views.proforma_invoice.as_view(), name="proforma_invoice"),
    path("proforma_invoice_list/<int:purchase_order_id>", views.proforma_invoice_list.as_view(), name="proforma_invoice_list"),
    path("invoice_status/<int:invoice_line_item_id>", views.invoice_status.as_view(), name="invoice_status"),
    path("non_fw_invoice/<int:purchase_order_id>", views.non_fw_invoice.as_view(), name="non_fw_invoice"),
    
]