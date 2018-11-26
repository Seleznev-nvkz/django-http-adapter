from django.contrib import admin

from django_http_adapter.models import HTTPRetry, HTTPRetryData


def retry_to_send(modeladmin, request, queryset):
    for bad_try in queryset:
        bad_try.retry()


retry_to_send.short_description = "Try to resend items"


class HTTPRetryAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'app_id', 'created_timestamp')
    related_lookup_fields = {'generic': [['content_type', 'content_id']]}
    actions = (retry_to_send,)


class HTTPRetryDataAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'created_timestamp')
    actions = (retry_to_send,)


admin.site.register(HTTPRetryData, HTTPRetryDataAdmin)
admin.site.register(HTTPRetry, HTTPRetryAdmin)
