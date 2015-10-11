# -*- coding: utf-8 -*-
from models import *
from PIL import Image
import random


def get_search_room_list(rooms):
    p = []
    for i in rooms:
        pictures = RoomPicture.objects.filter(roomNumber=i.roomNumber)
        images = []
        for j in pictures:
            images.append(j.picture)
        room = {'roomNumber': i.roomNumber,
                'price': i.price,
                'lng': 120+float(random.uniform(-0.1, 0.1)),
                'lat': 30+float(random.uniform(-0.1, 0.1)),
                'status':random.choice ( ['mansion', 'area'] ),
                'elevator': i.elevator,
                'see': i.see,
                'addr_xiaoqu': i.addr_xiaoqu,
                'type_room': i.type_room,
                'type_livingroom': i.type_livingroom,
                'type_toilet': i.type_toilet,
                'images': images}
        p.append(room)
    return p


# 判断身份
def is_root(status):
    return True
    # todo


def is_manager(status):
    return True
    # todo


def is_second_manager(status):
    return True
    # todo


# 后台管理界面得到相应的列表
def get_community_list(community=""):
    try:
        c = Community.objects.filter(name__icontains=community)
        return c
    except Exception, e:
        print e
        return []


def get_community_list_by_manager(manager=""):
    try:
        c = Community.objects.filter(manager=manager)
        return c
    except Exception, e:
        print e
        return []


def get_manager_list(user=""):
    try:
        m = Manager.objects.filter(user__icontains=user)
        return m
    except Exception, e:
        print e
        return []


def get_second_manager_list(manager):
    try:
        m = Manager.objects.filter(manager=manager)
        return m
    except Exception, e:
        print e
        return []


def roominfo_add_or_modify(roominfo_default):
    try:
        roomNumber = roominfo_default['roomNumber']
        p, created = RoomInfo.objects.update_or_create(roomNumber=roomNumber, defaults=roominfo_default)
        if p:
            print 'room info add success!'
        else:
            print 'room info modify success!'
        return True
    except Exception, e:
        print 'roominfo_add_or_modify error:'
        print e
        return False


def get_roomNumber():
    num = RoomInfo.objects.count() + 10001
    return 'HZ'+str(num)


def get_room_list_by_manager(manager=""):
    try:
        room_list = Room.objects.filter(contactPerson=manager)
        return room_list
    except Exception, e:
        print e
        return []


def get_environment(environment):
    try:
        em = RoomEvaluation.objects.get(name=environment)
        return em
    except Exception, e:
        print e
        return None


def get_room_picture(room):
    try:
        rp = RoomPicture.objects.filter(roomNumber=room)
        return rp
    except Exception, e:
        print e
        return []


def get_room_evaluation(room):
    try:
        re = RoomEvaluation.objects.get(roomNumber=room)
        return re
    except Exception, e:
        print e
        return None


def get_room_configuration(room):
    try:
        rc = RoomConfiguration.objects.get(roomNumber=room)
        return rc
    except Exception, e:
        print e
        return None


def get_room_description(room):
    try:
        rd = RoomDescription.objects.get(roomNumber=room)
        return rd
    except Exception, e:
        print e
        return None


def get_second_manager(user, pw):
    try:
        m = SecondManager.objects.get(user=user, pw=pw)
        print "get second manager success!"
        return True, m
    except Exception, e:
        print "get second manager error:"
        print e
        return False, None


def get_manager(user, pw):
    try:
        m = Manager.objects.get(user=user, pw=pw)
        print "get manager success!"
        return True, m
    except Exception, e:
        print "get manager error:"
        print e
        return False, None


def description_add(roomNumber, roomType, decoration,
                    configuration, cook, light, wind,
                    sound, requirement, suitable):
    try:
        room = Room.objects.get(roomNumbe=roomNumber)
        RoomDescription.objects.create(oomNumber=room,
                                       roomType=roomType,
                                       decoration=decoration,
                                       configuration=configuration,
                                       cook=cook,
                                       light=light,
                                       wind=wind,
                                       sound=sound,
                                       requirement=requirement,
                                       suitable=suitable)
        print "room description add success!"
        return True
    except Exception, e:
        print "room description add error!"
        print e
        return False


def description_modify(roomNumber, roomType, decoration,
                       configuration, cook, light, wind,
                       sound, requirement, suitable):
    try:
        room = Room.objects.get(roomNumbe=roomNumber)
        p = RoomDescription.objects.get(roomNumber=room)
        p.roomType = roomType
        p.decoration = decoration
        p.configuration = configuration
        p.cook = cook
        p.light = light
        p.wind = wind
        p.sound = sound
        p.requirement = requirement
        p.suitable = suitable
        p.save()
        print "room description modify success!"
        return True
    except Exception, e:
        print "room description modify error!"
        print e
        return False


def configuration_add(roomNumber, level, elevator, canZhuo,
                      shaFa, shuZhuo, yiZi, yiGui, chunag,
                      kongTiao, xiYiJi, reShuiQi, bingXiang,
                      dianShiJi, xiYouYanJi, ranQiZao):
    try:
        room = Room.objects.get(roomNumber=roomNumber)
        RoomConfiguration.objects.create(roomNumber=room,
                                         level=level,
                                         elevator=elevator,
                                         canZhuo=canZhuo,
                                         shaFa=shaFa,
                                         shuZhuo=shuZhuo,
                                         yiZi=yiZi,
                                         yiGui=yiGui,
                                         chunag=chunag,
                                         kongTiao=kongTiao,
                                         xiYiJi=xiYiJi,
                                         reShuiQi=reShuiQi,
                                         bingXiang=bingXiang,
                                         dianShiJi=dianShiJi,
                                         xiYouYanJi=xiYouYanJi,
                                         ranQiZao=ranQiZao)
        print "room configuration add success!"
        return True
    except Exception, e:
        print "room configuration add error!"
        print e
        return False


def configuration_modify(roomNumber, level, elevator, canZhuo,
                         shaFa, shuZhuo, yiZi, yiGui, chunag,
                         kongTiao, xiYiJi, reShuiQi, bingXiang,
                         dianShiJi, xiYouYanJi, ranQiZao):
    try:
        room = Room.objects.get(roomNumber=roomNumber)
        p = RoomConfiguration.objects.get(roomNumber=room)
        p.level = level
        p.elevator = elevator
        p.canZhuo = canZhuo
        p.shaFa = shaFa
        p.shuZhuo = shuZhuo
        p.yiZi = yiZi
        p.yiGui = yiGui
        p.chunag = chunag
        p.kongTiao = kongTiao
        p.xiYiJi = xiYiJi
        p.reShuiQi = reShuiQi
        p.bingXiang = bingXiang
        p.dianShiJi = dianShiJi
        p.xiYouYanJi = xiYouYanJi
        p.ranQiZao = ranQiZao
        p.save()
        print "room configuration modify success!"
        return True
    except Exception, e:
        print "room configuration modify error!"
        print e
        return False


def evaluation_add(roomNumber, text):
    try:
        room = Room.objects.get(roomNumber=roomNumber)
        RoomEvaluation.objects.create(roomNumber=room, text=text)
        print "evaluation add success!"
        return True
    except Exception, e:
        print "evaluation add error:"
        print e
        return False


def evaluation_delete(roomNumber, time):
    try:
        room = Room.objects.get(roomNumber=roomNumber)
        p = RoomEvaluation.objects.get(roomNumber=room, creatTime=time)
        p.delete()
        print "evaluation delete success!"
        return True
    except Exception, e:
        print "evaluation delete error:"
        print e
        return False


def room_picture_add(roomNumber, picture_addr):
    try:
        room = RoomInfo.objects.get(roomNumber=roomNumber)
        RoomPicture.objects.create(roomNumber=room, picture=picture_addr)
        print "room picture add success!"
        return True
    except Exception, e:
        print "room picture add error:"
        print e
        return False


def room_picture_delete(roomNumber, picture_addr):
    try:
        room = Room.objects.get(roomNumber=roomNumber)
        p = RoomPicture.objects.get(roomNumber=room, picture=picture_addr)
        p.delete()
        print "room picture delete success!"
        return True
    except Exception, e:
        print "room picture delete error:"
        print e
        return False


def room_logout(roomNumber):
    try:
        p = Room.objects.get(roomNumber=roomNumber)
        p.exist = False
        p.save(update_fields=['exist'])
        print "room logout success!"
        return True
    except Exception, e:
        print "room logout error:"
        print e
        return False


def room_active(roomNumber):
    try:
        p = Room.objects.get(roomNumber=roomNumber)
        p.exist = True
        p.save(update_fields=['exist'])
        print "room active success!"
        return True
    except Exception, e:
        print "room acitve error:"
        print e
        return False

def room_content_add(roomNumber, room_longitude, room_latitude, room_community, room_shi, \
               room_ting, room_wei, room_rent, room_area, room_direction, room_DateToLive, \
               room_lookAble, room_contactPerson, room_environment, rentDate, picture, \
               level, elevator, canZhuo, shaFa, shuZhuo, yiZi, yiGui, chuang, kongTiao, xiYiJi, reShuiQi, \
               bingXiang, dianShiJi, xiYouYanJi, ranQiZao, roomType, decoration, configuration, cook, \
               light, wind, sound, requirement, suitable,achieve):
    try:
        if not roomNumber.strip():
            roomNumber=get_roomNumber()
        room_defaults = {'longitude':room_longitude, 'latitude':room_latitude, 'community':room_community, \
                        'shi':room_shi,'ting':room_ting, 'wei':room_wei, 'rent':room_rent, 'area':room_area,\
                       'direction':room_direction, 'DateToLive':room_DateToLive,'lookAble':room_lookAble,\
                       'contactPerson':room_contactPerson, 'environment':room_environment,'sold':False,'exist':False,'achieve':False}
        rent_defaults = {'rentDate':rentDate}
        configuration_defaults = {'level': level,'elevator': elevator,'canZhuo': canZhuo,'shaFa': shaFa,'shuZhuo': shuZhuo,\
                                  'yiZi': yiZi,'yiGui': yiGui, 'chuang':chuang, 'kongTiao': kongTiao,'xiYiJi': xiYiJi,\
                                  'reShuiQi': reShuiQi, 'bingXiang': bingXiang, 'dianShiJi': dianShiJi, 'xiYouYanJi': xiYouYanJi,\
                                  'ranQiZao':ranQiZao}
        description_defaults = {'roomType': roomType,'decoration':decoration,'configuration': configuration,'cook': cook, \
                'light': light,'wind': wind,'sound': sound,'requirement': requirement,'suitable': suitable}
        p1,created1 = Room.objects.update_or_create(roomNumber=roomNumber,defaults=room_defaults)
        p1.achieve = achieve
        p1.save(update_fields=['achieve'])
        p2,created2 = RoomRented.objects.update_or_create(roomNumber=p1,defaults=rent_defaults)
        p4,created4 = RoomConfiguration.objects.update_or_create(roomNumber=p1,defaults=configuration_defaults)
        p5,created5 = RoomDescription.objects.update_or_create(roomNumber=p1,defaults=description_defaults)
        #picture
        picture_list=picture.split(';^_^;')
        p3=RoomPicture.objects.filter(roomNumber=p1)
        if p3.count() != 0:
            for pic in p3 :
                room_picture_delete(roomNumber,pic.picture)
        for pic in picture_list:
            room_picture_add(p1,pic)
        print "room content add success"
        return True
    except Exception, e:
        print  "room content add error:"
        print e
        return False

def room_save(roomNumber, room_longitude, room_latitude, room_community, room_shi, \
               room_ting, room_wei, room_rent, room_area, room_direction, room_DateToLive, \
               room_lookAble, room_contactPerson, room_environment, rentDate, picture, \
               level, elevator, canZhuo, shaFa, shuZhuo, yiZi, yiGui, chuang, kongTiao, xiYiJi, reShuiQi, \
               bingXiang, dianShiJi, xiYouYanJi, ranQiZao, roomType, decoration, configuration, cook, \
               light, wind, sound, requirement, suitable):
    try:
        p=room_content_add(roomNumber, room_longitude, room_latitude, room_community, room_shi, \
               room_ting, room_wei, room_rent, room_area, room_direction, room_DateToLive, \
               room_lookAble, room_contactPerson, room_environment, rentDate, picture, \
               level, elevator, canZhuo, shaFa, shuZhuo, yiZi, yiGui, chuang, kongTiao, xiYiJi, reShuiQi, \
               bingXiang, dianShiJi, xiYouYanJi, ranQiZao, roomType, decoration, configuration, cook, \
               light, wind, sound, requirement, suitable,False)
        if p:
            print "save success!"
        return True
    except Exception, e:
        print "save error:"
        print e
        return False


def room_sub(roomNumber,room_longitude,room_latitude,room_community,room_shi,\
                             room_ting, room_wei,room_rent,room_area,room_direction,room_DateToLive,\
                              room_lookAble,room_contactPerson,room_environment,rentDate,picture,\
                        level,elevator,canZhuo,shaFa,shuZhuo,yiZi,yiGui,chuang,kongTiao,xiYiJi,reShuiQi,\
                        bingXiang,dianShiJi,xiYouYanJi,ranQiZao,roomType,decoration,configuration,cook,\
                        light,wind,sound,requirement,suitable):
    try:
        p=room_content_add(roomNumber, room_longitude, room_latitude, room_community, room_shi, \
               room_ting, room_wei, room_rent, room_area, room_direction, room_DateToLive, \
               room_lookAble, room_contactPerson, room_environment, rentDate, picture, \
               level, elevator, canZhuo, shaFa, shuZhuo, yiZi, yiGui, chuang, kongTiao, xiYiJi, reShuiQi, \
               bingXiang, dianShiJi, xiYouYanJi, ranQiZao, roomType, decoration, configuration, cook, \
               light, wind, sound, requirement, suitable,True)
        if p:
            print 'submit success!'
        return True
    except Exception, e:
        print "submit error:"
        print e
        return False

def room_evaluation(roomNumber,text):
    try:
        p=Room.objects.get(roomNumber=roomNumber)
        RoomEvaluation.objects.create(roomNumber=p,text=text)
        print "evaluation success!"
        return True
    except Exception, e:
        print "evaluation error:"
        print e
        return False


def room_sold(roomNumber):
    try:
        p = Room.objects.get(roomNumber=roomNumber)
        p.sold = True
        p.save(update_fields=['sold'])
        print "room sold success!"
        return True
    except Exception, e:
        print "room sold error:"
        print e
        return False


def room_add(roomNumber, longitude, latitude,
             shi, ting, wei, rent, area, direction,
             DateToLive, losuccessAble, contactPerson, community, environment):
    try:
        SecondManager.objects.get(user=contactPerson)
        Community.objects.get(name=community)
        Environment.objects.get(name=environment)
        Room.objects.create(roomNumber=roomNumber,
                            longitude=longitude,
                            latitude=latitude,
                            shi=shi,
                            ting=ting,
                            wei=wei,
                            rent=rent,
                            area=area,
                            direction=direction,
                            DateToLive=DateToLive,
                            losuccessAble=losuccessAble,
                            contactPerson=contactPerson,
                            community=community,
                            environment=environment)
        print "room add success!"
        return True
    except Exception, e:
        print "room add error:"
        print e
        return False


def room_modify(roomNumber, longitude, latitude,
                shi, ting, wei, rent, area, direction,
                DateToLive, losuccessAble, contactPerson, community, environment):
    try:
        SecondManager.objects.get(user=contactPerson)
        Community.objects.get(name=community)
        Environment.objects.get(name=environment)
        p = Room.objects.get(roomNumber=roomNumber)
        p.roomNumber = roomNumber
        p.longitude = longitude
        p.latitude = latitude
        p.community = community
        p.shi = shi
        p.ting = ting
        p.wei = wei
        p.rent = rent
        p.area = area
        p.direction = direction
        p.DateToLive = DateToLive
        p.losuccessAble = losuccessAble
        p.contactPerson = contactPerson
        p.environment = environment
        p.save()
        print "room modify success!"
        return True
    except Exception, e:
        print "room modify error:"
        print e
        return False


def room_taken_off(roomNumber):
    try:
        p = Room.objects.get(roomNumber=roomNumber)
        p.exist = False
        print "room taken off success!"
        return True
    except Exception, e:
        print "room taken off error:"
        print e
        return False


def room_taken_off_cancel(roomNumber):
    try:
        p = Room.objects.get(roomNumber=roomNumber)
        p.exist = True
        print "room taken off cancel success!"
        return True
    except Exception, e:
        print "room taken off cancel error:"
        print e
        return False


def room_rented(roomNumber, rentDate):
    try:
        p = Room.objects.get(roomNumber=roomNumber)
        p.exist = False
        RoomRented.objects.create(roomNumber=roomNumber,
                                  rentDate=rentDate)
        print "room rented seccess!"
        return True
    except Exception, e:
        print "room rented error:"
        print e
        return False


def room_rented_cancel(roomNumber):
    try:
        p = Room.objects.get(roomNumber=roomNumber)
        p.exist = True
        p = RoomRented.objects.get(roomNumber=roomNumber)
        p.delete()
        print "room rented cancel success!"
        return True
    except Exception, e:
        print "room rented cancel error:"
        print e
        return False


def community_add_or_modify(name, manager, lng, lat, area, district, business, keyword, type_, year, level, facility, green, security,):
    try:
        community_default = {'name': name,
                             'manager': manager,
                             'lng': lng,
                             'lat': lat,
                             'area': area,
                             'district': district,
                             'business': business,
                             'keyword': keyword,
                             'type': type_,
                             'year': year,
                             'level': level,
                             'facility': facility,
                             'green': green,
                             'security': security}
        p, created = Community.objects.update_or_create(name=name, defaults=community_default)
        if created:
            print "community add success!"
        else:
            print "community modify success!"
        return True
    except Exception, e:
        print "community add or modify error:"
        print e
        return False


# def community_modify(name, item):
#     try:
#         p = Community.objects.get(name=name)
#         p.item = item
#         p.save()
#         print "community modify success!"
#         return True
#     except Exception, e:
#         print "community modify error:"
#         print e
#         return False


def community_delete(name):
    try:
        p = Community.objects.get(name=name)
        p.delete()
        print "community delete success!"
        return True
    except Exception, e:
        print "community delete error:"
        print e
        return False


def environment_add(name, shangquan, shuxing, nianxian, guimo, anbao):
    try:
        Environment.objects.create(name=name,
                                   shangQuan=shangquan,
                                   shuXing=shuxing,
                                   nianXian=nianxian,
                                   guiMo=guimo,
                                   anBao=anbao)
        print "environment add success!"
        return True
    except Exception, e:
        print "environment add error:"
        print e
        return False


def environment_modify(name, shangquan, shuxing, nianxian, guimo, anbao):
    try:
        p = Environment.objects.get(name=name)
        p.shangQuan = shangquan
        p.shuXing = shuxing
        p.nianXian = nianxian
        p.guiMo = guimo
        p.anBao = anbao
        p.save()
        print "environment modify success!"
        return True
    except Exception, e:
        print "environment modify error:"
        print e
        return False


def environment_delete(name):
    try:
        p = Environment.objects.get(name=name)
        p.delete()
        print "environment delete success!"
        return True
    except Exception, e:
        print "environment delete error:"
        print e
        return False


def manager_add_or_modify(user, pw, name, phone, status, district):
    try:
        manager_default = {'user': user,
                           'pw': pw,
                           'name': name,
                           'phone': phone,
                           'status': status,
                           'district': district}
        p, created = Manager.objects.update_or_create(user=user,defaults=manager_default)
        if created:
            print "Manager add success!"
        else:
            print "Manager modify success!"
        return True
    except Exception, e:
        print "Manager add or modify error:"
        print e
        return False


# def manager_modify(user, pw, name, phone, status, district):
#     try:
#         p = Manager.objects.get(user=user)
#         p.pw = pw
#         p.name = name
#         p.phone = phone
#         p.status = status
#         p.district = district
#         p.save()
#         print "manager modify success!"
#         return True
#     except Exception, e:
#         print "manager modify error:"
#         print e
#         return False


def manager_delete(user):
    try:
        p = Manager.objects.get(user=user)
        p.delete()
        print "manager delete success!"
        return True
    except Exception, e:
        print "manager delete error:"
        print e
        return False


def manager_logout(user):
    try:
        p = Manager.objects.get(user=user)
        p.exist = False
        p.save(update_fields=['exist'])
        print "manager logout success!"
        return True
    except Exception, e:
        print "manager logout error:"
        print e
        return False


def manager_active(user):
    try:
        p = Manager.objects.get(user=user)
        p.exist = True
        p.save(update_fields=['exist'])
        print "manager active success!"
        return True
    except Exception, e:
        print "manager acitve error:"
        print e
        return False


def manager_pw(user, oldpw, newpw):
    try:
        p = Manager.objects.get(user=user)
        if p.pw == oldpw:
            p.pw = newpw
            p.save(update_fields=['pw'])
            print 'pwd modify success'
            return True
        else:
            print 'pwd is not correct'
            return False
    except Exception, e:
        print 'pwd modify error:'
        print e
        return False


def second_manager_add_or_modify(manager_user, user, pw, name, phone, company, status):
    try:
        manager = Manager.objects.get(user=manager_user)
        smanager_default = {'manager': manager,
                            'user': user,
                            'pw': pw,
                            'name': name,
                            'phone': phone,
                            'company': company,
                            'status': status}

        p, created = SecondManager.objects.update_or_create(user=user, defaults=smanager_default)
        if created:
            print "SecondManager add success!"
        else:
            print "SecondManager modify success!"
        return True
    except Exception, e:
        print "SecondManager add or modify error:"
        print e
        return False


def second_manager_modify(user, pw, name, phone, company, status):
    try:
        p = SecondManager.objects.get(user=user)
        p.pw = pw
        p.name = name
        p.phone = phone
        p.company = company
        p.status = status
        p.save()
        print "SecondManager modify success!"
        return True
    except Exception, e:
        print "SecondManager modify error:"
        print e
        return False


def second_manager_logout(user):
    try:
        p = SecondManager.objects.get(user=user)
        p.exist = False
        p.save(update_fields=['exist'])
        print "second_manager logout success!"
        return True
    except Exception, e:
        print "second_manager logout error:"
        print e
        return False


def second_manager_active(user):
    try:
        p = SecondManager.objects.get(user=user)
        p.exist = True
        p.save(update_fields=['exist'])
        print "second_manager active success!"
        return True
    except Exception, e:
        print "second_manager active error:"
        print e
        return False


def second_manager_pw(user, oldpw, newpw):
    try:
        p = SecondManager.objects.get(user=user)
        if p.pw == oldpw:
            p.pw = newpw
            p.save(update_fields=['pw'])
            print 'pwd modify success'
            return True
        else:
            print 'pwd is not correct'
            return False
    except Exception, e:
        print 'pwd modify error:'
        print e
        return False


def watermark(img_source, img_water, img_new, offset_x, offset_y):
    try:
        im = Image.open(img_source)
        wm = Image.open(img_water)
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
        layer.paste(wm, (im.size[0] - offset_x, im.size[1] - offset_y))
        newIm = Image.composite(layer, im, layer)
        newIm.save(img_new)
    except Exception, e:
        print "watermark error:"
        print e
        return False
    else:
        return True

