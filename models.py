from django.db import models
from django.conf import settings
# Create your models here.

class StatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"
    
class Items(models.Model):
    name = models.CharField(max_length=200)
    total_quantity = models.PositiveIntegerField(default=0)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.name

class Bookings(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
class BookingItem(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, related_name="booking_items")
    item = models.ForeignKey(Items, on_delete=models.PROTECT, related_name = "booking_items")
    quantity = models.PositiveIntegerField()