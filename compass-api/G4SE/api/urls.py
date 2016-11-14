from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'metadata', views.MetaDataReadOnlyViewSet, base_name='metadata')
router.register(r'admin', views.GeoServiceMetadataAdminViewSet, base_name='admin')
router.register(r'search', views.GeoServiceMetadataSearchView, base_name="metadata-search")

urlpatterns = router.urls

urlpatterns += [
    url(r'^docs/$', views.schema_view),
]
