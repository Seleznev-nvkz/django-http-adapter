from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings
from django.urls import reverse, NoReverseMatch

from django_http_adapter.models import HTTPRetry, HTTPRetryData


def retry_to_send(modeladmin, request, queryset):
    for bad_try in queryset:
        bad_try.retry()


retry_to_send.short_description = "Try to resend items"


class AbsHTTPRetryAdmin(admin.ModelAdmin):
    readonly_fields = ('app_receiver',)

    @staticmethod
    def app_receiver(instance):
        return mark_safe(settings.HTTP_ADAPTER_SERVERS.get(instance.app_id))

    app_receiver.short_description = 'Receiver URL'


class HTTPRetryAdmin(AbsHTTPRetryAdmin):
    list_display = ('id', 'content_type', 'object_id', 'instance_link', 'app_receiver', 'created_timestamp')
    related_lookup_fields = {'generic': [['content_type', 'content_id']]}
    actions = (retry_to_send,)
    fieldsets = (
        (None, {
            'fields': ('exception_info', ('app_id', 'app_receiver'), 'content_type', 'object_id')
        }),
    )

    def instance_link(self, instance):
        content = instance.content_object
        try:
            change_url = reverse(
                'admin:{0}_{1}_change'.format(content._meta.app_label, content._meta.model_name),
                args=(content.pk,)
            )
        except (NoReverseMatch, AttributeError):
            return None
        return mark_safe('<a href="{0}">{1} ({2})</a>'.format(change_url, content._meta.model_name, content.pk))


class HTTPRetryDataAdmin(AbsHTTPRetryAdmin):
    list_display = ('id', 'app_receiver', 'created_timestamp')
    actions = (retry_to_send,)
    fieldsets = (
        (None, {
            'fields': ('exception_info', ('app_id', 'app_receiver'), 'data')
        }),
    )


admin.site.register(HTTPRetryData, HTTPRetryDataAdmin)
admin.site.register(HTTPRetry, HTTPRetryAdmin)
