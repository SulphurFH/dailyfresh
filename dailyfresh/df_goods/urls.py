from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^good(\d+)/$', views.detail),
    url(r'^goodlist/(\d+)&(\d+)&(\d+)/$', views.goodlist),
]
