import requests
from datetime import datetime, timedelta

from django.utils.timezone import make_aware, now
from django.db.models import Sum, Count

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from config.settings import (
    STRAVA_CLIENT_ID,
    STRAVA_CLIENT_SECRET,
    STRAVA_WEBHOOK_VERIFY_TOKEN,
)
from .models import Workout, Exercise, Set, StravaAccount, CardioSession
from .serializers import (
    WorkoutSerializer,
    ExerciseSerializer,
    SetSerializer,
    CardioSessionSerializer,
    StravaAccountSerializer,
)


class WorkoutListView(APIView):
    def get(self, request):
        workouts = Workout.objects.filter(user=request.user).order_by("-start_date")
        data = WorkoutSerializer(workouts, many=True).data
        return Response(data)

    def post(self, request):
        workout = Workout.objects.create(user=request.user)
        return Response(WorkoutSerializer(workout).data)


class WorkoutView(APIView):
    def get(self, request, id):
        try:
            workout = Workout.objects.get(id=id, user=request.user)
        except Workout.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = WorkoutSerializer(workout).data
        return Response(data)

    def delete(self, request, id):
        workout = Workout.objects.get(id=id, user=request.user)
        workout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExerciseCreateUpdateView(APIView):
    def post(self, request):
        workout = Workout.objects.get(id=request.data["workout_id"], user=request.user)
        exercise = Exercise.objects.create(
            workout=workout, exercise_name=request.data["exercise_name"]
        )
        data = ExerciseSerializer(exercise).data
        return Response(data)

    def put(self, request):
        exercise = Exercise.objects.get(
            id=request.data["exercise_id"], workout__user=request.user
        )
        for key, value in request.data.items():
            if key != "exercise_id":
                setattr(exercise, key, value)
        exercise.save()
        data = ExerciseSerializer(exercise).data
        return Response(data)


class ExerciseDeleteView(APIView):
    def delete(self, request, id):
        exercise = Exercise.objects.get(id=id, workout__user=request.user)
        exercise.delete()
        return Response(status=204)


class SetCreateUpdateView(APIView):
    def post(self, request):
        exercise_id = request.data["exercise_id"]
        exercise = Exercise.objects.get(id=exercise_id, workout__user=request.user)
        set = Set.objects.create(
            exercise=exercise, weight=request.data["weight"], reps=request.data["reps"]
        )
        data = SetSerializer(set).data
        return Response(data)

    def put(self, request):
        set_id = request.data["id"]
        set = Set.objects.get(id=set_id, exercise__workout__user=request.user)
        for key, value in request.data.items():
            if key in ["reps", "weight"]:
                setattr(set, key, value)
        set.save()
        data = SetSerializer(set).data
        return Response(data)


class SetDeleteView(APIView):
    def delete(self, request, id):
        set = Set.objects.get(id=id, exercise__workout__user=request.user)
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

        user = request.user
        try:
            account = StravaAccount.objects.get(strava_id=data["athlete"]["id"])
            if account.user != user:
                return Response(
                    {"detail": "Account already authenticated by another user"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            print("Athlete already exists. Updating")
        except:
            account = StravaAccount(user=user, strava_id=data["athlete"]["id"])
            print("Creating new athlete")
        account.token_type = data["token_type"]
        account.expires_at = make_aware(datetime.utcfromtimestamp(data["expires_at"]))
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
        offset = int(request.query_params.get("offset", 0)) * 10
        strava_accounts = StravaAccount.objects.filter(user=request.user)
        cardio_sessions = CardioSession.objects.filter(user=request.user).order_by(
            "-start_date"
        )
        weekly_stats = cardio_sessions.filter(
            start_date__gte=now() - timedelta(days=7)
        ).aggregate(
            runs=Count("id"), distance=Sum("distance"), duration=Sum("moving_time")
        )
        monthly_stats = cardio_sessions.filter(
            start_date__gte=now() - timedelta(days=30)
        ).aggregate(
            runs=Count("id"), distance=Sum("distance"), duration=Sum("moving_time")
        )
        yearly_stats = cardio_sessions.filter(
            start_date__gte=now() - timedelta(days=365)
        ).aggregate(
            runs=Count("id"), distance=Sum("distance"), duration=Sum("moving_time")
        )
        current_page = cardio_sessions[offset : offset + 10]

        data = {
            "strava_accounts": StravaAccountSerializer(strava_accounts, many=True).data,
            "cardio_sessions": CardioSessionSerializer(current_page, many=True).data,
            "count": cardio_sessions.count(),
            "weekly_stats": weekly_stats,
            "monthly_stats": monthly_stats,
            "yearly_stats": yearly_stats,
        }
        return Response(data)


class StravaWebhookView(APIView):
    def get(self, request):
        params = request.query_params
        print(params)
        if params.get("hub.verify_token") != STRAVA_WEBHOOK_VERIFY_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response({"hub.challenge": params.get("hub.challenge")})

    def post(self, request):
        owner_id = request.data["owner_id"]
        try:
            account = StravaAccount.objects.get(strava_id=owner_id)
        except StravaAccount.DoesNotExist:
            print("No account found")
            return Response(status=status.HTTP_202_ACCEPTED)

        object_type = request.data.get("object_type")
        aspect_type = request.data.get("aspect_type")
        if object_type == "activity":
            strava_id = request.data.get("object_id")
            if aspect_type == "create" or aspect_type == "update":
                account.get_single_activity(strava_id)
            if aspect_type == "delete":
                try:
                    CardioSession.objects.get(strava_id=strava_id).delete()
                except CardioSession.DoesNotExist:
                    print("Activity does not exist")
                    return Response(status=status.HTTP_202_ACCEPTED)

        return Response(status=200)
