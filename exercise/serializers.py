from rest_framework import serializers

from .models import Workout, Exercise, Set, CardioSession


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
            'name',
            'distance', 
            'moving_time', 
            'average_speed', 
            'max_speed', 
            'has_heartrate', 
            'average_heartrate',
            'max_heartrate',
        )
