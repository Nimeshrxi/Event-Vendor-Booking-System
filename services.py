from django.db.models import Sum
from .models import BookingItem
from datetime import timedelta

def get_available_quantity(item, start, end):
    rows = (
        BookingItem.objects
        .filter(item=item, booking__start_date__lte=end, booking__end_date__gte=start,)
        .exclude(booking__status="cancelled")
        .select_related("booking")
    )
    
    events = []
    for r in rows:
        s = max(r.booking.start_date, start)
        e = min(r.booking.end_date, end)
        events.append((s,  r.quantity))
        events.append((e + timedelta(days=1), -r.quantity))
    events.sort()
    current = 0
    peak = 0
    
    for day, delta in events:
        current += delta
        peak = max(peak, current)
    return item.total_quantity - peak