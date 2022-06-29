from django.urls import path

from . import views


urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo_list_view'),
    path('create/', views.todo_create_view, name='todo_create_view'),
    path('<int:pk>/complete/', views.todo_complete_view, name='todo_complete_view'),
]
