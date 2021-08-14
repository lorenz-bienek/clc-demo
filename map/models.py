from django.contrib.gis.db import models


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


clc18_de_mapping = {
    'object_id': 'OBJECTID',
    'code_18': 'CODE_18',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'alternative_id': 'ID',
    'area_ha': 'Area_Ha',
    'geom': 'MULTIPOLYGON',
}
