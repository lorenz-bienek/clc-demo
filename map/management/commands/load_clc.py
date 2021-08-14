from pathlib import Path

from django.contrib.gis.utils import LayerMapping
from django.core.management.base import BaseCommand

from map.models import CLC, clc18_de_mapping


class Command(BaseCommand):
    """
    Imports a shape file with the CORINE Land Cover data.

    CLC_data_source_description.pdf in the root of this repository
    describes the source of the data used.
    In order to make it work it has been preprocessed with the help of QGIS.
    The field code_18 has been converted from string to integer.
    The z and m values have been dropped.
    The resulting layer was then exported as a shape file.
    """

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str, help="The path to the CLC2018 shape file.")

    def handle(self, *args, **options):
        path = Path(options['path'][0])
        lm = LayerMapping(
            model=CLC,
            data=path,
            mapping=clc18_de_mapping,
            transform=False,
        )
        lm.save(strict=True, verbose=True)
