from django.conf.urls import url
from . import views


urlpatterns = [
    # API views
    url(r'^metadata/$', views.AllRecordsList.as_view()),
    url(r'^metadata/(?P<pk>[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[1345][a-fA-F0-9]{3}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12})/$',
        views.RecordDetail.as_view()),
    url('^metadata/search/$', views.Search.as_view()),
    url('^metadata/recent/$', views.MostRecentRecords.as_view()),

    # API admin views
    url(r'^admin/$', views.InternalRecordsList.as_view()),
    url(r'^admin/create/$', views.CreateRecord.as_view()),
    url(r'^admin/(?P<pk>[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[1345][a-fA-F0-9]{3}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12})/$',
        views.CreateAndEditRecord.as_view()),
]
