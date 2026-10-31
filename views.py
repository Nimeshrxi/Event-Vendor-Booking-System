from datetime import date
from rest_framework.response import Response
from .services import get_available_quantity
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Items, Bookings, BookingItem
from .serializers import BookingCreateSerializer

# Create your views here.

@api_view(["GET"])
def availability(request):
    item_id = request.query_params.get("item")
    start = request.query_params.get("start")
    end = request.query_params.get("end")
    
    if not item_id or not start or not end:
        return Response({"error": "item, start and end are required"}, status=400)
    
    try:
        start = date.fromisoformat(start)
        end = date.fromisoformat(end)
    except ValueError:
        return Response({"error": "invalid date, use YYYY-MM-DD"}, status=400)
    if end < start:
        return Response({"error": "end must not be before start"}, status=400)
    
    try:
        item = Items.objects.get(id=item_id)
    except (Items.DoesNotExist, ValueError):
        return Response({"error": "An Item must be there or a correct one"}, status=404)
    
    return Response({"item": item.name, "available": get_available_quantity(item, start, end)})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request):
    s = BookingCreateSerializer(data=request.data)
    if not s.is_valid():
        return Response(s.errors, status=400)
    data = s.validated_data
    
    with transaction.atomic():
        booking = Bookings.objects.create(
            customer=request.user,
            start_date=data["start_date"],
            end_date=data["end_date"],
        )
        
        for row in data["items"]:
            BookingItem.objects.create(
                booking=booking, item=row["item"], quantity=row["quantity"]
            )
            
    return Response({"booking_id": booking.id, "status": booking.status}, status=201)
