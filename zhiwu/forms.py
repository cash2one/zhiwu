from .models import *
from django import forms


class ImageForm(forms.Form):
    imageDate = forms.ImageField()


class AdminLogin(forms.Form):
    login_user = forms.CharField()
    login_pw = forms.CharField(widget=forms.PasswordInput)
    login_type = forms.CharField(required=False)


class RoomForm(forms.Form):
    room_roomNumber = forms.CharField()
    #房屋信息
    room_longitude = forms.FloatField()
    room_latitude = forms.FloatField()
    room_community = forms.CharField()
    room_shi = forms.IntegerField()
    room_ting = forms.IntegerField()
    room_wei = forms.IntegerField()
    room_rent = forms.IntegerField()
    room_rentStyle = forms.CharField()
    room_area = forms.IntegerField()
    room_direction = forms.CharField()
    room_DateToLive = forms.DateField()
    room_lookAble = forms.BooleanField()
    room_contactPerson = forms.CharField()
    room_environment = forms.CharField()
    #出租信息
    rentDate = forms.DateField()
    #房屋图片
    picture = forms.CharField()
    #房屋配置
    level = forms.IntegerField()
    elevator = forms.BooleanField()
    canZhuo = forms.BooleanField()
    shaFa = forms.BooleanField()
    shuZhuo = forms.BooleanField()
    yiZi = forms.BooleanField()
    yiGui = forms.BooleanField()
    chuang = forms.BooleanField()
    kongTiao = forms.BooleanField()
    xiYiJi = forms.BooleanField()
    reShuiQi = forms.BooleanField()
    bingXiang = forms.BooleanField()
    dianShiJi = forms.BooleanField()
    xiYouYanJi = forms.BooleanField()
    ranQiZao = forms.BooleanField()
    roomType = forms.CharField(max_length=100) #房屋描述
    decoration = forms.CharField(max_length=100)
    configuration = forms.CharField(max_length=100)
    cook = forms.CharField(max_length=100)
    light = forms.CharField(max_length=100)
    wind = forms.CharField(max_length=100)
    sound = forms.CharField(max_length=100)
    requirement = forms.CharField(max_length=100)
    suitable = forms.CharField(max_length=100)

class RoomEvaluation(forms.Form):
    # 租客评价
    roomNumber = forms.CharField()
    creatTime = forms.DateTimeField(auto_now_add=True)
    text = forms.CharField(widget=forms.Textarea)






class ManagerForm(forms.Form):
    manager_account = forms.CharField(required=False)
    manager_phone = forms.CharField(required=False)
    manager_name = forms.CharField(required=False)
    manager_pw = forms.CharField(widget=forms.PasswordInput, required=False)
    manager_status = forms.CharField(required=False)
    manager_district = forms.CharField(required=False)


class ManagerUserForm(forms.Form):
    manager_account = forms.CharField()


class SecondManagerForm(forms.Form):
    second_manager_assessor = forms.CharField(required=False)
    second_manager_user = forms.CharField(required=False)
    second_manager_pw = forms.CharField(widget=forms.PasswordInput, required=False)
    second_manager_name = forms.CharField(required=False)
    second_manager_phone = forms.CharField(required=False)
    second_manager_company = forms.CharField(required=False)
    second_manager_status = forms.CharField(required=False)


class SecondManagerUserForm(forms.Form):
    second_manager_account = forms.CharField()


class ManagerPwdChange(forms.Form):
    manager_account=forms.CharField(required=False)
    manager_oldpw=forms.CharField(widget=forms.PasswordInput)
    manager_newpw=forms.CharField(widget=forms.PasswordInput)

class SecondManagerPwdChange(forms.Form):
    sencond_manager_account=forms.CharField(required=False)
    second_manager_oldpw=forms.CharField(widget=forms.PasswordInput)
    second_manager_newpw=forms.CharField(widget=forms.PasswordInput)
