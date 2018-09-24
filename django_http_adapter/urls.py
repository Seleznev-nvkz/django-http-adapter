from django import VERSION

from django_http_adapter.views import HTTPAdapterView

if VERSION >= (2, 0):
    from django.urls import path
else:
    from django.conf.urls import url as path

urlpatterns = [
    path('', HTTPAdapterView.as_view(), name='main')
]
