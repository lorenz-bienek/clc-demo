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
