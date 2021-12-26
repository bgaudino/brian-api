from django.urls import path
from . import views


urlpatterns = [
    path("workouts/", views.WorkoutView.as_view()),
    path("delete/<int:id>/", views.ExerciseDeleteView.as_view()),
    path("create_or_update/", views.ExerciseCreateUpdateView.as_view()),
    path("set/delete/<int:id>/", views.SetDeleteView.as_view()),
    path("set/create_or_update/", views.SetCreateUpdateView.as_view()),
]
