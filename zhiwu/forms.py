# -*- coding: utf-8 -*-
from .models import *
from django import forms
from django.forms import ModelForm


class CommunityDeleteForm(forms.Form):
    id = forms.CharField()


class CommunityForm(forms.Form):
    xiaoqu_add_manager = forms.CharField()
    xiaoqu_add_name = forms.CharField()
    xiaoqu_add_lng = forms.FloatField()
    xiaoqu_add_lat = forms.FloatField()
    xiaoqu_add_area = forms.CharField()
    xiaoqu_add_district = forms.CharField()
    xiaoqu_add_business = forms.CharField()
    xiaoqu_add_keyword = forms.CharField()
    xiaoqu_add_type = forms.CharField()
    xiaoqu_add_year = forms.CharField()
    xiaoqu_add_level = forms.CharField()
    xiaoqu_add_facility = forms.CharField()
    xiaoqu_add_green = forms.CharField()
    xiaoqu_add_security = forms.CharField()


class ImageForm(forms.Form):
    imageDate = forms.ImageField()


class AdminLogin(forms.Form):
    login_user = forms.CharField()
    login_pw = forms.CharField(widget=forms.PasswordInput)
    login_type = forms.CharField(required=False)


class RoomForm(forms.Form):
    room_roomNumber = forms.CharField()
    #房屋信息
    room_longitude = forms.FloatField(required=False)
    room_latitude = forms.FloatField(required=False)
    room_community = forms.CharField(required=False)
    room_shi = forms.IntegerField(required=False)
    room_ting = forms.IntegerField(required=False)
    room_wei = forms.IntegerField(required=False)
    room_rent = forms.IntegerField(required=False)
    room_rentStyle = forms.CharField(required=False)
    room_area = forms.IntegerField(required=False)
    room_direction = forms.CharField(required=False)
    room_DateToLive = forms.DateField(required=False)
    room_lookAble = forms.BooleanField(required=False)
    room_contactPerson = forms.CharField(required=False)
    room_environment = forms.CharField(required=False)
    #出租信息
    rentDate = forms.DateField(required=False)
    #房屋图片
    picture = forms.CharField(required=False)
    #房屋配置
    level = forms.IntegerField(required=False)
    elevator = forms.BooleanField(required=False)
    canZhuo = forms.BooleanField(required=False)
    shaFa = forms.BooleanField(required=False)
    shuZhuo = forms.BooleanField(required=False)
    yiZi = forms.BooleanField(required=False)
    yiGui = forms.BooleanField(required=False)
    chuang = forms.BooleanField(required=False)
    kongTiao = forms.BooleanField(required=False)
    xiYiJi = forms.BooleanField(required=False)
    reShuiQi = forms.BooleanField(required=False)
    bingXiang = forms.BooleanField(required=False)
    dianShiJi = forms.BooleanField(required=False)
    xiYouYanJi = forms.BooleanField(required=False)
    ranQiZao = forms.BooleanField(required=False)
    roomType = forms.CharField(max_length=100,required=False) #房屋描述
    decoration = forms.CharField(max_length=100,required=False)
    configuration = forms.CharField(max_length=100,required=False)
    cook = forms.CharField(max_length=100,required=False)
    light = forms.CharField(max_length=100,required=False)
    wind = forms.CharField(max_length=100,required=False)
    sound = forms.CharField(max_length=100,required=False)
    requirement = forms.CharField(max_length=100,required=False)
    suitable = forms.CharField(max_length=100,required=False)


class RoomEvaluationForm(forms.Form):
    # 租客评价
    roomNumber = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)


class RoomShortForm(forms.Form):
    room_roomNumber = forms.CharField()


class ManagerForm(forms.Form):
    manager_account = forms.CharField(required=False)
    manager_phone = forms.CharField(required=False)
    manager_name = forms.CharField(required=False)
    manager_pw = forms.CharField(widget=forms.PasswordInput, required=False)
    manager_status = forms.CharField(required=False)
    manager_district = forms.CharField(required=False)


class ManagerUserForm(forms.Form):
    id = forms.CharField()


class SecondManagerForm(forms.Form):
    second_manager_manager = forms.CharField(required=False)#foreignkey
    second_manager_account = forms.CharField(required=False)
    second_manager_pw = forms.CharField(widget=forms.PasswordInput, required=False)
    second_manager_name = forms.CharField(required=False)
    second_manager_phone = forms.CharField(required=False)
    second_manager_company = forms.CharField(required=False)
    second_manager_status = forms.CharField(required=False)


class SecondManagerUserForm(forms.Form):
    id = forms.CharField()


class ManagerPwdChange(forms.Form):
    manager_account=forms.CharField(required=False)
    manager_oldpw=forms.CharField(widget=forms.PasswordInput)
    manager_newpw=forms.CharField(widget=forms.PasswordInput)

class SecondManagerPwdChange(forms.Form):
    sencond_manager_account=forms.CharField(required=False)
    second_manager_oldpw=forms.CharField(widget=forms.PasswordInput)
    second_manager_newpw=forms.CharField(widget=forms.PasswordInput)

class TenantForm(forms.Form):
    tenant_id = forms.CharField()
    tenant_pw = forms.CharField(widget=forms.PasswordInput)
    tenant_name = forms.CharField(max_length=30)
    tenant_phone = forms.CharField(max_length=11)
    tenant_profession = forms.CharField(max_length=30, required=False)

class TenantLoginForm(forms.Form):
    tenant_id = forms.CharField()
    tenant_pw = forms.CharField(widget=forms.PasswordInput)

class TenantUserForm(forms.Form):
    tenant_id = forms.CharField()

# class RequirementForm(forms.Form): 用于test
#    # requireId = models.AutoField(primary_key=True);
#     user = forms.CharField()
#     priceMin = forms.IntegerField()
#     priceMax = forms.IntegerField()
#     #基本房屋信息
#     addr_xiaoqu = forms.CharField(max_length=30,required=False)
#     payway = forms.CharField(max_length=30,required=False)
#     type_room = forms.CharField(max_length=30,required=False)
#     type_livingroom = forms.CharField(max_length=30,required=False)
#     type_toilet = forms.CharField(max_length=30,required=False)
#     floor_level = forms.CharField(max_length=30,required=False)
#     level = forms.IntegerField()
#     #房屋配置
#     elevator = forms.CharField(max_length=30, required=False)
#     canzhuo = forms.CharField(max_length=30, required=False)
#     sofa = forms.CharField(max_length=30, required=False)
#     desk = forms.CharField(max_length=30, required=False)
#     chair = forms.CharField(max_length=30, required=False)
#     closet = forms.CharField(max_length=30,required=False)
#     bed = forms.CharField(max_length=30, required=False)
#     aircon = forms.CharField(max_length=30, required=False)
#     washer = forms.CharField(max_length=30,required=False)
#     waterheater = forms.CharField(max_length=30,required=False)
#     refregister = forms.CharField(max_length=30, required=False)
#     tv = forms.CharField(max_length=30, required=False)
#     cookerhood = forms.CharField(max_length=30, required=False)
#     gascooker = forms.CharField(max_length=30, required=False)
#     #房源描述
#     original_house_type = forms.CharField(max_length=200,required=False)
#     decorate_level = forms.CharField(max_length=200,required=False)
#     config_level = forms.CharField(max_length=200,required=False)
#     can_cook = forms.CharField(max_length=200,required=False)
#     lighting = forms.CharField(max_length=200,required=False)
#     ventilate = forms.CharField(max_length=200,required=False)
#     noise = forms.CharField(max_length=200,required=False)


