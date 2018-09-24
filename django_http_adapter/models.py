from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from http_adapter.exceptions import HTTPClientException


class HTTPRetry(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    exception_info = models.TextField()
    app_id = models.IntegerField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name_plural = 'HttpRetry'
        unique_together = ('content_type', 'object_id', 'app_id')
        ordering = ('-created_timestamp',)

    @classmethod
    def create_from_exc(cls, instance, app_id, exc):
        content_type = ContentType.objects.get_for_model(instance)
        cls.objects.update_or_create(content_type=content_type, object_id=instance.id, app_id=app_id,
                                     defaults={'exception_info': str(exc)})

    def retry(self):
        from http_adapter.client import http_adapter_clients

        if self.content_object:
            try:
                http_adapter_clients[self.app_id].send_data(self.content_object.get_http_data())
            except HTTPClientException as e:
                self.exception_info = str(e)
                self.save()
                return
        self.delete()
