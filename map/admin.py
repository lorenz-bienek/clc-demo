from django.contrib.gis import admin

from map.models import PLZ

admin.site.register(PLZ, admin.OSMGeoAdmin)
