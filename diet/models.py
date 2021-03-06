import datetime

from django.db import models
from django.db.models import F, Sum
from django.conf import settings


class Food(models.Model):
    name = models.CharField(max_length=200)
    calories = models.IntegerField()
    fat = models.DecimalField(decimal_places=1, max_digits=4)
    protein = models.DecimalField(decimal_places=1, max_digits=4)
    carbs = models.DecimalField(decimal_places=1, max_digits=4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "user")

    def __str__(self):
        return self.name


class ConsumedFoodManager(models.Manager):
    def with_totals(self, **kwargs):
        return self.filter(**kwargs).annotate(
            total_calories=F("servings") * F("food__calories"),
            total_fat=F("servings") * F("food__fat"),
            total_protein=F("servings") * F("food__protein"),
            total_carbs=F("servings") * F("food__carbs"),
        )

    def by_day_with_totals(self, days=7, **kwargs):
        date = datetime.date.today() - datetime.timedelta(days=days)
        return (
            self.with_totals(date__gte=date)
            .extra(select={"day": "date(date)"})
            .values("day")
            .annotate(
                calories=Sum("total_calories"),
                fat=Sum("total_fat"),
                protein=Sum("total_protein"),
                carbs=Sum("total_carbs"),
            )
            .order_by("-day")
        )


class ConsumedFood(models.Model):
    date = models.DateField()
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servings = models.DecimalField(default=1, max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.food} - {self.date}"

    objects = ConsumedFoodManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                duplicate = ConsumedFood.objects.get(date=self.date, food=self.food)
                duplicate.servings = F("servings") + self.servings
                duplicate.save()
                return
            except ConsumedFood.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    @staticmethod
    def nutrition(queryset):
        return queryset.aggregate(
            calories=Sum("total_calories"),
            fat=Sum("total_fat"),
            protein=Sum("total_protein"),
            carbs=Sum("total_carbs"),
        )
