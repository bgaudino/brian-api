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

        
class ConsumedFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumedFood
        fields = (
            'date',
            'food',
        )
 
class ConsumedFoodListSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    class Meta:
        model = ConsumedFood
        fields = (
            'food',
            'id',
        )
        read_only_fields = ('id',)
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        food_representation = representation.pop('food')
        for key, value in food_representation.items():
            if key != 'id':
                representation[key] = value
            
        return representation
