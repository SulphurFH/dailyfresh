from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart),
    url(r'^addcart(\d+)&(\d+)/$', views.addcart),
    url(r'^edit(\d+)&(\d+)/$', views.edit),
    url(r'^del(\d+)/$', views.delcart),
]
