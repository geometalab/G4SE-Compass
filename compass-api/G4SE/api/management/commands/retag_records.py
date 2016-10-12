from django.core.management.base import BaseCommand

from api.signals import retag_all


class Command(BaseCommand):
    help = 'Applies tags to all the Geo Service Metadata'

    def handle(self, *args, **options):
        retag_all()
