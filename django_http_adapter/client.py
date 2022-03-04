import json
from pprint import pprint
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
                    return response.json()
                else:
                    # if something wrong in data
                    bad_responses.append({'status': response.status_code, 'content': response.json()})
            except Exception as e:
                # if something wrong with server or response
                bad_responses.append({'error': str(e)})
            sleep(settings.HTTP_ADAPTER_SLEEP_TIME)
        raise HTTPClientException(message='Unsuccessful Send {} tries'.format(self.tries), data=bad_responses)

    def send(self, input_data, thread=True):
        """ Send data, If sending will fail - will create HTTPRetryData for resending in future
        """

        def threading_request(data):
            with semaphore:
                make_request(data)

        def make_request(data):
            try:
                return self._send(data)
            except HTTPClientException as e:
                self.retry_model.create_from_exc(data, self.app_id, e)

        if settings.HTTP_ADAPTER_USE_THREAD and thread:
            Thread(target=threading_request, args=(input_data,)).start()
        else:
            return make_request(input_data)


class HTTPDataClient(BaseHTTPClient):
    retry_model = HTTPRetryData


class HTTPInstanceClient(BaseHTTPClient):
    retry_model = HTTPRetry

    def _send(self, instance):
        return super()._send(instance.get_http_data())

class HTTPDevClient(BaseHTTPClient):

    def send(self, data, thread=True):
        if isinstance(data, Model):
            data = data.get_http_data()
        print('-' * 100)
        print('URL: ', self.url)
        print('App ID: ', self.app_id)
        print('Payload:')
        pprint(data)
        print('-' * 100)


class HTTPClient:
    def __init__(self, app_id: int):
        self.data_client = HTTPDataClient(app_id)
        self.instance_client = HTTPInstanceClient(app_id)
        self.dev_client = HTTPDevClient(app_id)

    def send(self, data, thread=True):
        if settings.HTTP_ADAPTER_MODE == 'dev':
            client = self.dev_client
        elif isinstance(data, Model):
            client = self.instance_client
        else:
            client = self.data_client
        return client.send(data, thread)


semaphore = BoundedSemaphore(settings.HTTP_ADAPTER_MAX_THREADS)
http_adapter_clients = {app_id: HTTPClient(app_id) for app_id in settings.HTTP_ADAPTER_SERVERS}
