from django.conf.urls import url, include
from api import views


urlpatterns = [
    url(r'^api/$', views.AllRecordsList.as_view()),
    url('^api/search/$', views.Search.as_view()),
    # UUID router
    url(r'^api/(?P<pk>[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[1345][a-fA-F0-9]{3}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12})/$',
        views.RecordDetail.as_view()),
    url(r'^api/admin/$', views.InternalRecordsList.as_view()),
    url(r'^api/admin/create/$', views.CreateRecord.as_view()),
    url(r'^api/admin/(?P<pk>[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[1345][a-fA-F0-9]{3}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12})/$',
        views.CreateAndEditRecord.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
