from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from rest_framework import viewsets

from map.models import PLZ
from map.serializers import PLZSerializer


class MapView(TemplateView):

    template_name = 'map.html'


class PLZViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API view that returns the data for all PLZen.
    """

    queryset = PLZ.objects.all()
    serializer_class = PLZSerializer

    # Cache response for 7 days because the PLZen will not change.
    @method_decorator(cache_page(60 * 60 * 24 * 7))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
