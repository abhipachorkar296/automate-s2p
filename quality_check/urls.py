from django.urls import path
from quality_check import views

app_name = 'quality_check'
urlpatterns = [
    path("quality_check/<int:quality_check_id>", views.quality_check.as_view(), name="quality_check"),
    path("quality_check_list/<int:goods_receipt_entry_id>", views.quality_check_list.as_view(), name="quality_check_list"),

]