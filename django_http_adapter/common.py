from collections import OrderedDict

from requests.adapters import HTTPAdapter as BaseAdapter
from requests.sessions import Session

from django_http_adapter import settings

""" https://stackoverflow.com/questions/34837026/whats-the-meaning-of-pool-connections-in-requests-adapters-httpadapter 
"""


class HTTPAdapter(BaseAdapter):
    def __init__(self):
        """
        HTTP_ADAPTER_POOL_SIZE – The number of urllib3 connection pools to cache.
                                 Should be equal or more than urls for app you have
        HTTP_ADAPTER_POOL_COUNT - Size of pool. Helpful for using threads.
                                  Should be equal or more than HTTP_ADAPTER_MAX_THREADS.
        HTTP_ADAPTER_CONNECT_RETRIES - The maximum number of retries each connection should attempt.
        HTTP_ADAPTER_POOL_BLOCK - Whether the connection pool should block for connections.
        """
        super().__init__(pool_connections=settings.HTTP_ADAPTER_POOL_SIZE,
                         pool_maxsize=settings.HTTP_ADAPTER_POOL_COUNT,
                         max_retries=settings.HTTP_ADAPTER_CONNECT_RETRIES,
                         pool_block=settings.HTTP_ADAPTER_POOL_BLOCK)


class HTTPSession(Session):
    """ Using pool of connection for specific urls
        HTTP_ADAPTER_APP_ID - id of current app """

    def __init__(self, *urls):
        super().__init__()
        self.headers['http-adapter-app'] = str(settings.HTTP_ADAPTER_APP_ID)

        self.adapters = OrderedDict()
        for server_url in urls:
            self.mount(server_url, HTTPAdapter())
