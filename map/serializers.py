import json

from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework_gis import serializers

from map.models import PLZ


class PLZSerializer(serializers.GeoFeatureModelSerializer):
    """
    Serializer for PLZen that returns all fields.
    """

    class Meta:
        model = PLZ
        fields = '__all__'
        geo_field = 'geom'


class GeoJSONEncoder(DjangoJSONEncoder):
    """
    Extend the DjangoJSONEncoder for GEOSGeometry.
    """

    def default(self, o):
        if isinstance(o, GEOSGeometry):
            # Use the geojson method of GEOS to create a valid geoJSON.
            # Then use json to create a python dict, that can be easily serialized.
            # This is an inefficient but simple way to have a valid object in the final JSON.
            return json.loads(o.geojson)
        else:
            return super().default(o)
