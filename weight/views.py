from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import WeighIn
from .serializers import WeighInSerializer


class WeighInListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WeighInSerializer

    def get_queryset(self):
        return WeighIn.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
