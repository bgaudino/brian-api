from django.urls import path
from . import views

urlpatterns = [
    path('shopping/purchase/<int:item_id>/',
         views.ItemPurchaseView.as_view(), name="item_purchase"),
    path('shopping/delete/<int:item_id>/',
         views.ItemDeleteView.as_view(), name="item_delete"),
    path('shopping/restore/<int:item_id>/',
         views.ItemRestoreView.as_view(), name="item_restore"),
    path('shopping/', views.ItemView.as_view(), name="item_view"),
    path('api/items/', views.ItemListAPIView.as_view(), name="item_list_api"),
    path('api/item/<int:item_id>/',
         views.ItemDetailAPIView.as_view(), name="item_detail_api"),
]
