# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Environment(models.Model):
    # 小区环境
    name = models.CharField(max_length=30, primary_key=True)
    shangQuan = models.CharField(max_length=100)
    shuXing = models.CharField(max_length=100)
    nianXian = models.CharField(max_length=100)
    guiMou = models.CharField(max_length=100)
    anBao = models.CharField(max_length=100)


class Room(models.Model):
    # 房屋信息
    roomNumber = models.CharField(max_length=10, primary_key=True)
    longitude = models.FloatField(default=120.200)
    latitude = models.FloatField(default=30.3)
    community = models.CharField(max_length=30)
    shi = models.IntegerField()
    ting = models.IntegerField()
    wei = models.IntegerField()
    rent = models.IntegerField()
    area = models.IntegerField()
    direction = models.CharField(max_length=10)
    level = models.IntegerField()
    elevator = models.BooleanField()
    timeToLive = models.TimeField()
    lookAble = models.BooleanField()
    contactPerson = models.CharField(max_length=30)
    environment = models.CharField(max_length=30)
    exist = models.BooleanField(default=True)

    def __unicode__(self):
        return self


class RoomPicture(models.Model):
    # 房屋照片
    roomNumber = models.ForeignKey(Room)
    picture = models.ImageField()


class RoomEvaluation(models.Model):
    # 租客评价
    roomNumber = models.ForeignKey(Room)
    text = models.TextField()


class RoomConfiguration(models.Model):
    # 房屋配置
    roomNumber = models.ForeignKey(Room)
    canZhuo = models.BooleanField()
    shaFa = models.BooleanField()
    shuZhuo = models.BooleanField()
    yiZi = models.BooleanField()
    yiGui = models.BooleanField()
    chunag = models.BooleanField()
    kongTiao = models.BooleanField()
    xiYiJi = models.BooleanField()
    reShuiQi = models.BooleanField()
    bingXiang = models.BooleanField()
    dianShiJi = models.BooleanField()
    xiYouYanJi = models.BooleanField()
    ranQiZao = models.BooleanField()


class RoomDescription(models.Model):
    # 房屋描述
    roomNumber = models.ForeignKey(Room)
    roomType = models.CharField(max_length=100)
    decoration = models.CharField(max_length=100)
    configuration = models.CharField(max_length=100)
    cook = models.CharField(max_length=100)
    light = models.CharField(max_length=100)
    wind = models.CharField(max_length=100)
    sound = models.CharField(max_length=100)
    requirement = models.CharField(max_length=100)
    suitable = models.CharField(max_length=100)


class Assessor(models.Model):
    # 鉴定员
    user = models.CharField(max_length=30, primary_key=True)
    pw = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    exist = models.BooleanField(default=True)
    status = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Broker(models.Model):
    # 经纪人
    assessor = models.ForeignKey(Assessor)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    company = models.CharField(max_length=30)
    status = models.CharField(max_length=30)

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
