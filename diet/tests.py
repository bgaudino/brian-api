from django.test import TestCase
from django.utils.timezone import now

from user.models import User
from . import models


class ConsumedFoodTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@test.com")
        self.pizza = models.Food.objects.create(
            name="Pizza",
            calories=400,
            fat=20,
            protein=20,
            carbs=60,
            user=self.user,
        )

    def test_duplicate_food(self):
        models.ConsumedFood.objects.create(
            user=self.user, food=self.pizza, servings=1, date=now()
        )
        models.ConsumedFood.objects.create(
            user=self.user, food=self.pizza, servings=2, date=now()
        )
        self.assertEqual(models.ConsumedFood.objects.count(), 1)
        self.assertEqual(models.ConsumedFood.objects.first().servings, 3)
