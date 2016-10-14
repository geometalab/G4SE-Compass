from django.core.management.base import BaseCommand

from api.management.commands._private import harvest


class Command(BaseCommand):
    help = 'Updates all GeoVITe imports (HarvestedRecords)'

    def handle(self, *args, **options):
        harvest()
