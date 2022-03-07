from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Trip, User, TripCompanion, City, TripCity
from .validators import TripPostSerializer, TripPutSerializer, TripPatchSerializer, TripCityPostSerializer
from backend.travell_companion.utils import APIView, get_payload, logger


class TripAPI(APIView):

    def get(self, _, trip_id=None):
        if not trip_id:
            trips = [*Trip.objects.values()]
            return JsonResponse({'success': trips, 'error': {}}, status=200)

        # Get trip by ID and convert to dict
        trip = Trip.get_by_id(trip_id)
        trip_details = model_to_dict(trip or Trip())

        # Get trip companions and add data to dict
        companions = TripCompanion.objects.filter(trip_id=trip)
        trip_details.update({
            'companions': [{'user_id': obj.user_id.user_id, 'user_name': obj.user_id.name} for obj in companions]
        })

        return JsonResponse({'success': trip_details, 'error': {}})

    def post(self, request):
        # Load JSON body and validate
        req_data = get_payload(request.body)
        body = TripPostSerializer(data=req_data)
        if not body.is_valid():
            return JsonResponse({'error': body.errors}, status=400)
        req_data = body.data

        # Create new trip and add companions (if exist)
        user = User.objects.get(user_id=req_data['userId'])
        trip = Trip(
            name=req_data['tripName'],
            owner_id=user,
            starting_time=req_data['startingTime'],
            duration=req_data['duration'],
            cost_estimation=req_data['costEstimation'],
            description=req_data['description']
        )
        trip.save()
        logger.info(f'Trip {trip.trip_id} created and saved.')

        companion_qset = User.objects.filter(user_id__in=req_data['companions'])
        TripCompanion.objects.bulk_create(
            [TripCompanion(trip_id=trip, user_id=c) for c in companion_qset]
        )
        len(companion_qset) and logger.info(f"Saved companions {req_data['companions']} to trip {trip.trip_id}")

        return JsonResponse({'success': req_data, 'error': {}}, status=201)

    def put(self, request, trip_id):
        req_data = get_payload(request.body)
        body = TripPutSerializer(trip_id, data=req_data)
        if not body.is_valid():
            return JsonResponse({'error': body.errors}, status=400)
        req_data = body.data

        # Update Trip in DB
        user = User.objects.get(user_id=req_data['userId'])

        trip = Trip.get_by_id(trip_id)
        trip.name = req_data['tripName']
        trip.owner_id = user
        trip.starting_time = req_data['startingTime']
        trip.duration = req_data['duration']
        trip.cost_estimation = req_data['costEstimation']
        trip.description = req_data['description']
        trip.save()
        logger.info(f'Trip {trip.trip_id} updated and saved.')

        # 3. Delete companions for trip.
        deleted_companions = TripCompanion.objects.filter(trip_id=trip_id).delete()
        logger.info(f'Removed all ({deleted_companions}) companions from trip {trip_id}')

        # 4. Insert new list of companions (if any new item).
        companion_qset = User.objects.filter(user_id__in=req_data['companions'])
        TripCompanion.objects.bulk_create(
            [TripCompanion(trip_id=trip, user_id=c) for c in companion_qset]
        )
        len(companion_qset) and logger.info(f"Saved companions {req_data['companions']} to trip {trip.trip_id}")

        return JsonResponse({'success': req_data, 'error': {}})

    def patch(self, request, trip_id):
        trip_request2model_mapping = {
            'tripName': 'name',
            'userId': 'owner_id',
            'startingTime': 'starting_time',
            'duration': 'duration',
            'costEstimation': 'cost_estimation',
            'description': 'description',
        }

        req_data = get_payload(request.body)
        body = TripPatchSerializer(trip_id, data=req_data)
        if not body.is_valid():
            return JsonResponse({'error': body.errors}, status=400)
        req_data = body.data

        trip = Trip.get_by_id(trip_id)
        for field in trip_request2model_mapping:
            if req_data.get(field) is not None:
                setattr(trip, trip_request2model_mapping[field], req_data[field])
        trip.save()
        logger.info(f"Trip '{trip_id}' updated and saved.")

        if req_data.get('companions'):
            # 3. Delete companions for trip.
            deleted_companions = TripCompanion.objects.filter(trip_id=trip_id).delete()
            logger.info(f'Removed all ({deleted_companions}) companions from trip {trip_id}')

            # 4. Insert new list of companions (if any new item).
            companion_qset = User.objects.filter(user_id__in=req_data['companions'])
            TripCompanion.objects.bulk_create(
                [TripCompanion(trip_id=trip, user_id=c) for c in companion_qset]
            )
            len(companion_qset) and logger.info(f"Saved companions {req_data['companions']} to trip {trip.trip_id}")

        return JsonResponse({'success': req_data, 'error': {}})


class DestinationAPI(APIView):

    def get(self, _, trip_id):
        trip = Trip.get_by_id(trip_id)
        destinations = TripCity.objects.filter(trip=trip).order_by('dest_city_order')

        trip_details = model_to_dict(trip)
        dest_list = [model_to_dict(d) for d in destinations]
        trip_details.update({'destinations': dest_list})

        return JsonResponse({'success': trip_details, 'error': {}})

    def post(self, request, trip_id):
        # Load JSON body and validate
        req_data = get_payload(request.body)
        body = TripCityPostSerializer(trip_id, data=req_data)
        if not body.is_valid():
            return JsonResponse({'error': body.errors}, status=400)
        req_data = body.data

        trip_city = TripCity(
            city=City.objects.get(city_id=req_data['cityId']),
            trip=Trip.objects.get(trip_id=trip_id),
            dest_city_order=req_data['destinationOrder']
        )
        trip_city.save()
        logger.info(f'Added trip destination {req_data["cityId"]} to trip {trip_id}')

        return JsonResponse({'success': req_data, 'error': {}})
