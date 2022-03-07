from uuid import uuid4

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (
    Model, UUIDField, CharField, DateTimeField, ForeignKey,
    CASCADE, EmailField, TextField, IntegerField, FloatField
)


# TODO: move to separate 'user' API
class User(Model):
    class Meta:
        db_table = 'User'

    user_id = UUIDField(default=uuid4, primary_key=True, editable=False)
    name = CharField(max_length=30)
    email = EmailField()

    # Meta fields (debugging purposes)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_by_id(user_id):
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return []


class Trip(Model):
    class Meta:
        db_table = 'Trip'
        unique_together = ('owner_id', 'name')

    trip_id = UUIDField(default=uuid4, primary_key=True, editable=False)
    name = CharField(max_length=50)
    owner_id = ForeignKey(User, on_delete=CASCADE)
    starting_time = DateTimeField()
    duration = IntegerField()
    cost_estimation = FloatField()
    description = TextField(null=True, blank=True)

    # Meta fields (debugging purposes)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_by_id(trip_id):
        try:
            return Trip.objects.get(trip_id=trip_id)
        except Trip.DoesNotExist:
            return None

    # TODO: remove except - filter not rising exception
    @staticmethod
    def filter_by_name(name):
        try:
            return Trip.objects.filter(name=name)
        except Trip.DoesNotExist:
            return []

    # TODO: remove except - filter not rising exception
    @staticmethod
    def filter_by_owner(owner_id):
        try:
            return Trip.objects.filter(owner_id=owner_id)
        except Trip.DoesNotExist:
            return []


class TripCompanion(Model):
    class Meta:
        db_table = 'Companion'

    trip_id = ForeignKey(Trip, on_delete=CASCADE)
    user_id = ForeignKey(User, on_delete=CASCADE)

    # Meta fields (debugging purposes)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f'Trip {self.trip_id} - companion {self.user_id}'


class City(Model):
    class Meta:
        db_table = 'City'

    city_id = UUIDField(default=uuid4, primary_key=True, editable=False)
    city_name = CharField(max_length=30)
    country = CharField(max_length=30)
    population = IntegerField(validators=[MinValueValidator(0)])
    rating = FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    # Meta fields (debugging purposes)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.city_name

    @staticmethod
    def get_by_id(city_id):
        try:
            return City.objects.get(city_id=city_id)
        except City.DoesNotExist:
            return None


class TripCity(Model):
    class Meta:
        db_table = 'TripCity'

    city = ForeignKey(City, on_delete=CASCADE)
    trip = ForeignKey(Trip, on_delete=CASCADE)
    dest_city_order = IntegerField(validators=[MinValueValidator(1)])

    # Meta fields (debugging purposes)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f'Trip {self.trip} - Dest {self.city}. Stop nb {self.dest_city_order}'
