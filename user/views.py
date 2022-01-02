from django.db.utils import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from .models import User


class CurrentUserView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Not authenticated'}, status=401)
        response = UserSerializer(request.user).data
        return Response(response)


class CreateUserView(APIView):
    def post(self, request):
        if request.data["password"] != request.data["confirmation"]:
            return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(
                request.data["email"], request.data["email"], request.data["password"])
        except IntegrityError:
            return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(user).data)
