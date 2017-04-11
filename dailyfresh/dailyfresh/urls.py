"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from df_goods import search_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
<<<<<<< HEAD
    url(r'^/', include('book.urls')),
    url(r'^hero/', include('hero.urls')),
    url(r'^fixbug')
xfeibu]
aaaa
=======
<<<<<<< HEAD
    url(r'^user/', include('df_user.urls', namespace='user')),
    url(r'^cart/', include('df_cart.urls', namespace='cart')),
    url(r'^', include('df_goods.urls', namespace='goods')),
    url(r'^order/', include('df_order.urls', namespace='order')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^search/', search_views.MySeachView(), name='haystack_search'),
=======
>>>>>>> 642be5f8a44a62264e01c1cef0c38e2df7ef1abc
>>>>>>> dev
]
