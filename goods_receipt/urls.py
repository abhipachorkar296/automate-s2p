from django.urls import path
from goods_receipt import views

app_name = 'goods_receipt'
urlpatterns = [
    path("goods_receipt/<int:goods_receipt_entry_id>", views.goods_receipt.as_view(), name="goods_receipt"),
    path("goods_receipt_list/<int:invoice_id>", views.goods_receipt_list.as_view(), name="get_goods_receipt_list"),
    path("goods_receipt_list/<int:user_id>/<int:invoice_line_item_id>", views.goods_receipt_list.as_view(), name="post_goods_receipt_list"),
    path("goods_receipt_non_fw_invoice/<int:user_id>/<int:purchase_order_id>", views.goods_receipt_non_fw_invoice.as_view(), name="goods_receipt_non_fw_invoice")
    
]