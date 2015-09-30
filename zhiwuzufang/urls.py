# -*- coding: utf-8 -*-
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
from django.conf import settings

urlpatterns = [
    url(r'^$', 'zhiwu.views.upload_image', name='home'),
    url(r'^work_search/', 'zhiwu.views.work_search', name='work_search'),
    url(r'^home_search/', 'zhiwu.views.home_search', name='home_search'),
    url(r'^room_detail/', 'zhiwu.views.room_detail', name='room_detail'),
    url(r'^manager_login/', 'zhiwu.views.admin_manager_login',name='manager_login'),
    url(r'^admin_root/', 'zhiwu.views.admin_root',name='admin_root'),
    url(r'^admin_manager/', 'zhiwu.views.admin_manager',name='admin_manager'),
    # root get user
    url(r'^admin_second_manager/', 'zhiwu.views.admin_second_manager',name='admin_second_manager'),

    # url(r'^insert/','zhiwu.views.insert', name='insert'),
    # url(r'^search/', 'zhiwu.views.search', name='search'),
    # url(r'^room_detail/', 'zhiwu.views.room_detail', name='room_detail'),
    # url(r'^admin_login/', 'zhiwu.views.admin_login', name='admin_login'),
    # url(r'^admin_root/', 'zhiwu.views.admin_root', name='admin_root'),
    # url(r'^admin_assessor/', 'zhiwu.views.admin_assessor', name='admin_assessor'),
    # url(r'^admin_uploader/', 'zhiwu.views.admin_uploader', name='admin_uploader'),

    # ajax
    url(r'^map_search/', 'zhiwu.views.map_search', name='map_search'),
    # 地图拖动接口 data:longtitude,latitude
    url(r'^room_collection/', 'zhiwu.views.room_collection', name='room_collection'),
    # 收藏房源 data:room_num
    # post
    url(r'^manager_add/', 'zhiwu.views.post_manager_add', name='manager_add'),
    url(r'^manager_delete/', 'zhiwu.views.post_manager_delete', name='manager_delete'),
    url(r'^manager_modify/', 'zhiwu.views.post_manager_modify', name='manager_modify'),
    url(r'^manager_logout/', 'zhiwu.views.post_manager_logout', name='manager_logout'),
    url(r'^manager_active/', 'zhiwu.views.post_manager_active', name='manager_active'),
    url(r'^manager_pw/', 'zhiwu.views.post_manager_pw', name='manager_pw'),

    url(r'^second_manager_add/', 'zhiwu.views.post_second_manager_add', name='second_manager_add'),
    url(r'^second_manager_modify/', 'zhiwu.views.post_second_manager_modify', name='second_manager_modify'),
    url(r'^second_manager_logout/', 'zhiwu.views.post_second_manager_logout', name='second_manager_logout'),
    url(r'^second_manager_active/', 'zhiwu.views.post_second_manager_active', name='second_manager_active'),
    url(r'^second_manager_pw/', 'zhiwu.views.post_second_manager_pw', name='second_manager_pw'),

    url(r'^room_logout/', 'zhiwu.views.post_room_logout', name='room_logout'),
    url(r'^room_active/', 'zhiwu.views.post_room_active', name='room_active'),
    url(r'^room_save/', 'zhiwu.views.post_room_save', name='room_save'),
    url(r'^room_sub/', 'zhiwu.views.post_room_sub', name='room_sub'),
    url(r'^room_sold/', 'zhiwu.views.post_room_sold', name='room_sold'),

    url(r'^upload_image/', 'zhiwu.views.upload_image', name='upload_image'),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
    #
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL+"js"}),
    url(r'^stylesheet/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL+"stylesheet"}),
    url(r'^resource/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL+"resource"}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

]
