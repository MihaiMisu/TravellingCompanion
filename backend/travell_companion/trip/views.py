from django.http import JsonResponse

from .models import Trip, User, TripCompanion
from .validators import TripPostSerializer
from backend.travell_companion.utils import APIView, get_payload, logger


class TripAPI(APIView):

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



