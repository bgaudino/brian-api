from rest_framework import serializers

from .models import Workout, Exercise, Set, CardioSession, StravaAccount


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('id', 'reps', 'weight', 'exercise', 'created_at')


class ExerciseSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ('id', 'exercise_name', 'sets')


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ('id', 'start_date', 'exercises', 'exercises')


class CardioSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardioSession
        fields = (
            'id',
            'start_date',
            'start_date_local',
            'name',
            'distance', 
            'moving_time', 
            'total_elevation_gain',
            'average_speed', 
            'max_speed', 
            'has_heartrate', 
            'average_heartrate',
            'max_heartrate',
        )

class StravaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = StravaAccount
        fields = (
            'id',
            'avatar',
            'first_name',
            'last_name',
            'username',
        )