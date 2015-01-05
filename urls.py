from django.conf.urls import patterns, url,include
#from django.conf.urls.static import static
from hiseqlibraries import views
from rest_framework.routers import DefaultRouter

#from hiseqlibraries.views import SummaryViewSet
from rest_framework import renderers


urlpatterns = patterns('',
 #   url(r'^', include(router.urls)),
    url(r'^libraries/$', 'hiseqlibraries.views.libraries'),
    url(r'^qc/$', 'hiseqlibraries.views.qc'),
    url(r'^usergrid/$', 'hiseqlibraries.views.usergrid'),
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),	

    url(r'^summarylist/$',views.SummaryList.as_view() ),
    url(r'^summarydetail/(?P<pk>[0-9]+)/$',views.SummaryDetail.as_view() ),
    url(r'^fileslist/$',views.FilesList.as_view() ),
    url(r'^filesdetail/(?P<pk>[0-9]+)/$',views.FilesDetail.as_view() ),
    url(r'^seqstatslist/$',views.SeqStatsList.as_view() ),
    url(r'^seqstatsdetail/(?P<pk>[0-9]+)/$',views.SeqStatsDetail.as_view() ),
    url(r'^alignstatslist/$',views.AlignStatsList.as_view() ),
    url(r'^alignstatsdetail/(?P<pk>[0-9]+)/$',views.AlignStatsDetail.as_view() ),
)

