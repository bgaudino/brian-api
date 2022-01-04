from django.urls import path
from . import views


urlpatterns = [
    path("scores/", views.ScoreListView.as_view(), name="score_list"),
]
