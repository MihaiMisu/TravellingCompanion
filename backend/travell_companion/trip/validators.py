from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, UUIDField, ListField, FloatField, IntegerField, DateTimeField

from .models import Trip, User, City, TripCity
from backend.travell_companion.utils import logger


class TripPostSerializer(Serializer):
    tripName = CharField(max_length=50)
    userId = UUIDField(required=True)
    startingTime = DateTimeField(required=True)
    duration = IntegerField(required=True, min_value=0)
    costEstimation = FloatField(required=True)
    description = CharField(required=False, allow_blank=True, max_length=500, default='')
    companions = ListField(required=True, allow_empty=True, child=UUIDField())

    def validate(self, data):
        """
        The validations bellow are meant to check any logic errors (like non existing user creating a trip).
        """

        # Check if user/trip creator exists
        if not User.get_by_id(data['userId']):
            err_msg = f"User ('{data['userId']}') does not exists"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # Check if there exists already a trip with the same name for a given user
        if Trip.filter_by_name(data['tripName']) and Trip.filter_by_owner(data['userId']):
            err_msg = f"A trip with the same name ('{data['tripName']}') already exists for this user {data['userId']}."
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # check if any selected companions are not registered users
        not_existing_companions = [str(c) for c in data['companions'] if not User.get_by_id(c)]
        if not_existing_companions:
            err_msg = f"Not existing companions/users: {','.join(not_existing_companions)}"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # check if the trip owner/user creator is not within the companions list
        if data['userId'] in data['companions']:
            err_msg = f'Trip owner cannot be within the companions list.'
            logger.error(err_msg)
            raise ValidationError(err_msg)

        return data


class TripPutSerializer(TripPostSerializer):
    def __init__(self, trip_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trip_id = trip_id

    def validate(self, data):
        """
        The validations bellow are meant to check any logic errors (like non existing user creating a trip).
        """
        if not Trip.get_by_id(self.trip_id):
            err_msg = f"Trip not found"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # Check if user/trip creator exists
        if not User.get_by_id(data['userId']):
            err_msg = f"User ('{data['userId']}') does not exists"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # check if any selected companions are not registered users
        not_existing_companions = [str(c) for c in data['companions'] if not User.get_by_id(c)]
        if not_existing_companions:
            err_msg = f"Not existing companions/users: {','.join(not_existing_companions)}"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # check if the trip owner/user creator is not within the companions list
        if data['userId'] in data['companions']:
            err_msg = f'Trip owner cannot be within the companions list.'
            logger.error(err_msg)
            raise ValidationError(err_msg)

        return data


class TripPatchSerializer(Serializer):
    tripName = CharField(required=False, max_length=50)
    userId = UUIDField(required=False)
    startingTime = DateTimeField(required=False)
    duration = IntegerField(required=False, min_value=0)
    costEstimation = FloatField(required=False)
    description = CharField(required=False, allow_blank=True, max_length=500)
    companions = ListField(required=False, allow_empty=True, child=UUIDField())

    def __init__(self, trip_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trip_id = trip_id

    def validate(self, data):
        """
        The validations bellow are meant to check any logic errors (like non existing user creating a trip).
        """

        if not Trip.get_by_id(self.trip_id):
            err_msg = f"Trip not found"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # Check if user/trip creator exists
        if 'userId' in data and not User.get_by_id(data['userId']):
            err_msg = f"User ('{data['userId']}') does not exists"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # # Check if there exists already a trip with the same name for a given user
        if Trip.filter_by_name(data.get('tripName')) and Trip.filter_by_owner(data.get('userId')):
            err_msg = f"A trip with the same name ('{data['tripName']}') already exists for this user {data['userId']}."
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # # check if any selected companions are not registered users
        not_existing_companions = [str(c) for c in data.get('companions', []) if not User.get_by_id(c)]
        if not_existing_companions:
            err_msg = f"Not existing companions/users: {','.join(not_existing_companions)}"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        # check if the trip owner/user creator is not within the companions list
        if data.get('userId') in data.get('companions'):
            err_msg = f'Trip owner cannot be within the companions list.'
            logger.error(err_msg)
            raise ValidationError(err_msg)

        return data


class TripCityPostSerializer(Serializer):
    cityId = UUIDField(required=True)
    destinationOrder = IntegerField(required=True, min_value=1)

    def __init__(self, trip_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trip_id = trip_id

    def validate(self, data):

        trip = Trip.get_by_id(self.trip_id)
        if not Trip.get_by_id(self.trip_id):
            err_msg = f"Trip not found"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        city = City.get_by_id(data['cityId'])
        if not city:
            err_msg = f"City {data['cityId']} does not exist."
            logger.error(err_msg)
            raise ValidationError(err_msg)

        if TripCity.objects.filter(trip=trip, dest_city_order=data['destinationOrder']):
            err_msg = f"Already existing destination nb {data['destinationOrder']} for trip {self.trip_id}"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        if TripCity.objects.filter(trip=trip, city=city):
            err_msg = 'Trip-City destination already existing with different order index.'
            logger.error(err_msg)
            raise ValidationError(err_msg)

        if TripCity.objects.filter(trip=trip, city=city, dest_city_order=data['destinationOrder']):
            err_msg = 'Trip-City-DestinationOrder already existing.'
            logger.error(err_msg)
            raise ValidationError(err_msg)

        return data
