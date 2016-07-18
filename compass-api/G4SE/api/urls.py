from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/$', views.AllRecordsList.as_view()),
    url('^api/search/$', views.Search.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.RecordDetail.as_view()),
    url(r'^api/edit/$', views.InternalRecordsList.as_view()),
    url(r'^api/edit/(?P<pk>[0-9]+)/$', views.EditRecord.as_view()),
]
