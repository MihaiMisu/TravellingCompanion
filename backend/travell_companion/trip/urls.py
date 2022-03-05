from django.urls import path

from .views import TripAPI

urlpatterns = [
    path('manage', TripAPI.as_view())
]
