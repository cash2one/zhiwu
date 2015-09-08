"""zhiwuzufang URL Configuration

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

urlpatterns = [
    url(r'^$', 'zhiwu.views.home', name='home'),
    url(r'^search/', 'zhiwu.views.search', name='search'),
    url(r'^room_detail/', 'zhiwu.views.room_detail', name='room_detail'),
    url(r'^admin_login/', 'zhiwu.views.admin_login', name='admin_login'),
    url(r'^admin_assessor/', 'zhiwu.views.admin_assessor', name='admin_assessor'),
    url(r'^admin_uploader/','zhiwu.views.admin_uploader', name='admin_uploader'),
    url(r'^admin/', include(admin.site.urls)),
]
