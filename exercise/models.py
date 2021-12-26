from django.db import models
from user.models import User


class Workout(models.Model):
    user = models.ForeignKey(
        User,
        related_name="users",
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.start_date.strftime('%m%d%y')}: {self.user.email}"


class Exercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        related_name="exercises",
        on_delete=models.CASCADE,
    )
    exercise_name = models.CharField(max_length=100)

    def __str__(self):
        return self.exercise_name


class Set(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    exercise = models.ForeignKey(
        Exercise,
        related_name="sets",
        on_delete=models.CASCADE,
    )
    weight = models.IntegerField()
    reps = models.IntegerField()
