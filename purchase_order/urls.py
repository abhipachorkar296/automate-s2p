from django.urls import path
from purchase_order import views

app_name = 'purchase_order'
urlpatterns = [
    path("hello", views.hello.as_view(), name="hello"),
    path("entity_identification_list", views.entity_identification_list.as_view(), name="entity_identification_list"),
    path("entity_default_identification_list", views.entity_default_identification_list.as_view(), name="entity_default_identification_list"),
    path("draft_purchase_order/<int:purchase_order_id>", views.draft_purchase_order.as_view(), name="draft_purchase_order"),
    path("draft_purchase_order_list/<int:event_id>/<int:seller_id>", views.draft_purchase_order_list.as_view(), name="draft_purchase_order_list"),
    path("purchase_order/<int:purchase_order_id>", views.purchase_order.as_view(), name="purchase_order"),
    path("award_status_from_purchase_order/<int:purchase_order_id>", views.award_status_from_purchase_order.as_view(), name="award_status_from_purchase_order"),
    path("seller_purchase_order_response/<int:user_id>/<int:entity_id>/<int:purchase_order_id>", views.seller_purchase_order_response.as_view(), name="seller_purchase_order_response"),
    path("draft_purchase_order_shift_purchase_order/<int:purchase_order_id>", views.draft_purchase_order_shift_purchase_order.as_view(), name="draft_purchase_order_shift_purchase_order"),
    path("purchase_order_from_award/<int:award_id>", views.purchase_order_from_award.as_view(), name="purchase_order_from_award"),
    path("purchase_order_accept_termination/<int:user_id>/<int:entity_id>/<int:purchase_order_id>", views.purchase_order_accept_termination.as_view(), name="purchase_order_accept_termination"),
    path("purchase_order_list/<int:event_id>", views.purchase_order_list.as_view(), name="purchase_order_list"),
    path("latest_purchase_order/<int:event_id>/<int:seller_id>", views.latest_purchase_order.as_view(), name="lastest_purchase_order"),
    path("shift_purchase_order_to_draft_purchase_order/<int:purchase_order_id>", views.shift_purchase_order_to_draft_purchase_order.as_view(), name="shift_purchase_order_to_draft_purchase_order"),
    path("purchase_order_termination_request/<int:user_id>/<int:entity_id>/<int:purchase_order_id>", views.purchase_order_termination_request.as_view(), name="purchase_order_termination_request"),
    path("purchase_order_undo_termination_request/<int:user_id>/<int:entity_id>/<int:purchase_order_id>", views.purchase_order_undo_termination_request.as_view(), name="purchase_order_undo_termination_request"),
    path("event_purchase_order_list/<int:event_id>", views.event_purchase_order_list.as_view(), name="event_purchase_order_list"),
    path("rescind_purchase_order/<int:user_id>/<int:purchase_order_id>", views.rescind_purchase_order.as_view(), name="rescind_purchase_order"),
    path("buyer_purchase_order_tab_count/<int:user_id>", views.buyer_purchase_order_tab_count.as_view(), name="buyer_purchase_order_tab_count"),
    path("buyer_purchase_order_tab_info/<int:user_id>/<str:tab_name>", views.buyer_purchase_order_tab_info.as_view(), name="buyer_purchase_order_tab_info"),
    path("seller_purchase_order_tab_count/<int:user_id>", views.seller_purchase_order_tab_count.as_view(), name="seller_purchase_order_tab_count"),
]