import logging
from pprint import pformat

from django_http_adapter.settings import HTTP_ADAPTER_LOGGER

logger = logging.getLogger(HTTP_ADAPTER_LOGGER)


class HTTPClientException(Exception):
    def __init__(self, message: str, data):
        self.message = message
        self.data = pformat(data, indent=4)
        logger.error(repr(self))

    def __str__(self) -> str:
        return self.data

    def __repr__(self) -> str:
        return '{}\n\n{}'.format(self.message, self.data)
