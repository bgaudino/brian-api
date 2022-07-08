from rest_framework import serializers

from .models import Workout, Exercise, Set, CardioSession, StravaAccount, Map


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ("id", "reps", "weight", "exercise", "created_at")


class ExerciseSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ("id", "exercise_name", "sets")


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ("id", "start_date", "exercises", "exercises")


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ("id", "summary_polyline")


class CardioSessionSerializer(serializers.ModelSerializer):
    map = MapSerializer(read_only=True)

    class Meta:
        model = CardioSession
        fields = (
            "id",
            "start_date",
            "start_date_local",
            "name",
            "distance",
            "moving_time",
            "total_elevation_gain",
            "average_speed",
            "max_speed",
            "has_heartrate",
            "average_heartrate",
            "max_heartrate",
            "map",
            "start_latitude",
            "start_longitude",
        )


class StravaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = StravaAccount
        fields = (
            "id",
            "avatar",
            "first_name",
            "last_name",
            "username",
        )
