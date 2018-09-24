from django.conf import settings

HTTP_ADAPTER_SEND_TRIES = getattr(settings, 'HTTP_ADAPTER_SEND_TRIES', 3)
HTTP_ADAPTER_SLEEP_TIME = getattr(settings, 'HTTP_ADAPTER_SLEEP_TIME', 0.5)
HTTP_ADAPTER_USE_THREAD = getattr(settings, 'HTTP_ADAPTER_USE_THREAD', True)
HTTP_ADAPTER_MAX_THREADS = getattr(settings, 'HTTP_ADAPTER_MAX_THREADS', 3)

HTTP_ADAPTER_CONNECT_RETRIES = getattr(settings, 'HTTP_ADAPTER_CONNECT_RETRIES', 5)
HTTP_ADAPTER_POOL_BLOCK = getattr(settings, 'HTTP_ADAPTER_POOL_BLOCK', False)
HTTP_ADAPTER_POOL_COUNT = getattr(settings, 'HTTP_ADAPTER_POOL_COUNT', 10)
HTTP_ADAPTER_POOL_SIZE = getattr(settings, 'HTTP_ADAPTER_POOL_SIZE', 2)
HTTP_ADAPTER_LOGGER = getattr(settings, 'HTTP_ADAPTER_LOGGER', 'django.request')

HTTP_ADAPTER_SERVERS = getattr(settings, 'HTTP_ADAPTER_SERVERS')
assert HTTP_ADAPTER_SERVERS, 'set HTTP_ADAPTER_SERVERS in settings'
assert isinstance(HTTP_ADAPTER_SERVERS, dict), 'HTTP_ADAPTER_SERVERS should be dict'

HTTP_ADAPTER_APP_ID = getattr(settings, 'HTTP_ADAPTER_APP_ID')
assert HTTP_ADAPTER_APP_ID is not None, 'set HTTP_ADAPTER_APP_ID in settings'
assert isinstance(HTTP_ADAPTER_APP_ID, int), 'HTTP_ADAPTER_APP_ID should be int'
