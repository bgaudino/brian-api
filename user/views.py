from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer


class CurrentUserView(APIView):
    def get(self, request):
        print(request.user)
        if not request.user.is_authenticated:
            return Response({'detail': 'Not authenticated'}, status=401)
        response = UserSerializer(request.user).data
        print(response)
        return Response(response)
