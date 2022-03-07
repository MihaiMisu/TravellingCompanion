from django.http import JsonResponse
from django.apps import apps
from django.forms.models import model_to_dict

from .validators import CityPostSerializer, CityPutSerializer
from backend.travell_companion.utils import APIView, get_payload, logger


class CityAPI(APIView):
    CityModel = apps.get_model('trip', 'City')

    def get(self, _, city_id=None):
        if not city_id:
            cities = [*self.CityModel.objects.values()]
            return JsonResponse({'success': cities, 'error': {}})

        obj = self.CityModel.objects.get(city_id=city_id)
        obj = model_to_dict(obj)
        return JsonResponse({'success': obj, 'error': {}})

    def post(self, request):
        # Load JSON body and validate
        req_data = get_payload(request.body)
        body = CityPostSerializer(data=req_data)
        if not body.is_valid():
            return JsonResponse({'error': body.errors}, status=400)
        req_data = body.data

        logger.debug(req_data)

        city = self.CityModel(
            city_name=req_data['cityName'],
            country=req_data['country'],
            population=req_data['population'],
            rating=req_data['rating']
        )
        city.save()
        logger.info(f'Saved new city: {city.city_name} ({city.city_id})')

        return JsonResponse({'success': req_data, 'error': {}})

    def put(self, request, city_id):
        # Load JSON body and validate
        req_data = get_payload(request.body)
        body = CityPutSerializer(city_id, data=req_data)
        if not body.is_valid():
            return JsonResponse({'error': body.errors}, status=400)
        req_data = body.data

        city = self.CityModel.objects.get(city_id=city_id)
        city.city_name = req_data['cityName']
        city.country = req_data['country']
        city.population = req_data['population']
        city.rating = req_data['rating']
        city.save()
        logger.info(f'City {city_id} updated')

        return JsonResponse({'success': req_data, 'error': {}})
