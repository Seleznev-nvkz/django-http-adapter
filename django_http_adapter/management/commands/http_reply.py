from django.core.management import BaseCommand

from django_http_adapter.models import HTTPRetry


class Command(BaseCommand):
    help = "Try to resend all failed requests"

    def handle(self, *args, **options):
        count = 0

        for item in HTTPRetry.objects.all():
            item.retry()
            count += 1

        print("{} items resent".format(count))
