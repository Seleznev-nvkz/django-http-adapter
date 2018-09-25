from django.forms.models import model_to_dict

from django_http_adapter.client import http_adapter_clients
from django_http_adapter.settings import HTTP_ADAPTER_SERVERS


class HTTPMixin:
    """ Mixin for using with django models
         - http_receiver - to set handler for other servers """

    http_receiver = None

    @property
    def http_from(self):
        """ id of server where was created obj """
        return getattr(self, '_http_from', None)

    def get_http_data(self) -> dict:
        """ data of instance to send """
        return {**model_to_dict(self), **{'receiver': self.http_receiver}}

    def http_send(self):
        """ send data to all apps for sending, excluding id of app whence was received """
        for server_id in self.get_http_apps() - {self.http_from}:
            http_adapter_clients[server_id].send_instance(self)

    def get_http_apps(self) -> set:
        """ :return set of all apps for sending """
        return set(HTTP_ADAPTER_SERVERS.keys())

    def save(self, *args, **kwargs):
        super(HTTPMixin, self).save(*args, **kwargs)
        self.http_send()
