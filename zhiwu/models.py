# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Environment(models.Model):
    # 小区环境
    name = models.CharField(max_length=30, primary_key=True)
    shangQuan = models.CharField(max_length=100)
    shuXing = models.CharField(max_length=100)
    nianXian = models.CharField(max_length=100)
    guiMo = models.CharField(max_length=100)
    anBao = models.CharField(max_length=100)


class Community(models.Model):
    # 小区信息
    name = models.CharField(max_length=30, primary_key=True)
    environment = models.ForeignKey(Environment)
    item = models.CharField(max_length=100)


class Room(models.Model):
    # 房屋信息
    roomNumber = models.CharField(max_length=10, primary_key=True)
    longitude = models.FloatField(default=120.200)
    latitude = models.FloatField(default=30.3)
    shi = models.IntegerField()
    ting = models.IntegerField()
    wei = models.IntegerField()
    rent = models.IntegerField()
    rentStyle = models.CharField(max_length=30)
    area = models.IntegerField()
    direction = models.CharField(max_length=10)
    DateToLive = models.DateField()
    lookAble = models.BooleanField()
    contactPerson = models.CharField(max_length=30)
    community = models.CharField(max_length=30)
    environment = models.CharField(max_length=30)
    sold = models.BooleanField(default=False)
    exist = models.BooleanField(default=False)
    achieve = models.BooleanField(default=False)

    def __unicode__(self):
        return self.roomNumber


class RoomRented(models.Model):
    # 房屋出租信息 todo 还有很多信息需要补全
    roomNumber = models.CharField(max_length=10, primary_key=True)
    rentDate = models.DateField()


class RoomPicture(models.Model):
    # 房屋照片
    roomNumber = models.ForeignKey(Room)
    picture = models.CharField(max_length=100)


class RoomEvaluation(models.Model):
    # 租客评价
    roomNumber = models.ForeignKey(Room)
    creatTime = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class RoomConfiguration(models.Model):
    # 房屋配置
    roomNumber = models.OneToOneField(Room, primary_key=True)
    level = models.IntegerField()
    elevator = models.BooleanField()
    canZhuo = models.BooleanField()
    shaFa = models.BooleanField()
    shuZhuo = models.BooleanField()
    yiZi = models.BooleanField()
    yiGui = models.BooleanField()
    chuang = models.BooleanField()
    kongTiao = models.BooleanField()
    xiYiJi = models.BooleanField()
    reShuiQi = models.BooleanField()
    bingXiang = models.BooleanField()
    dianShiJi = models.BooleanField()
    xiYouYanJi = models.BooleanField()
    ranQiZao = models.BooleanField()


class RoomDescription(models.Model):
    # 房屋描述
    roomNumber = models.OneToOneField(Room, primary_key=True)
    roomType = models.CharField(max_length=100)
    decoration = models.CharField(max_length=100)
    configuration = models.CharField(max_length=100)
    cook = models.CharField(max_length=100)
    light = models.CharField(max_length=100)
    wind = models.CharField(max_length=100)
    sound = models.CharField(max_length=100)
    requirement = models.CharField(max_length=100)
    suitable = models.CharField(max_length=100)


class Manager(models.Model):
    # 一级管理员
    user = models.CharField(max_length=30, primary_key=True)
    pw = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    status = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    exist = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class SecondManager(models.Model):

    # 二级管理员
    manager = models.ForeignKey(Manager)
    user = models.CharField(max_length=30, primary_key=True)
    pw = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    company = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    exist = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


# class Uploader(models.Model):
#     # 上传者
#     user = models.CharField(max_length=30, primary_key=True)
#     pw = models.CharField(max_length=30)
#     name = models.CharField(max_length=30)
#     company = models.CharField(max_length=30)
#     exist = models.BooleanField(default=True)
#
#     def __unicode__(self):
#         return self.name
#
#
# class Butler(models.Model):
#     # 管家
#     uploader = models.ForeignKey(Uploader)
#     name = models.CharField(max_length=30)
#     phone = models.CharField(max_length=11)
#     company = models.CharField(max_length=30)
#
#     def __unicode__(self):
#         return self.name
