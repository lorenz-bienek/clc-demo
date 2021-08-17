from django.urls import include, path
from rest_framework import routers

from map.views import MapView, PLZViewSet, clc_for_plz

app_name = 'map'

router = routers.DefaultRouter()
router.register(r'plz', PLZViewSet)

urlpatterns = [
    path('', MapView.as_view()),
    path('api/', include(router.urls)),
    path('api/plz/<plz>/clc/', clc_for_plz),
]
