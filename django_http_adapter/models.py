import json

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from django_http_adapter.exceptions import HTTPClientException


class AbsHTTPRetry(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    exception_info = models.TextField()
    app_id = models.IntegerField()

    class Meta:
        abstract = True
        ordering = ('-created_timestamp',)

    def __str__(self):
        return '{} - {}'.format(self.app_id, self.created_timestamp)

    def _retry_data(self, data):
        from django_http_adapter.client import http_adapter_clients

        try:
            http_adapter_clients[self.app_id].send(data)
        except HTTPClientException as e:
            self.exception_info = str(e)
            self.save()
            return
        self.delete()


class HTTPRetry(AbsHTTPRetry):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name_plural = 'Retry'
        unique_together = ('content_type', 'object_id', 'app_id')

    @classmethod
    def create_from_exc(cls, instance, app_id, exc):
        content_type = ContentType.objects.get_for_model(instance)
        cls.objects.update_or_create(content_type=content_type, object_id=instance.id, app_id=app_id,
                                     defaults={'exception_info': str(exc)})

    def retry(self):
        if self.content_object:
            self._retry_data(self.content_object)


class HTTPRetryData(AbsHTTPRetry):
    data = models.TextField()

    class Meta:
        verbose_name_plural = 'Retry Data'
        unique_together = ('data', 'app_id')

    @classmethod
    def create_from_exc(cls, data, app_id, exc):
        post_data = json.dumps(data, cls=DjangoJSONEncoder)
        cls.objects.update_or_create(data=post_data, app_id=app_id, defaults={'exception_info': str(exc)})

    def retry(self):
        self._retry_data(json.loads(self.data))
