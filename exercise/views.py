from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User
from .models import Session, Exercise, Set
from .serializers import SessionSerializer, ExerciseSerializer, SetSerializer


class SessionView(APIView):
    def get(self, request):
        sessions = Session.objects.all()
        data = SessionSerializer(sessions, many=True).data
        return Response(data)

    def post(self, request):
        user = User.objects.all().first()
        session = Session.objects.create(user=user)
        return Response(SessionSerializer(session).data)


class ExerciseCreateUpdateView(APIView):
    def post(self, request):
        session = Session.objects.get(id=request.data["session_id"])
        exercise = Exercise.objects.create(
            session=session,
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
