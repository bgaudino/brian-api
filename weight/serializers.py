from rest_framework import serializers

from .models import WeighIn


class WeighInSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeighIn
        fields = (
            "date",
            "weight",
            "id",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        weigh_in = WeighIn.objects.update_or_create(
            user=validated_data["user"],
            date=validated_data["date"],
            defaults={"weight": validated_data["weight"]},
        )[0]
        return weigh_in
