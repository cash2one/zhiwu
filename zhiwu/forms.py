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
    room_longitude = forms.FloatField()
    room_latitude = forms.FloatField()
    room_community = forms.CharField()
    room_shi = forms.IntegerField()
    room_ting = forms.IntegerField()
    room_wei = forms.IntegerField()
    room_rent = forms.IntegerField()
    room_area = forms.IntegerField()
    room_direction = forms.CharField()
    room_DateToLive = forms.DateField()
    room_lookAble = forms.BooleanField()
    room_contactPerson = forms.CharField()
    room_environment = forms.CharField()


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
