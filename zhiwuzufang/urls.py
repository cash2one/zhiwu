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


handler404 = 'zhiwu.views.page_not_found'
handler500 = 'zhiwu.views.page_error'

urlpatterns = [
    # test
    url(r'^test/', 'zhiwu.views.test', name='test'),

    # Part1: 页面显示url

        # 主页
        # url(r'^$', 'zhiwu.views.upload_image', name='home'),
        url(r'^$', 'zhiwu.views.home', name='home'),

        # 主页搜索
        url(r'^work_search/', 'zhiwu.views.work_search', name='work_search'),
        url(r'^home_search/', 'zhiwu.views.home_search', name='home_search'),
        url(r'^search/', 'zhiwu.views.search', name='search'),

        # 详情页
        url(r'^room_detail/', 'zhiwu.views.room_detail', name='room_detail'),
        url(r'^salehouse_detail/', 'zhiwu.views.salehouse_detail', name='salehouse_detail'),

        # 客户后台
        url(r'^client_back/', 'zhiwu.views.client_back', name='client_back'),
        # url(r'^client_back_list/', 'zhiwu.views.client_back_list', name='client_back_list'),
        # url(r'^client_back_account/', 'zhiwu.views.client_back_account', name='client_back_account'),
        # url(r'^client_back_comment/', 'zhiwu.views.client_back_comment', name='client_back_comment'),

        # 后台登陆
        url(r'^admin_login/', 'zhiwu.views.admin_login', name='admin_login'),

        # 后台注销
        url(r'^admin_logout/', 'zhiwu.views.admin_logout', name='admin_logout'),

        # 用户登录
        url(r'^user_login/', 'zhiwu.views.user_login', name='user_login'),

        # 用户注销
        url(r'^user_logout/', 'zhiwu.views.user_logout', name='user_logout'),

        # 一级管理
        url(r'^admin_root/', 'zhiwu.views.admin_root', name='admin_root'),

        # 二级管理
        url(r'^admin_manager/', 'zhiwu.views.admin_manager', name='admin_manager'),

        # 三级管理
        url(r'^admin_second_manager/', 'zhiwu.views.admin_second_manager', name='admin_second_manager'),

        # 新建房源
        url(r'^new_house/', 'zhiwu.views.new_house', name='new_house'),
        url(r'^new_salehouse/', 'zhiwu.views.new_salehouse', name='new_salehouse'),
        url(r'^use_old_house/', 'zhiwu.views.use_old_house', name='use_old_house'),
        url(r'^use_old_salehouse/', 'zhiwu.views.use_old_salehouse', name='use_old_salehouse'),


    # Part2:Post ajax

        # 区域管理
        url(r'^post_new_area/', 'zhiwu.views.post_new_area', name='post_new_area'),
        url(r'^post_delete_area/', 'zhiwu.views.post_delete_area', name='post_delete_area'),
        url(r'^area_list/', 'zhiwu.views.area_list', name='area_list'),
        url(r'^get_area_name/', 'zhiwu.views.get_area_name', name='get_area_name'),


        # 一级管理员添加，为什么名字怎么奇葩，因为一开始的需求是管理员和区域是一起建立的
        url(r'^modify_pw', 'zhiwu.views.modify_pw', name='modify_pw'),
        url(r'^area_add/', 'zhiwu.views.post_area_add', name='area_add'),
        url(r'^area_modify/', 'zhiwu.views.post_area_modify', name='area_add_or_modify'),

        url(r'^mansion_manager_add/', 'zhiwu.views.post_mansion_manager_add', name='mansion_add'),
        url(r'^mansion_manager_modify/', 'zhiwu.views.post_mansion_manager_modify', name='mansion_modify'),

        url(r'^area_search/', 'zhiwu.views.post_area_search', name='area_search'),
        url(r'^mansion_manager_search/', 'zhiwu.views.post_mansion_manager_search', name='mansion_manager_search'),
        url(r'^get_manager/', 'zhiwu.views.post_get_manager_search', name='get_manager'),
        url(r'^get_second_manager/', 'zhiwu.views.post_get_second_manager_search', name='get_second_manager'),
        url(r'^get_community/', 'zhiwu.views.post_get_community', name='get_community'),
        url(r'^get_community_list_by_manager/', 'zhiwu.views.post_get_community_list_by_manager', name='get_community_list_by_manager'),



        url(r'^manager_delete/', 'zhiwu.views.post_manager_delete', name='manager_delete'),
        # url(r'^manager_modify/', 'zhiwu.views.post_manager_modify', name='manager_modify'),
        url(r'^manager_logout/', 'zhiwu.views.post_manager_logout', name='manager_logout'),
        url(r'^manager_active/', 'zhiwu.views.post_manager_active', name='manager_active'),
        url(r'^manager_pw/', 'zhiwu.views.post_manager_pw', name='manager_pw'),

        url(r'^wuye_add/', 'zhiwu.views.wuye_add', name='wuye_add'),
        url(r'^mansion_keeper_add/', 'zhiwu.views.mansion_keeper_add', name='mansion_keeper_add'),


        url(r'^wuye_modify/', 'zhiwu.views.wuye_modify', name='wuye_modify'),
        url(r'^mansion_keeper_modify/', 'zhiwu.views.mansion_keeper_modify', name='mansion_keeper_modify'),

        url(r'^wuye_search/', 'zhiwu.views.wuye_search', name='wuye_search'),
        url(r'^mansion_keeper_search/', 'zhiwu.views.mansion_keeper_search', name='mansion_keeper_search'),

        # url(r'^second_manager_add/', 'zhiwu.views.post_second_manager_add', name='second_manager_add'),
        # url(r'^second_manager_modify/', 'zhiwu.views.post_second_manager_modify', name='second_manager_modify'),
        url(r'^second_manager_logout/', 'zhiwu.views.post_second_manager_logout', name='second_manager_logout'),
        url(r'^second_manager_delete/', 'zhiwu.views.post_second_manager_delete', name='second_manager_delete'),
        url(r'^second_manager_active/', 'zhiwu.views.post_second_manager_active', name='second_manager_active'),
        url(r'^second_manager_pw/', 'zhiwu.views.post_second_manager_pw', name='second_manager_pw'),

        # 新建房源操作
        url(r'^roominfo_save/', 'zhiwu.views.post_roominfo_save', name='roominfo_save'),
        url(r'^roominfo_submit/', 'zhiwu.views.post_roominfo_submit', name='roominfo_sub'),
        url(r'^roominfo_logout/', 'zhiwu.views.post_roominfo_logout', name='roominfo_logout'),
        url(r'^roominfo_active/', 'zhiwu.views.post_roominfo_active', name='roominfo_active'),
        url(r'^roominfo_sold/', 'zhiwu.views.post_roominfo_sold', name='roominfo_sold'),


        # 新卖房源操作
        url(r'^salehouse_save/', 'zhiwu.views.post_salehouse_save', name='salehouse_save'),
        url(r'^salehouse_submit/', 'zhiwu.views.post_salehouse_submit', name='salehouse_sub'),
        url(r'^salehouse_logout/', 'zhiwu.views.post_salehouse_logout', name='salehouse_logout'),
        url(r'^salehouse_active/', 'zhiwu.views.post_salehouse_active', name='salehouse_active'),
        url(r'^salehouse_sold/', 'zhiwu.views.post_salehouse_sold', name='salehouse_sold'),


        # 评论
        url(r'^evaluation_add/', 'zhiwu.views.post_evaluation_add', name='evaluation_add'),
        url(r'^evaluation_pass/', 'zhiwu.views.post_evaluation_pass', name='evaluation_pass'),
        url(r'^evaluation_no_pass/', 'zhiwu.views.post_evaluation_no_pass', name='evaluation_no_pass'),
        url(r'^evaluation_delete/', 'zhiwu.views.post_evaluation_delete', name='evaluation_delete'),
        url(r'^evaluation_search/', 'zhiwu.views.post_evaluation_search', name='evaluation_search'),


        # url(r'^room_save/', 'zhiwu.views.post_room_save', name='room_save'),
        # url(r'^room_sub/', 'zhiwu.views.post_room_sub', name='room_sub'),

        url(r'^upload_image/', 'zhiwu.views.upload_image', name='upload_image'),
        url(r'^community_add/', 'zhiwu.views.post_community_add', name='community_add'),
        url(r'^community_search/', 'zhiwu.views.post_community_search', name='community_search'),
        url(r'^community_delete/', 'zhiwu.views.post_community_delete', name='community_delete'),


    # Part3:Get ajax
        # 编辑时候的判断是否有房子roominfo_addr_search
        url(r'^roominfo_addr_search/', 'zhiwu.views.roominfo_addr_search', name='roominfo_addr_search'),
        url(r'^salehouse_addr_search/', 'zhiwu.views.salehouse_addr_search', name='salehouse_addr_search'),

        # 搜索页面ajax
        url(r'^map_search/', 'zhiwu.views.map_search', name='map_search'),  # 地图拖动接口 data:longtitude,latitude
        url(r'^room_collection/', 'zhiwu.views.room_collection', name='room_collection'),  # 收藏房源 data:room_num
        url(r'^room_book/', 'zhiwu.views.room_book', name='room_book'),

        url(r'^room_search', 'zhiwu.views.room_search_except', name='room_search'),
        url(r'^salehouse_search', 'zhiwu.views.salehouse_search_except', name='salsehouse_search'),

        # 文件下载的路由，get过来一些条件就可以了
        url(r'^download_roominfo', 'zhiwu.views.download_roominfo', name='download_roominfo'),
        url(r'^download_salehouse', 'zhiwu.views.download_salehouse', name='download_salehouse'),


        url(r'^admin/', include(admin.site.urls)),
        # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
        #
        url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL+"js"}),
        url(r'^stylesheet/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL+"stylesheet"}),
        url(r'^resource/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL+"resource"}),
        url(r'^font/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL+"font"}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

]
