# Django-HTTP-Adapter

## In a nutshell
Simple third-party application for communicating back-end systems on Django using HTTP. 

## How to use
Firstly add HTTPMixin to the Model, whose instances want to send:
```
class OriginTag(HTTPMixin, models.Model):
	...
```

Then add property `http_receiver` to the Model with the full path of the handler on another server:
```
class OriginTag(HTTPMixin, models.Model):
	...
	http_receiver = 'tags.models.OtherTag:receive'
```
And now data will send to other servers on save Model. 

## Getting going
### Requirements
- Django 1.11+
- python 3.5+
- requests 2.19+
### Installation
``` pip install git+ ```

Should update `INSTALLED_APPS`

``` 
INSTALLED_APPS = (
    # ...
    'django_http_adapter',
    # ...
)
```
and `urls.py`:
``` urlpatterns += (url(r'^your_receive_url/', include('django_http_adapter.urls')),) ```
To store in DB failed sendings:
``` python manage.py migrate ```
### Required settings

Name|Description|Example
------------ | ------------- | ------
HTTP_ADAPTER_SERVERS|Dictionary with servers to send, where key is Id of server and value is url |{2: "https://example.com/your_receive_url/"}
HTTP_ADAPTER_APP_ID|Id of current server|1

### Optional settings
Name|Description|Default
------------ | ------------- | ------
HTTP_ADAPTER_SEND_TRIES|Count of try to send.|3
HTTP_ADAPTER_SLEEP_TIME|Time of sleeping between failed tries.|0.5
HTTP_ADAPTER_USE_THREAD|Allow to send in separate thread|True
HTTP_ADAPTER_MAX_THREADS|How many threads can be running in one time|3
HTTP_ADAPTER_CONNECT_RETRIES|The maximum number of retries each connection should attempt.|5
HTTP_ADAPTER_POOL_BLOCK|Whether the connection pool should block for connections.|False
HTTP_ADAPTER_POOL_COUNT|Size of pool. Helpful for using threads. Should be equal or more than HTTP_ADAPTER_MAX_THREADS.|10
HTTP_ADAPTER_POOL_SIZE|The number of urllib3 connection pools to cache. Should be equal or more than urls for app you have.| 2
HTTP_ADAPTER_LOGGER|Name of logger for using in package|'django.request'

## Extra info
### Django Management Commands
To retry failed sendings run:
> python manage.py http_retry

### Other features
- Can using `ujson` instead common `json`. Just install `ujson` and this will be auto change.
- Exists simple admin form with custom action `Try to resend items` to retry selected instances.

## ToDo
- add ability to add symmetric-key algorithm
- add tests
- add example