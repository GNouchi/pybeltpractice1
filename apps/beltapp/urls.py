from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^wall$', views.wall),
    url(r'^addtrip$', views.addtrip),
    url(r'^create$', views.create),
    url(r'^destroy/(?P<id>\d)$', views.destroy),
    url(r'^show/(?P<id>\d)$', views.show),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^cancel/(?P<id>\d)$', views.cancel),
    url(r'^join/(?P<id>\d)$', views.join),
    url(r'^$', views.index),
]