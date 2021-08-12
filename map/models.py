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
