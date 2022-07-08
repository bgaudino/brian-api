from rest_framework.serializers import ModelSerializer
from .models import Item


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "store", "is_purchased", "purchased_at")
