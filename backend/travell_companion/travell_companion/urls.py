from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trip/', include('trip.urls')),
    path('city/', include('city.urls')),
]
