import json
from threading import Thread, BoundedSemaphore
from time import sleep

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model

from django_http_adapter import settings
from django_http_adapter.common import HTTPSession
from django_http_adapter.exceptions import HTTPClientException
from django_http_adapter.models import HTTPRetry, HTTPRetryData


class BaseHTTPClient:
    """ Client to send data for different applications(urls) | using as singleton """

    retry_model = None

    def __init__(self, app_id: int):
        """
        :param app_id: id of app for which will send
        """
        self._session = None
        self.app_id = app_id
        self.tries = settings.HTTP_ADAPTER_SEND_TRIES
        self.url = settings.HTTP_ADAPTER_SERVERS[app_id]

    @property
    def session(self) -> HTTPSession:
        if self._session is None:
            self._session = HTTPSession(self.url)
        return self._session

    def _send(self, data: dict):
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

    def send(self, input_data):
        """ Send data, If sending will fail - will create HTTPRetryData for resending in future
        """

        def threading_request(data):
            with semaphore:
                make_request(data)

        def make_request(data):
            try:
                self._send(data)
            except HTTPClientException as e:
                self.retry_model.create_from_exc(data, self.app_id, e)

        if settings.HTTP_ADAPTER_USE_THREAD:
            Thread(target=threading_request, args=(input_data,)).start()
        else:
            make_request(input_data)


class HTTPDataClient(BaseHTTPClient):
    retry_model = HTTPRetryData


class HTTPInstanceClient(BaseHTTPClient):
    retry_model = HTTPRetry

    def _send(self, instance):
        super()._send(instance.get_http_data())


class HTTPClient:
    def __init__(self, app_id: int):
        self.data_client = HTTPDataClient(app_id)
        self.instance_client = HTTPInstanceClient(app_id)

    def send(self, data):
        if isinstance(data, Model):
            self.instance_client.send(data)
        else:
            self.data_client.send(data)


semaphore = BoundedSemaphore(settings.HTTP_ADAPTER_MAX_THREADS)
http_adapter_clients = {app_id: HTTPClient(app_id) for app_id in settings.HTTP_ADAPTER_SERVERS}
