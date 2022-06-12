from django.contrib import admin

from . import models

@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ConsumedFood)
class ConsumedFood(admin.ModelAdmin):
    pass