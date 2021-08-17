from django.contrib.gis.db import models
from django.contrib.gis.db.models import Union
from django.contrib.gis.db.models.functions import Intersection
from django.db.models import F


class PLZ(models.Model):
    plz = models.CharField(max_length=5)
    name = models.CharField(max_length=86, blank=True, null=True)
    population = models.IntegerField()
    qkm = models.FloatField()
    geom = models.MultiPolygonField()

    class Meta:
        verbose_name = "PLZ"
        verbose_name_plural = "PLZen"

    def __str__(self):
        return self.name or ""

    @property
    def calculated_area_square_kilometers(self):
        return self.geom.transform(25832, clone=True).area / 1_000_000


plz_mapping = {
    'population': 'einwohner',
    'name': 'note',
    'plz': 'plz',
    'qkm': 'qkm',
    'geom': 'MULTIPOLYGON',
}


class CLC(models.Model):
    """
    The CORINE Land Cover data.
    """
    object_id = models.IntegerField()
    alternative_id = models.CharField(max_length=12)
    code_18 = models.IntegerField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    area_ha = models.FloatField()
    geom = models.MultiPolygonField(srid=25832)

    def __str__(self):
        return f"{ self.alternative_id }: { self.code_18 }"

    @classmethod
    def calculate_intersections(cls, geom):
        """
        Returns all CLCs that share any space with the given geom and adds intersecting_geom.

        intersecting_geom is the area that falls inside of the given geom.
        """
        return cls.objects.filter(
            geom__intersects=geom).annotate(
            intersection_geom=Intersection(F('geom'), geom)
        )

    @classmethod
    def group_intersections(cls, geom):
        """
        Returns the high level aggregates of the land use in the given geom.
        """
        def aggregate_intersection(queryset):
            return queryset.aggregate(Union('intersection_geom'))['intersection_geom__union']

        intersections = cls.calculate_intersections(geom)

        return {
            'aggregate_1': aggregate_intersection(intersections.filter(code_18__gte=100, code_18__lt=200)),
            'aggregate_2': aggregate_intersection(intersections.filter(code_18__gte=200, code_18__lt=300)),
            'aggregate_3': aggregate_intersection(intersections.filter(code_18__gte=300, code_18__lt=400)),
            'aggregate_4': aggregate_intersection(intersections.filter(code_18__gte=400, code_18__lt=500)),
            'aggregate_5': aggregate_intersection(intersections.filter(code_18__gte=500, code_18__lt=600)),
        }


clc18_de_mapping = {
    'object_id': 'OBJECTID',
    'code_18': 'CODE_18',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'alternative_id': 'ID',
    'area_ha': 'Area_Ha',
    'geom': 'MULTIPOLYGON',
}
