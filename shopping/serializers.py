from rest_framework.serializers import ModelSerializer, CharField, URLField
from .models import Item, ItemInstance


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ("photo",)


class ItemInstanceSerializer(ModelSerializer):
    name = CharField(required=False, source="item.name")
    url = URLField(required=False, read_only=True, source="item.get_photo_url")

    class Meta:
        model = ItemInstance
        fields = ("id", "name", "url", "store", "is_purchased", "purchased_at", "item")
