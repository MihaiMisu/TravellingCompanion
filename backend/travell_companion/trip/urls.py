from django.urls import path

from .views import TripAPI, DestinationAPI

urlpatterns = [
    path('detail/', TripAPI.as_view()),
    path('detail/<uuid:trip_id>', TripAPI.as_view()),
    path('manage', TripAPI.as_view()),
    path('manage/<uuid:trip_id>', TripAPI.as_view()),
    path('manage/<uuid:trip_id>/destination', DestinationAPI.as_view()),
]
