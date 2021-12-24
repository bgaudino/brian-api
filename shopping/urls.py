from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItemView.as_view(), name="item_view"),
    path('purchase/<int:item_id>/', views.ItemPurchaseView.as_view(), name="item_purchase"),
    path('delete/<int:item_id>/', views.ItemDeleteView.as_view(), name="item_delete"),
    path('restore/<int:item_id>/', views.ItemRestoreView.as_view(), name="item_restore"),
]
