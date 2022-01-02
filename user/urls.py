from django.urls import path
from . import views

urlpatterns = [
    path('', views.CurrentUserView.as_view(), name='current_user'),
    path('register/', views.CreateUserView.as_view(), name='register'),
]
