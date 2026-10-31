from django.urls import path
from . import views

urlpatterns = [
    path("availability/", views.availability),
    path("bookings/", views.create_booking),
]