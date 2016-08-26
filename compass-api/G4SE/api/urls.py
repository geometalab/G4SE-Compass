from django.conf.urls import url, include
from api import views


urlpatterns = [
    # API views
    url(r'^api/metadata/$', views.AllRecordsList.as_view()),
    url(r'^api/metadata/(?P<pk>[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[1345][a-fA-F0-9]{3}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12})/$',
        views.RecordDetail.as_view()),
    url('^api/search/$', views.Search.as_view()),
    url('^api/recent/$', views.MostRecentRecords.as_view()),

    # API admin views
    url(r'^api/admin/$', views.InternalRecordsList.as_view()),
    url(r'^api/admin/create/$', views.CreateRecord.as_view()),
    url(r'^api/admin/(?P<pk>[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[1345][a-fA-F0-9]{3}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12})/$',
        views.CreateAndEditRecord.as_view()),

    # User management
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
