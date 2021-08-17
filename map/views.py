from django.http import JsonResponse
from django.views.generic.base import TemplateView
from rest_framework import viewsets

from map.models import CLC, PLZ
from map.serializers import GeoJSONEncoder, PLZSerializer


class MapView(TemplateView):

    template_name = 'map.html'


class PLZViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API view that returns the data for all PLZen.
    """

    queryset = PLZ.objects.all()
    serializer_class = PLZSerializer

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


def clc_for_plz(request, **kwargs):
    """
    Returns the area and geojson for the high level land cover of a PLZ.
    """
    plz = PLZ.objects.get(plz=kwargs['plz'])
    aggregates = CLC.group_intersections(plz.geom)
    aggregates_area_square_kilometers = {
        key: value.area / 1_000_000 if value else 0 for key, value in aggregates.items()
    }
    aggregates_geojson = {
        key: value.geojson if value else None for key, value in aggregates.items()
    }
    response = {
        'name': plz.name,
        'plz_area_square_kilometers': plz.calculated_area_square_kilometers,
        'aggregates_area_square_kilometers': aggregates_area_square_kilometers,
        'aggregates': aggregates,
    }
    return JsonResponse(response, encoder=GeoJSONEncoder)
