from rest_framework import serializers
from .models import Items
from .services import get_available_quantity

class BookingItemInputSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())
    quantity = serializers.IntegerField(min_value=1)
    
class BookingCreateSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    items = BookingItemInputSerializer(many=True, allow_empty=False)
    
    def validate(self, data):
        if data["end_date"] < data["start_date"]:
            raise serializers.ValidationError("end_date must not be before start_date")
        for row in data["items"]:
            free = get_available_quantity(row["item"], data["start_date"], data["end_date"])
            if row["quantity"] > free:
                raise serializers.ValidationError(f"Only {free} of {row['item'].name} available")
        return data