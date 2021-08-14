from django.urls import include, path
from rest_framework import routers

from map.views import MapView, PLZViewSet

app_name = 'map'

router = routers.DefaultRouter()
router.register(r'plz', PLZViewSet)

urlpatterns = [
    path('', MapView.as_view()),
    path('api/', include(router.urls)),
]
