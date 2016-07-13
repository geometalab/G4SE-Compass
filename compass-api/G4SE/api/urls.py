from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/$', views.RecordList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.RecordDetail.as_view()),
]
