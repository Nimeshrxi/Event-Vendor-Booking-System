from django.contrib import admin 
from .models import Items, Bookings, BookingItem

# Register your models here.

admin.site.register(Items)
admin.site.register(Bookings)
admin.site.register(BookingItem)