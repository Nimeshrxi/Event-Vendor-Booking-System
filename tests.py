from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from .models import Items, Bookings, BookingItem
from .services import get_available_quantity
# Create your tests here.

class AvailabilityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pass123")
        self.tent = Items.objects.create(name="Tent", total_quantity=10, price_per_day=100)
        
    def test_no_bookings_gives_full_stock(self):
        free = get_available_quantity(self.tent, date(2026, 11, 10), date(2026, 11, 15))
        self.assertEqual(free, 10)