from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'metadata', views.MetaDataReadOnlyViewSet, base_name='metadata')
router.register(r'admin', views.RecordsAdminViewSet, base_name='admin')
router.register(r'search', views.CombinedRecordsSearchView, base_name="metadata-search")
urlpatterns = router.urls

urlpatterns += [
    url(r'^docs/$', views.schema_view),
]
