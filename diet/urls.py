from datetime import date

from django.urls import path, register_converter

from . import views
from .converters import DateConverter


register_converter(DateConverter, 'yyyy-dd-mm')

urlpatterns = [
    path('create/', views.ConsumedFoodCreateView.as_view(), name='consumed_food_create_view'),
    path('food/', views.FoodListView.as_view(), name='food_list_view'),
    path('<yyyy-dd-mm:date>/', views.ConsumedFoodListView.as_view(), name='consumed_food_list_create_view'),
    path('<int:pk>/', views.ConsumedFoodDestroyView.as_view(), name='consumed_food_destroy_view'),
    path('', views.ConsumedFoodListView.as_view(), name='consumed_food_list_create_view_today'),
]
