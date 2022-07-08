from datetime import date, timedelta

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Food, ConsumedFood
from .serializers import (
    ByDayWithTotalsSerializer,
    ConsumedFoodListSerializer,
    ConsumedFoodSerializer,
    FoodSerializer,
)


class FoodListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FoodSerializer

    def get_queryset(self):
        return Food.objects.filter(user=self.request.user).order_by("name")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConsumedFoodListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsumedFoodListSerializer

    def get_queryset(self):
        return ConsumedFood.objects.with_totals(
            user=self.request.user, date=self.kwargs.get("date", date.today())
        )

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        weekly_nutrition = ConsumedFood.objects.by_day_with_totals(days=7)

        return Response(
            {
                "food": ConsumedFoodListSerializer(queryset, many=True).data,
                "nutrition": ConsumedFood.nutrition(queryset),
                "weekly_nutrition": ByDayWithTotalsSerializer(
                    weekly_nutrition, many=True
                ).data,
            }
        )


class ConsumedFoodCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsumedFoodSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConsumedFoodDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ConsumedFood.objects.filter(user=self.request.user)
