from threading import Thread, BoundedSemaphore
from time import sleep

from django.core.serializers.json import DjangoJSONEncoder

from django_http_adapter import settings
from django_http_adapter.common import HTTPSession
from django_http_adapter.exceptions import HTTPClientException
from django_http_adapter.models import HTTPRetry

try:
    import ujson as json
except ImportError:
    import json


class HTTPClient:
    """ Client to send data for different applications(urls) | using as singleton """

    def __init__(self, app_id: int, tries: int = settings.HTTP_ADAPTER_SEND_TRIES):
        """
        :param app_id: id of app for which will send
        :param tries: count of try to send
        """
        self._session = None
        self.app_id = app_id
        self.tries = tries
        self.url = settings.HTTP_ADAPTER_SERVERS[app_id]

    @property
    def session(self) -> HTTPSession:
        if self._session is None:
            self._session = HTTPSession(self.url)
        return self._session

    def send_data(self, data: dict):
        """ Send data to self.url using self.tries times """
        bad_responses = []
        post_data = json.dumps(data, cls=DjangoJSONEncoder)

        for _ in range(self.tries):
            try:
                response = self.session.post(self.url, data=post_data, headers={'Content-Type': 'application/json'})
                if response.ok:
                    return
                else:
                    # if something wrong in data
                    bad_responses.append({'status': response.status_code, 'content': response.json()})
            except Exception as e:
                # if something wrong with server or response
                bad_responses.append({'error': str(e)})
            sleep(settings.HTTP_ADAPTER_SLEEP_TIME)
        raise HTTPClientException(message='Unsuccessful Send {} tries'.format(self.tries), data=bad_responses)

    def send_instance(self, instance):
        """ Send instance' data, Should be mixin with HTTPMixin
            If sending will fail - will create HTTPRetry for resending in future
        """

        def threading_request(instance_data: dict):
            with semaphore:
                make_request(instance_data)

        def make_request(instance_data: dict):
            try:
                self.send_data(instance_data)
            except HTTPClientException as e:
                HTTPRetry.create_from_exc(instance, self.app_id, e)

        if settings.HTTP_ADAPTER_USE_THREAD:
            Thread(target=threading_request, args=(instance.get_http_data(),)).start()
        else:
            make_request(instance.get_http_data())


semaphore = BoundedSemaphore(settings.HTTP_ADAPTER_MAX_THREADS)
http_adapter_clients = {app_id: HTTPClient(app_id) for app_id in settings.HTTP_ADAPTER_SERVERS}
