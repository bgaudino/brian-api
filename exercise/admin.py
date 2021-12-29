from django.contrib import admin
import nested_admin
from .models import Workout, Exercise, Set, StravaAccount, CardioSession, Map


class SetInline(nested_admin.NestedStackedInline):
    extra = 1
    model = Set


class ExerciseInline(nested_admin.NestedStackedInline):
    extra = 1
    model = Exercise
    inlines = [SetInline]


@admin.register(Workout)
class WorkoutAdmin(nested_admin.NestedModelAdmin):
    inlines = [ExerciseInline]


admin.site.register(StravaAccount)
admin.site.register(CardioSession)
admin.site.register(Map)
