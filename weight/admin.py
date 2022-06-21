from django.contrib import admin

from .models import WeighIn


@admin.register(WeighIn)
class WeighInAdmin(admin.ModelAdmin):
    pass
