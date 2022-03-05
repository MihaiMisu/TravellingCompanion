from json import loads

from django.http import JsonResponse
from django.views import View

from .logger import logger


class APIView(View):

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as ex:
            logger.exception(ex)
            return JsonResponse({'error': {'message': 'Internal server error'}, 'Success': ''}, status=500)


def get_payload(req_body) -> dict:
    return loads(req_body)
