from django.urls import path

from .views import CityAPI

urlpatterns = [
    path('detail/', CityAPI.as_view()),
    path('detail/<uuid:city_id>', CityAPI.as_view()),
    path('manage', CityAPI.as_view()),
    path('manage/<uuid:city_id>', CityAPI.as_view()),
]
