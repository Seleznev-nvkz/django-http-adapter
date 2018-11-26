from django.core.management import BaseCommand

from django_http_adapter.models import HTTPRetry, HTTPRetryData


class Command(BaseCommand):
    help = "Try to resend all failed requests"

    def handle(self, *args, **options):
        retry_query = HTTPRetry.objects.all()
        retry_data_query = HTTPRetryData.objects.all()
        print("Resending {} retry_query and {} retry_data_query".format(retry_query.count(), retry_data_query.count()))

        for item in retry_query.iterator():
            item.retry()

        for item in retry_data_query.iterator():
            item.retry()

        print("Done")
