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

    url(r'^work_search/', 'zhiwu.view.worksearch',name='work_search'),
    url(r'^home_search/', 'zhiwu.view.homesearch',name='home_search'),

    # url(r'^room_search/', 'zhiwu.view.roomsearch',name='room_search'),

    url(r'^room_detail/', 'zhiwu.view.roomdetail',name='room_detail'),
    url(r'^manager_login/', 'zhiwu.view.manager_login',name='manager_login'),
    url(r'^admin_root/', 'zhiwu.view.admin_root',name='admin_root'),
    url(r'^admin_manager/', 'zhiwu.view.admin_manager',name='admin_manager'),
    # root get user
    url(r'^admin_second_manager/', 'zhiwu.view.admin_second_manager',name='admin_second_manager'),

    # url(r'^insert/','zhiwu.views.insert', name='insert'),
    url(r'^$', 'zhiwu.views.home', name='home'),
    # url(r'^search/', 'zhiwu.views.search', name='search'),
    # url(r'^room_detail/', 'zhiwu.views.room_detail', name='room_detail'),
    # url(r'^admin_login/', 'zhiwu.views.admin_login', name='admin_login'),
    # url(r'^admin_root/', 'zhiwu.views.admin_root', name='admin_root'),
    # url(r'^admin_assessor/', 'zhiwu.views.admin_assessor', name='admin_assessor'),
    # url(r'^admin_uploader/', 'zhiwu.views.admin_uploader', name='admin_uploader'),

    # ajax
    url(r'^map_search/', 'zhiwu.view.mapsearch', name='map_search'), 
    # 地图拖动接口 data:longtitude,latitude
    url(r'^room_collection/', 'zhiwu.view.roomcollection', name='room_collection'), 
    # 收藏房源 data:room_num
    # post
    url(r'^manager_add/', 'zhiwu.view.manageradd', name='manager_add'),
    url(r'^manager_delete/', 'zhiwu.view.manageradd', name='manager_delete'),
    url(r'^manager_modify/', 'zhiwu.view.managermodify', name='manager_modify'), 
    url(r'^manager_logout/', 'zhiwu.view.managerlogout', name='manager_logout'), 
    url(r'^manager_active/', 'zhiwu.view.manageractive', name='manager_active'), 
    url(r'^manager_pw/', 'zhiwu.view.managerpw', name='manager_pw'), 

    url(r'^second_manager_add/', 'zhiwu.view.secondmanageradd', name='second_manager_add'),
    url(r'^second_manager_modify/', 'zhiwu.view.secondmanagermodify', name='second_manager_modify'), 
    url(r'^second_manager_logout/', 'zhiwu.view.secondmanagerlogout', name='second_manager_logout'), 
    url(r'^second_manager_active/', 'zhiwu.view.secondmanageractive', name='second_manager_active'), 
    url(r'^second_manager_pw/', 'zhiwu.view.secondmanagerpw', name='second_manager_pw'),

    url(r'^room_logout/', 'zhiwu.view.roomlogout', name='room_logout'),
    url(r'^room_active/', 'zhiwu.view.roomactive', name='room_active'),
    url(r'^room_save/', 'zhiwu.view.roomsave', name='room_save'),
    url(r'^room_sub/', 'zhiwu.view.roomsub', name='room_sub'),
    url(r'^room_sold/', 'zhiwu.view.roomsold', name='room_sold'),








    url(r'^admin/', include(admin.site.urls)),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
    #
    url(r'^stylesheet/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL+"stylesheet"}),
    url(r'^resource/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL+"resource"}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

]
