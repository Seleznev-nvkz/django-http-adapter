from django.http import JsonResponse
from django.views.generic import View

from django_http_adapter.utils import get_module_attr

try:
    import ujson as json
except ImportError:
    import json


class HTTPAdapterView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """ Should contain the header with id of the server, which sent the request.
            Also 'receiver' in data from the request to launch handler """
        body = request.body.decode('utf-8')

        try:
            data = json.loads(body)
            handler = get_module_attr(data.pop('receiver'))
            app_id = int(request.META['HTTP_HTTP_ADAPTER_APP'])
            return JsonResponse({'result': handler(http_from=app_id, **data)})
        except Exception as e:
            return JsonResponse({'error': str(e), 'data': body}, status=400)
