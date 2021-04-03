from django.conf.urls import url
import cmms.views



urlpatterns = [
    url(r'^$',cmms.views.dashboard,name='dashboard'),
    url(r'^maintenance/$',views.list_wo,name='list_wo'),
    url(r'^WorkOrder/$',views.list_wo,name='list_wo'),
    url(r'^Workorder/create/$', views.wo_create, name='wo_create'),
    url(r'^Workorder/(?P<id>\d+)/create/$', views.wo_create, name='wo_create'),
    url(r'^Workorder/(?P<id>\d+)/update/$', views.wo_update, name='wo_update'),
    url(r'^Workorder/(?P<id>\d+)/delete/$', views.wo_delete, name='wo_delete'),


]
