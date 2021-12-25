from rest_framework import serializers

from .models import Session, Exercise, Set


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('id', 'reps', 'weight', 'exercise', 'created_at')


class ExerciseSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ('id', 'exercise_name', 'sets')


class SessionSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ('id', 'start_date', 'exercises', 'exercises')
