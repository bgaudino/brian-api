from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User
from .models import Workout, Exercise, Set
from .serializers import WorkoutSerializer, ExerciseSerializer, SetSerializer


class WorkoutListView(APIView):
    def get(self, request):
        workouts = Workout.objects.all()
        data = WorkoutSerializer(workouts, many=True).data
        return Response(data)

    def post(self, request):
        user = User.objects.all().first()
        workout = Workout.objects.create(user=user)
        return Response(WorkoutSerializer(workout).data)


class WorkoutView(APIView):
    def get(self, request, id):
        workout = Workout.objects.get(id=id)
        data = WorkoutSerializer(workout).data
        return Response(data)

    def delete(self, request, id):
        workout = Workout.objects.get(id=id)
        workout.delete()
        return Response(status=204)


class ExerciseCreateUpdateView(APIView):
    def post(self, request):
        workout = Workout.objects.get(id=request.data["workout_id"])
        exercise = Exercise.objects.create(
            workout=workout,
            exercise_name=request.data["exercise_name"]
        )
        data = ExerciseSerializer(exercise).data
        return Response(data)

    def put(self, request):
        exercise = Exercise.objects.get(id=request.data["exercise_id"])
        for key, value in request.data.items():
            if key != "exercise_id":
                setattr(exercise, key, value)
        exercise.save()
        data = ExerciseSerializer(exercise).data
        return Response(data)


class ExerciseDeleteView(APIView):
    def delete(self, request, id):
        exercise = Exercise.objects.get(id=id)
        exercise.delete()
        return Response(status=204)


class SetCreateUpdateView(APIView):
    def post(self, request):
        exercise_id = request.data["exercise_id"]
        exercise = Exercise.objects.get(id=exercise_id)
        set = Set.objects.create(
            exercise=exercise,
            weight=request.data["weight"],
            reps=request.data["reps"])
        data = SetSerializer(set).data
        return Response(data)

    def put(self, request):
        set_id = request.data["id"]
        set = Set.objects.get(id=set_id)
        for key, value in request.data.items():
            if key in ["reps", "weight"]:
                setattr(set, key, value)
        set.save()
        data = SetSerializer(set).data
        return Response(data)


class SetDeleteView(APIView):
    def delete(self, request, id):
        set = Set.objects.get(id=id)
        set.delete()
        return Response(status=204)
