from django.db import models
from user.models import User


class Score(models.Model):
    GAME_TYPES = (
        ("note_id", "Note Identification"),
        ("interval_ear_training", "Interval Ear Training"),
    )
    date = models.DateTimeField(auto_now_add=True)
    game_type = models.CharField(max_length=50, choices=GAME_TYPES)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="scores", null=True, blank=True
    )
    num_correct = models.IntegerField(default=0)
    num_attempted = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.percentage = (
            ((self.num_correct / self.num_attempted) * 100) if self.num_attempted else 0
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.name}: ({self.num_correct}/{self.num_attempted}) {self.percentage}%"
        )
