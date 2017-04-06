# coding=utf-8
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^user_exist/$', views.user_exist),
    url(r'^email_exist/$', views.email_exist),
    url(r'^user_handle/$', views.user_handle),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^login_handle/$', views.login_handle),
    url(r'^user_center_info/$', views.user_center_info),
    url(r'^user_center_site/$', views.user_center_site),
    url(r'^user_center_order/$', views.user_center_order),
]
