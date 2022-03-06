from uuid import uuid4
from django.db.models import (
    Model, UUIDField, CharField, DateTimeField, ForeignKey,
    CASCADE, EmailField, TextField, IntegerField, FloatField
)


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

    @staticmethod
    def filter_by_name(name):
        try:
            return Trip.objects.filter(name=name)
        except Trip.DoesNotExist:
            return []

    @staticmethod
    def filter_by_owner(owner_id):
        try:
            return Trip.objects.filter(owner_id=owner_id)
        except Trip.DoesNotExist:
            return []


class TripCompanion(Model):
    class Meta:
        db_table = 'Companion'

    # id = IntegerField(primary_key=True)
    trip_id = ForeignKey(Trip, on_delete=CASCADE)
    user_id = ForeignKey(User, on_delete=CASCADE)

    # Meta fields (debugging purposes)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f'Trip {self.trip_id} - companion {self.user_id}'
