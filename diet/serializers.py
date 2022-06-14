from rest_framework import serializers

from .models import ConsumedFood, Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = (
            'name',
            'calories',
            'fat',
            'carbs',
            'protein',
            'id',
        )
        read_only_fields = ('id',)


class FoodNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('name',)


class ConsumedFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumedFood
        fields = (
            'date',
            'food',
            'servings',
        )


class ConsumedFoodListSerializer(serializers.ModelSerializer):
    food = FoodNameSerializer()
    total_calories = serializers.IntegerField()
    total_fat = serializers.IntegerField()
    total_protein = serializers.IntegerField()
    total_carbs = serializers.IntegerField()

    class Meta:
        model = ConsumedFood
        fields = (
            'food',
            'id',
            'servings',
            'total_calories',
            'total_fat',
            'total_protein',
            'total_carbs',
        )
        read_only_fields = ('id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        food_representation = representation.pop('food')
        for key, value in food_representation.items():
            if key == 'id':
                continue
            representation[key] = value

        return representation


class ByDayWithTotalsSerializer(serializers.Serializer):
    day = serializers.DateField()
    calories = serializers.IntegerField()
    fat = serializers.DecimalField(decimal_places=1, max_digits=4)
    protein = serializers.DecimalField(decimal_places=1, max_digits=4)
    carbs = serializers.DecimalField(decimal_places=1, max_digits=4)
