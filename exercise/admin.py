from django.contrib import admin
import nested_admin
from .models import Session, Exercise, Set


class SetInline(nested_admin.NestedStackedInline):
    extra = 1
    model = Set

class ExerciseInline(nested_admin.NestedStackedInline):
    extra = 1
    model = Exercise
    inlines = [SetInline]

@admin.register(Session)
class SessionAdmin(nested_admin.NestedModelAdmin):
    inlines = [ExerciseInline]