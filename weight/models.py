from django.db import models
from django.conf import settings


class WeighIn(models.Model):
    date = models.DateField()
    weight = models.DecimalField(decimal_places=1, max_digits=4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user} - {self.weight} - {self.date}'

    class Meta:
        unique_together = ('date', 'user')
