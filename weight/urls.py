from django.urls import path

from . import views


urlpatterns = [
    path('', views.WeighInListCreateView.as_view(), name='weigh_in_list_create'),
]
