from django.contrib.gis.utils import LayerMapping
from django.core.management.base import BaseCommand

from map.models import PLZ, plz_mapping


class Command(BaseCommand):
    """
    Imports a shape file for PLZ.

    The files this works with are available at
    https://www.suche-postleitzahl.org/plz-karte-erstellen
    """

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str, help="The path to the PLZ shape file.")

    def handle(self, *args, **options):
        path = options['path'][0]
        lm = LayerMapping(
            model=PLZ,
            data=path,
            mapping=plz_mapping,
            transform=False,
        )
        lm.save(strict=True, verbose=True)
