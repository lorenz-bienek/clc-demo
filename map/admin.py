from django.contrib.gis import admin

from map.models import CLC, PLZ

admin.site.register(PLZ, admin.OSMGeoAdmin)
admin.site.register(CLC, admin.OSMGeoAdmin)
