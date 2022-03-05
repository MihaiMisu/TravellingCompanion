from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, UUIDField, ListField, FloatField, IntegerField, DateTimeField

from .models import Trip, User
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
