from collections import OrderedDict

from requests.adapters import HTTPAdapter as BaseAdapter
from requests.sessions import Session

from django_http_adapter import settings

""" https://stackoverflow.com/questions/34837026/whats-the-meaning-of-pool-connections-in-requests-adapters-httpadapter 
"""


class HTTPAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(pool_connections=settings.HTTP_ADAPTER_POOL_SIZE,
                         pool_maxsize=settings.HTTP_ADAPTER_POOL_COUNT,
                         max_retries=settings.HTTP_ADAPTER_CONNECT_RETRIES,
                         pool_block=settings.HTTP_ADAPTER_POOL_BLOCK)


class HTTPSession(Session):
    def __init__(self, *urls):
        super().__init__()
        self.headers['http-adapter-app'] = str(settings.HTTP_ADAPTER_APP_ID)

        self.adapters = OrderedDict()
        for server_url in urls:
            self.mount(server_url, HTTPAdapter())
