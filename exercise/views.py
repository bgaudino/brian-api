import requests
from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import make_aware

from config.settings import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET
from user.models import User
from .models import Workout, Exercise, Set, StravaAccount, CardioSession, Map
from .serializers import WorkoutSerializer, ExerciseSerializer, SetSerializer, CardioSessionSerializer, StravaAccountSerializer


class WorkoutListView(APIView):
    def get(self, request):
        workouts = Workout.objects.all().order_by('-start_date')
        data = WorkoutSerializer(workouts, many=True).data
        return Response(data)

    def post(self, request):
        user = User.objects.all().first()
        workout = Workout.objects.create(user=user)
        return Response(WorkoutSerializer(workout).data)


class WorkoutView(APIView):
    def get(self, request, id):
        try:
            workout = Workout.objects.get(id=id)
        except Workout.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = WorkoutSerializer(workout).data
        return Response(data)

    def delete(self, request, id):
        workout = Workout.objects.get(id=id)
        workout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class StravaAuthView(APIView):
    def post(self, request):
        code = request.data["code"]
        body = {
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        }
        res = requests.post("https://www.strava.com/oauth/token", json=body)
        data = res.json()

        user = User.objects.all().first()
        try:
            account = StravaAccount.objects.get(
                strava_id=data["athlete"]["id"])
            print("Athlete already exists. Updating")
        except:
            account = StravaAccount(
                user=user,
                strava_id=data["athlete"]["id"]
            )
            print("Creating new athlete")
        account.token_type = data["token_type"]
        account.expires_at = make_aware(
            datetime.utcfromtimestamp(data["expires_at"]))
        account.access_token = data["access_token"]
        account.refresh_token = data["refresh_token"]
        account.username = data["athlete"]["username"]
        account.first_name = data["athlete"]["firstname"]
        account.last_name = data["athlete"]["lastname"]
        account.premium = data["athlete"]["premium"]
        account.created_at = data["athlete"]["created_at"]
        account.updated_at = data["athlete"]["updated_at"]
        account.avatar_medium = data["athlete"]["profile_medium"]
        account.avatar = data["athlete"]["profile"]
        account.save()
        print("Success")

        account.get_activities()

        return Response(data)


class CardioListView(APIView):
    def get(self, request):
        strava_accounts = StravaAccount.objects.all()
        cardio_sessions = CardioSession.objects.all()
        data = {
            "strava_accounts": StravaAccountSerializer(strava_accounts, many=True).data,
            "cardio_sessions": CardioSessionSerializer(cardio_sessions, many=True).data,
        }
        return Response(data)
