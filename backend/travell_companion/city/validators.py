from django.apps import apps

from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, FloatField, IntegerField, ValidationError

from backend.travell_companion.utils import logger


class CityPostSerializer(Serializer):
    cityName = CharField(required=True, max_length=30)
    country = CharField(required=True, max_length=30)
    population = IntegerField(required=False, min_value=0, default=0)
    rating = FloatField(required=False, min_value=0, max_value=5, default=0)

    def validate(self, data):
        CityModel = apps.get_model('trip', 'City')
        if CityModel.objects.filter(city_name=data['cityName'], country=data['country']):
            err_msg = f"City - Country ({data['cityName']} - {data['country']}) already exists"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        return data


class CityPutSerializer(CityPostSerializer):

    def __init__(self, city_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city_id = city_id

    def validate(self, data):
        CityModel = apps.get_model('trip', 'City')

        city = CityModel.get_by_id(self.city_id)
        if not city:
            err_msg = 'City not found'
            logger.error(err_msg)
            raise ValidationError(err_msg)

        if CityModel.objects.filter(city_name=data['cityName'], country=data['country']):
            err_msg = f"City - Country ({data['cityName']} - {data['country']}) already exists"
            logger.error(err_msg)
            raise ValidationError(err_msg)

        return data
