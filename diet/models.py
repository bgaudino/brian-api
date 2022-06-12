from django.db import models
from django.conf import settings


class Food(models.Model):
    name = models.CharField(max_length=200)
    calories = models.IntegerField()
    fat = models.DecimalField(decimal_places=1, max_digits=4)
    protein = models.DecimalField(decimal_places=1, max_digits=4)
    carbs = models.DecimalField(decimal_places=1, max_digits=4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name


class ConsumedFood(models.Model):
    date = models.DateField()
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user} - {self.food} - {self.date}'

    @staticmethod
    def nutrition(queryset):
        fields = ['calories', 'fat', 'protein', 'carbs']
        return {
            field: queryset.aggregate(sum=models.Sum(f'food__{field}'))['sum'] for field in fields
        }
