# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
# from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core import serializers
from .forms import *
from .help import *
from zhiwu.models import *
import json
import time
import os
import random
from pyExcelerator import *
# Create your views here.

rename = {"code": 0, "msg": "用户已经存在"}
not_valid = {"code": 0, "msg": "信息不合法"}
not_exist = {"code": 0, "msg": "用户不存在"}
success = {"code": 1}
fail = {"code": 0}


def page_not_found(request):
    return render(request, "404.html")


def page_error(request):
    return render(request, "500.html")


def home(request):
    return render(request, "index.html")


# def home(request):
#     # room = ManagerForm()
#     r = {"user": 2, "kk":3}
#     # return HttpResponseRedirect("admin_manager")
#
#     return render(request, "detail.html", {"r": json.dumps(r)})
#     # return HttpResponse("hello world",status=200)

def test(request):
    room = RoomPicture.objects.all()
    print request.POST.get('issalehouse', '')
    p = RoomEvaluationForm()
    return render(request, "home.html", {'kk': p})


def check_root(request):
    try:
        user = request.session.get('user')
        status = request.session.get('status')
        if status == 'root':
            return True, user, status
        else:
            return False, None, None
    except Exception, e:
        print 'check root error:'
        print e
        return False, None, None


def check_manager(request):
    try:
        user = request.session.get('user')
        status = request.session.get('status')
        if status == 'manager':
            return True, user, status
        else:
            return False, None, None
    except Exception, e:
        print 'check root error:'
        print e
        return False, None, None


def search(request):
    return render(request, "companyPresent.html")


def work_search(request):
    user, status, identity = user_session_check(request)
    try:
        distance = {"walk": {"5": 0.005, "10": 0.010, "15": 0.015, "20": 0.020, "30": 0.030, "45": 0.045, "60": 0.060},
                    "bus": {"5": 0.010, "10": 0.020, "15": 0.025, "20": 0.040, "30": 0.50, "45": 0.075, "60": 0.100},
                    "drive": {"5": 0.020, "10": 0.03, "15": 0.050, "20": 0.080, "30": 0.100, "45": 0.150, "60": 0.200}}
        work_location = request.GET.get("work_location", None)
        time_get = request.GET.get("time", None)
        way = request.GET.get("way", None)
        longitude = float(request.GET.get("lng", None))
        latitude = float(request.GET.get("lat", None))
        sts = request.GET.get("status", None)
        if time is None or way is None or longitude is None and latitude is None:
            print "get 信息不全:"
            return page_not_found(request)
        else:
            try:
                dis = distance.get(way).get(time_get)
            except:
                return page_not_found(request)
            if dis is None:
                return page_not_found(request)
            if sts == 'sale':
                rooms = SaleHouse.objects.filter(lng__range=(longitude - dis, longitude + dis),
                                                 lat__range=(latitude - dis, latitude + dis),
                                                 exist=True,
                                                 sold=False)
                room_list = get_search_saldhouse_list(rooms, user)
                return render(request, "searchForSale.html", {"rooms": json.dumps(room_list),
                                                              "lng": json.dumps(longitude),
                                                              "lat": json.dumps(latitude),
                                                              "way": way,
                                                              "time": json.dumps(time_get),
                                                              "isWork": True,
                                                              "user": user})
            elif sts == 'rent':
                rooms = RoomInfo.objects.filter(lng__range=(longitude - dis, longitude + dis),
                                                lat__range=(latitude - dis, latitude + dis),
                                                exist=True,
                                                sold=False)
                room_list = get_search_room_list(rooms, user)
                return render(request, "search.html", {"rooms": json.dumps(room_list),
                                                       "lng": json.dumps(longitude),
                                                       "lat": json.dumps(latitude),
                                                       "way": way,
                                                       "time": json.dumps(time_get),
                                                       "isWork": True,
                                                       "user": user})
            else:
                return page_not_found(request)
    except Exception, e:
        print "work search error:"
        print e
        return page_not_found(request)


def home_search(request):
    user, status, identity = user_session_check(request)
    location = request.GET.get("home_location", None)
    longitude = request.GET.get("lng", "120.170245")
    latitude = request.GET.get("lat", "30.278905")
    sts = request.GET.get("status", None)
    if longitude is None or longitude == "":
        longitude = 120.170245
    else:
        longitude = float(longitude)
    if latitude is None or latitude == "":
        latitude = 30.278905
    else:
        latitude = float(latitude)
    cs = Community.objects.filter(Q(name__icontains=location) | Q(keyword__icontains=location))
    dis = 0.010
    if sts == 'sale':
        rooms = SaleHouse.objects.filter(addr_xiaoqu__in=cs, exist=True, sold=False)
        if len(rooms) == 0:
            rooms = SaleHouse.objects.filter(lng__range=(longitude - dis, longitude + dis),
                                             lat__range=(latitude - dis, latitude + dis),
                                             exist=True,
                                             sold=False)
        room_list = get_search_saldhouse_list(rooms, user)
        return render(request, "searchForSale.html", {"rooms": json.dumps(room_list),
                                                      "lng": json.dumps(longitude),
                                                      "lat": json.dumps(latitude),
                                                      "isWork": False,
                                                      "user": user})
    elif sts == 'rent':
        rooms = RoomInfo.objects.filter(addr_xiaoqu__in=cs, exist=True, sold=False)
        if len(rooms) == 0:
            rooms = RoomInfo.objects.filter(lng__range=(longitude - dis, longitude + dis),
                                            lat__range=(latitude - dis, latitude + dis),
                                            exist=True,
                                            sold=False)
        room_list = get_search_room_list(rooms, user)
        return render(request, "search.html", {"rooms": json.dumps(room_list),
                                               "lng": json.dumps(longitude),
                                               "lat": json.dumps(latitude),
                                               "isWork": False,
                                               "user": user})
    else:
        return page_not_found(request)


def map_search(request):
    user, status, identity = user_session_check(request)
    try:
        # longitude = models.FloatField(default=120.200)
        # latitude = models.FloatField(default=30.3)
        longitude_l = request.POST.get("lng_left", None)
        latitude_l = request.POST.get("lat_left", None)
        longitude_r = request.POST.get("lng_right", None)
        latitude_r = request.POST.get("lat_right", None)
        sts = request.POST.get("status", None)
        if sts == 'sale':
            rooms = SaleHouse.objects.filter(lng__range=(longitude_l, longitude_r),
                                             lat__range=(latitude_l, latitude_r),
                                             exist=True,
                                             sold=False)
            room_list = get_search_saldhouse_list(rooms, user)
        elif sts == 'rent':
            rooms = RoomInfo.objects.filter(lng__range=(longitude_l, longitude_r),
                                            lat__range=(latitude_l, latitude_r),
                                            exist=True,
                                            sold=False)
            room_list = get_search_room_list(rooms, user)
        else:
            return page_not_found(request)
        result = {"code": 1,
                  "newData": room_list}
        return JsonResponse(result, safe=False)
    except Exception, e:
        print "map search error:"
        print e
        return JsonResponse(fail)


def salehouse_detail(request):
    try:
        roomNum = request.GET.get('roomNumber')
        room = SaleHouse.objects.get(roomNumber=roomNum)
        evaluation = SaleHouseEvaluation.objects.filter(roomNumber=roomNum, ifpass=True).order_by('createTime')
        cp = SecondManager.objects.get(user=room.contactPerson)
        roomP = get_salehouse_picture(room)
        return render(request, "detailForSale.html", {"room": room,
                                               "lat": json.dumps(room.lat),
                                               "lng": json.dumps(room.lng),
                                               "evaluation": evaluation,
                                               "contactPerson": cp,
                                               "picture": roomP})
    except Exception, e:
        print e
        return page_not_found(request)

def room_detail(request):
    try:
        roomNum = request.GET.get('roomNumber')
        room = RoomInfo.objects.get(roomNumber=roomNum)
        evaluation = RoomEvaluation.objects.filter(roomNumber=roomNum, ifpass=True).order_by('createTime')
        cp = SecondManager.objects.get(user=room.contactPerson)
        roomP = get_room_picture(room)
        return render(request, "detail.html", {"room": room,
                                               "lat": json.dumps(room.lat),
                                               "lng": json.dumps(room.lng),
                                               "evaluation": evaluation,
                                               "contactPerson": cp,
                                               "picture": roomP})
    except Exception, e:
        print e
        return page_not_found(request)


def admin_login(request):
    if request.method == "POST":
        form = AdminLogin(request.POST)
        if form.is_valid():
            try:
                user = form.cleaned_data['account']
                pw = form.cleaned_data['password']
                identity = form.cleaned_data['identity']
                if identity == "manager":
                    tag, m, msg = get_manager(user, pw)
                elif identity == "second_manager":
                    tag, m, msg = get_second_manager(user, pw)
                elif identity == "root":
                    tag, m, msg = get_root(user, pw)
                else:
                    return JsonResponse(fail)
                    # 身份不正确
                if tag:
                    request.session['user'] = m.user
                    request.session['status'] = m.status
                    request.session['identity'] = identity
                    if identity == "root":
                        print 'root login'
                        #return HttpResponseRedirect(reverse('admin_root'))
                        return JsonResponse({"code": 1, "url": "/admin_root"})
                    elif identity == "manager":
                        print 'manager login'
                        #return HttpResponseRedirect(reverse('admin_manager'))
                        return JsonResponse({"code": 1, "url": "/admin_manager"})
                    else:
                        print 'second manager login'
                        #return HttpResponseRedirect(reverse('admin_second_manager'))
                        return JsonResponse({"code": 1, "url": "/admin_second_manager"})
                else:
                    return JsonResponse({"code": 0, "msg": msg})
                    # 账号密码错误
            except Exception, e:
                print 'admin manager login error:'
                print e
                return page_not_found(request)
    else:
        return render(request, "loginForBack.html")


def admin_logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('admin_login'))


def user_login(request):
    if request.method == 'POST':
        user = request.POST.get('phone')
        request.session['user'] = user
        request.session['identity'] = 'user'
        request.session['status'] = 'user'
        return JsonResponse(success)
    else:
        return page_not_found(request)


def user_logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('home'))


def admin_root(request):
    identity = request.session.get("identity", "")
    status = request.session.get("status", "")
    user = request.session.get("user", "")
    if is_root(identity):
        m_list = get_manager_list()
        community_list = get_community_list()
        e = RoomEvaluation.objects.order_by('-createTime')[0:10]
        count = RoomEvaluation.objects.count()
        areas = Area.objects.all()
        if status == 'root':
            html = "backend.html"
        else:
            html = "backendSearch.html"
        return render(request, html, {"managers": m_list,
                                      "managers_js": json.dumps(serializers.serialize('json',m_list)),
                                      "evaluation_count": count,
                                      "status": status,
                                      "identity": json.dumps(identity),
                                      "user": user,
                                      "communities": community_list,
                                      "area_list": areas})
    else:
        return HttpResponseRedirect(reverse("admin_login"))


def admin_manager(request):
    status = request.session.get("status", "")
    identity = request.session.get("identity", "")
    user = request.session.get("user", "")
    if not is_manager(identity):
        return HttpResponseRedirect(reverse("admin_login"))
    try:
        manager = Manager.objects.get(user=user)
    except Exception, e:
        print "admin manager error:"
        print e
        return HttpResponseRedirect(reverse("admin_login"))
        # return render(request, "backendL1.html")
    m_list = get_second_manager_list(manager)
    c_list = get_community_list_by_manager(user)
    # m_list = json.dumps(serializers.serialize('json', m_list))
    return render(request, "backendL1.html", {"second_managers": m_list,
                                              "community_list": c_list,
                                               "manager": manager,
                                              "status": status,
                                              "identity": json.dumps(identity),
                                              "user": user})


def admin_second_manager(request):
    status = request.session.get("status", "")
    identity = request.session.get("identity", "")
    user = request.session.get("user", "")
    if not is_second_manager(identity):
        return HttpResponseRedirect(reverse("admin_login"))
    rooms = RoomInfo.objects.filter(contactPerson=user)
    salehouses = SaleHouse.objects.filter(contactPerson=user)
    rms = []
    shs = []
    for i in rooms:
        rms.append({"info": i, "picture": RoomPicture.objects.filter(roomNumber=i).exists()})
    for i in salehouses:
        shs.append({"info": i, "picture": SaleHousePicture.objects.filter(roomNumber=i).exists()})
    # rooms = json.dumps(serializers.serialize('json', rooms))
    return render(request, "backendL2.html", {"rooms": rms,
                                              "salehouses": shs,
                                              "identity": json.dumps(identity),
                                              "status": status,
                                              "user": user})


def new_house(request):
    return new_house_handle(request, False)


def new_house_handle(request, use_old):
    roomNumber = request.GET.get("roomNumber", "")
    user = request.session.get("user")
    status = request.session.get("status", "")
    identity = request.session.get("identity", "")
    if is_second_manager(identity) or is_root(identity) or is_manager(identity):
        if roomNumber == "":
            sm = SecondManager.objects.get(user=user)
            communities = Community.objects.get(name=sm.company)
            return render(request, "newHouse.html", {"user": user,
                                                     "status": status,
                                                     "identity": json.dumps(identity),
                                                     "communities": communities})
        else:
            roominfo = RoomInfo.objects.get(roomNumber=roomNumber)
            sm = SecondManager.objects.get(user=roominfo.contactPerson)
            communities = Community.objects.get(name=sm.company)
            pictures = RoomPicture.objects.filter(roomNumber=roominfo)
            merit = roominfo.merit.split(',')
            landlord_req = roominfo.landlord_req.split(',')
            images = []
            for i in pictures:
                data = {
                    'url': i.picture,
                    'thumbnailUrl': i.picture,
                    'name': i.picture.split('/')[-1],
                    'size':  os.path.getsize('./zhiwu'+i.picture)
                }
                images.append(data)
            if use_old:
                roominfo.roomNumber = get_roomNumber()
            elif roominfo.sold:
                return page_not_found(request)
            return render(request, "editHouse.html", {"user": user,
                                                      "status": status,
                                                      "room": roominfo,
                                                      "merit": merit,
                                                      "identity": json.dumps(identity),
                                                      "landlord_req": landlord_req,
                                                      "lat": json.dumps(roominfo.lat),
                                                      "lng": json.dumps(roominfo.lng),
                                                      "files": json.dumps(images),
                                                      "communities": communities})
    else:
        return HttpResponseRedirect(reverse("admin_login"))


def new_salehouse(request):
    return new_salehouse_handle(request, False)


def new_salehouse_handle(request, use_old):
    roomNumber = request.GET.get("roomNumber", "")
    user = request.session.get("user")
    status = request.session.get("status", "")
    identity = request.session.get("identity", "")
    if is_second_manager(identity) or is_root(identity) or is_manager(identity):
        if roomNumber == "":
            sm = SecondManager.objects.get(user=user)
            communities = Community.objects.get(name=sm.company)
            return render(request, "newHouseForSale.html", {"user": user,
                                                            "status": status,
                                                            "identity": json.dumps(identity),
                                                            "communities": communities})
        else:
            salehouse = SaleHouse.objects.get(roomNumber=roomNumber)
            sm = SecondManager.objects.get(user=salehouse.contactPerson)
            communities = Community.objects.get(name=sm.company)
            pictures = SaleHousePicture.objects.filter(roomNumber=salehouse)
            images = []
            for i in pictures:
                data = {
                    'url': i.picture,
                    'thumbnailUrl': i.picture,
                    'name': i.picture.split('/')[-1],
                    'size':  os.path.getsize('./zhiwu'+i.picture)
                }
                images.append(data)
            if use_old:
                salehouse.roomNumber = get_salehouseNumber()
            elif salehouse.sold:
                return page_not_found(request)
            return render(request, "editHouseForSale.html", {"user": user,
                                                             "status": status,
                                                             "room": salehouse,
                                                             "lat": json.dumps(salehouse.lat),
                                                             "lng": json.dumps(salehouse.lng),
                                                             "identity": json.dumps(identity),
                                                             "files": json.dumps(images),
                                                             "communities": communities})
    else:
        return HttpResponseRedirect(reverse("admin_login"))


# todo


def use_old_house(request):
    return new_house_handle(request, True)


def use_old_salehouse(request):
    return new_salehouse_handle(request, True)


def client_back(request):
    user, status, identity = user_session_check(request)
    collects = RoomCollect.objects.filter(user=user)
    c_list = []
    for i in collects:
        c_list.append(i.roomNumber)
    rooms = RoomInfo.objects.filter(roomNumber__in=c_list)
    houses = SaleHouse.objects.filter(roomNumber__in=c_list)
    room_list = get_search_room_list(rooms, user)
    house_list = get_search_saldhouse_list(houses, user)
    return render(request, "clientBackend.html",{"room_list": room_list,
                                                 "house_list": house_list,
                                                 "user": user})
# def client_back_account(request):
#     return render(request, "myAccount.html",{"route":"account"})
#
#
# def client_back_list(request):
#     return render(request, "mylist.html",{"route":"list"})
#
#
# def client_back_comment(request):
#     return render(request, "serviceContact.html",{"route":"comment"})


def room_collection(request):
    user, status, identity = user_session_check(request)
    if request.method == 'POST':
        try:
            roomNumber = request.POST.get('roomNumber', '')
            if identity == 'user' and user != '':
                if roomNumber != '':
                    c, created = RoomCollect.objects.get_or_create(roomNumber=roomNumber, user=user)
                    if created:
                        return JsonResponse({'code': 1, 'msg': '收藏成功'})
                    else:
                        c.delete()
                        return JsonResponse({'code': 1, 'msg': '取消收藏成功'})
                else:
                    return JsonResponse({'code': 0, 'msg': '没有房源编号'})

            else:
                return JsonResponse({'code': 0, 'msg': '没有登陆'})
        except Exception, e:
            print 'collection error:'
            print e
            return JsonResponse(fail)
    else:
        return page_not_found(request)


def room_book(request):
    user, status, identity = user_session_check(request)
    roomNumber = request.POST.get('roomNumber')

    return JsonResponse(success)

# post
# JianDing

def post_new_area(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', None)
            p, created = Area.objects.get_or_create(name=name)
            if created:
                return JsonResponse(success)
            else:
                return JsonResponse({'code': 0, 'msg': '区域名已经存在'})
        except Exception, e:
            print 'post new area error:'
            print e
            return JsonResponse(fail)
    else:
        return page_not_found(request)


def post_delete_area(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('id')
            p = Area.objects.get(name=name)
            p.delete()
            return JsonResponse(success)
        except Exception, e:
            print 'post new area error:'
            print e
            return JsonResponse({'code': 0, 'msg': '区域名不存在'})
    else:
        return page_not_found(request)


def get_area_name(request):
    try:
        name = request.GET.get('name')
        areas = Area.objects.filter(name__icontains=name)
        areas = serializers.serialize('json', areas)
        result = {'code': 1,
                  'context': areas}
        return JsonResponse(result, safe=False)
    except Exception, e:
        print 'get area name error:'
        print e
        return JsonResponse(fail)


def area_list(request):
    areas = Area.objects.all()
    areas = serializers.serialize('json', areas)
    return JsonResponse(areas, safe=False)


def post_area_search(request):
    try:
        return manager_search(request, 'area')
    except Exception, e:
        print e
        return JsonResponse(fail)


def post_mansion_manager_search(request):
    try:
        return manager_search(request, 'mansion')
    except Exception, e:
        print e
        return JsonResponse(fail)


def manager_search(request, status):
    district = request.GET.get('manager_search_district', "")
    m_list = Manager.objects.filter(district__icontains=district,
                                    status = status)
    result = {'code': 1,
              'context': serializers.serialize('json', m_list)}
    return JsonResponse(result, safe=False)


def post_get_manager_search(request):
    try:
        user = request.GET.get('id')
        m = Manager.objects.get(user=user)
        areas = Area.objects.all()
        area_l = []
        for i in areas:
            area_l.append(i.name)
        result = {'code': 1,
                  'context': {'user': m.user,
                              'pw': m.pw,
                              'name': m.name,
                              'phone': m.phone,
                              'status': m.status,
                              'district': m.district,
                              'area_list': area_l,
                              'exist': m.exist}}
        return JsonResponse(result)
    except Exception, e:
        print e
        return JsonResponse(fail)


def post_get_second_manager_search(request):
    try:
        user = request.GET.get('id')
        m = SecondManager.objects.get(user=user)
        c = Community.objects.filter(manager=m.manager.user)
        c_list = []
        for i in c:
            c_list.append(i.name)
        result = {'code': 1,
                  'context': {'community_list': c_list,
                              'manager': m.manager.user,
                              'user': m.user,
                              'pw': m.pw,
                              'name': m.name,
                              'phone': m.phone,
                              'company': m.company,
                              'status': m.status,
                              'exist': m.exist}}
        return JsonResponse(result)
    except Exception, e:
        print e
        return JsonResponse(fail)


def post_get_community_list_by_manager(request):
    try:
        manager = request.GET.get('id')
        c_list = Community.objects.filter(manager=manager)
        c_list = serializers.serialize('json', c_list)
        result = {'code': 1,
                  'context': c_list}
        return JsonResponse(result, safe=False)
    except Exception, e:
        print 'post_get_community_list_by_manager error:'
        print e
        return JsonResponse(fail)


def post_get_community(request):
    try:
        name = request.GET.get('id')
        c = Community.objects.get(name=name)
        m_list = get_manager_list()
        ms = []
        for i in m_list:
            ms.append(i.user)
        result = {'code': 1,
                  'context': {'manager_list': ms,
                              'name': c.name,
                              'manager': c.manager,
                              # 'item': c.item,
                              'lng': c.lng,
                              'lat': c.lat,
                              # 'area': c.area,
                              # 'district': c.district,
                              'business': c.business,
                              'keyword': c.keyword,
                              'type': c.type,
                              'year': c.year,
                              'level': c.level,
                              # 'facility': c.facility,
                              # 'green': c.green,
                              'security': c.security}}
        return JsonResponse(result)
    except Exception, e:
        print e
        return JsonResponse(fail)


def modify_pw(request):
    try:
        user = request.session.get('user', '')
        status = request.session.get('status', '')
        identity = request.session.get('identity', '')
        old_pw = request.POST.get("old_pw", None)
        new_pw = request.POST.get("new_pw", None)
        if old_pw is not None and new_pw is not None:
            try:
                if identity == "root":
                    m = Root.objects.get(user=user, pw=old_pw)
                elif identity == "manager":
                    m = Manager.objects.get(user=user, pw=old_pw)
                elif identity == "second_manager":
                    m = SecondManager.objects.get(user=user, pw=old_pw)
                else:
                    return JsonResponse({"code": 0, "msg": "身份不存在"})
            except :
                return JsonResponse({"code": 0, "msg": "旧密码不正确"})
            m.pw = new_pw
            m.save()
            return JsonResponse(success)
        else:
            return JsonResponse({"code": 0, "msg": "信息不全"})
    except Exception, e:
        print "modify error:"
        print e
        return JsonResponse(fail)


def post_area_add(request):
    return post_manager_add(request, "area")


def post_area_modify(request):
    return post_manager_modify(request, "area")


def post_mansion_manager_add(request):
    return post_manager_add(request, "mansion")


def post_mansion_manager_modify(request):
    return post_manager_modify(request, "mansion")


# code from here
def post_manager_add(request, status):
    if request.method == 'POST':  # 当提交表单时
        form = ManagerForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['manager_account']
                pw = form.cleaned_data['manager_pw']
                name = form.cleaned_data['manager_name']
                phone = form.cleaned_data['manager_phone']
                district = form.cleaned_data['manager_district']
                p = manager_add(user, pw, name, phone, status, district)
                if p:
                    return JsonResponse(success)
                else:
                    return JsonResponse(rename)
            except Exception, e:
                print e
                return JsonResponse(not_valid)
        else:
            return JsonResponse(not_valid)
    else:  # 当正常访问时
        return page_not_found(request)


def post_manager_modify(request, status):
    if request.method == 'POST':  # 当提交表单时
        form = ManagerForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['manager_account']
                pw = form.cleaned_data['manager_pw']
                name = form.cleaned_data['manager_name']
                phone = form.cleaned_data['manager_phone']
                district = form.cleaned_data['manager_district']
                p = manager_modify(user, pw, name, phone, status, district)
                if p:
                    return JsonResponse(success)
                else:
                    return JsonResponse(not_exist)
            except Exception, e:
                print e
                return JsonResponse(not_valid)
        else:
            return JsonResponse(not_valid)
    else:  # 当正常访问时
        return page_not_found(request)


# 添加或者修改一条一级管理员


# def post_manager_modify(request):
#     if request.method == 'POST':  # 当提交表单时
#         form = ManagerForm(request.POST)  # form 包含提交的数据
#         if form.is_valid():  # 如果提交的数据合法
#             try:
#                 user = form.cleaned_data['manager_account']
#                 pw = form.cleaned_data['manager_pw']
#                 name = form.cleaned_data['manager_name']
#                 phone = form.cleaned_data['manager_phone']
#                 status = form.cleaned_data['manager_status']
#                 district = form.cleaned_data['manager_district']
#                 p = manager_modify(user, pw, name, phone, status, district)
#                 return HttpResponse(status=1)
#             except Exception, e:
#                 print e
#                 return HttpResponse(status=0)
#     else:  # 当正常访问时
#         print 'not post'
# # 修改一条一级管理员


# def post_manager_create(request):
#     if request.method == 'POST':  # 当提交表单时
#         form = ManagerUserForm(request.POST)  # form 包含提交的数据
#         if form.is_valid():  # 如果提交的数据合法
#             try:
#                 user = form.cleaned_data['manager_account']
#                 p, flag = Manager.objects.get_or_create(user=user)
#                 if not flag:
#                     p.exist = True
#                 print 'create success!'
#                 return HttpResponse(status=1)
#             except Exception, e:
#                 print e
#                 return HttpResponse(status=0)
#     else:  # 当正常访问时
#         print 'not post'


# 创建一个空的一级管理员


def post_manager_delete(request):
    if request.method == 'POST':  # 当提交表单时
        form = ManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['id']
                p = manager_delete(user)
                if p:
                    print 'delete success!'
                    return JsonResponse(success)
                else:
                    return JsonResponse(fail)
            except Exception, e:
                print e
                return JsonResponse(fail)
        else:
            return JsonResponse(fail)
    else:  # 当正常访问时
        return page_not_found(request)


# 删除一个一级管理员


# code from here
def post_manager_logout(request):
    if request.method == 'POST':  # 当提交表单时
        form = ManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            user = form.cleaned_data['id']
            p = manager_logout(user)
            if p:
                return JsonResponse(success)
            else:
                return JsonResponse(fail)
        else:
            return JsonResponse(fail)
    else:
        return page_not_found(request)
# 管理员登出


def post_manager_active(request):
    if request.method == 'POST':  # 当提交表单时
        form = ManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['id']
                p = manager_active(user)
                if p:
                    return JsonResponse(success)
                else:
                    return JsonResponse(fail)
            except Exception, e:
                print e
                return JsonResponse(fail)
        else:
            return JsonResponse(fail)
    else:
        print 'not post'
        return page_not_found(request)
# 激活一个管理员账号


def post_manager_pw(request):
    if request.method == 'POST':
        form = ManagerPwdChange(request.POST)
        if form.is_valid():
            try:
                user = form.cleaned_data['manager_account']
                oldpw = form.cleaned_data['manager_oldpw']
                newpw = form.cleaned_data['manager_newpw']
                p = manager_pw(user, oldpw, newpw)
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return HttpResponse(status=0)
    else:
        print 'not post'


def mansion_keeper_add(request):
    return post_second_manager_add(request, 'mansion')


def mansion_keeper_modify(request):
    return post_second_manager_modify(request, 'mansion')


def wuye_add(request):
    return post_second_manager_add(request, 'wuye')


def wuye_modify(request):
    return post_second_manager_modify(request, 'wuye')


def post_second_manager_add(request, status):
    if request.method == 'POST':  # 当提交表单时
        form = SecondManagerForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                manager = form.cleaned_data['second_manager_manager']
                user = form.cleaned_data['second_manager_account']
                pw = form.cleaned_data['second_manager_pw']
                name = form.cleaned_data['second_manager_name']
                phone = form.cleaned_data['second_manager_phone']
                company = form.cleaned_data['second_manager_company']
                p = second_manager_add(manager, user, pw, name, phone, company, status)
                if p:
                    return JsonResponse(success)
                else:
                    return JsonResponse(rename)
            except Exception, e:
                print e
                return JsonResponse(not_valid)
        else:
            return JsonResponse(not_valid)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_second_manager_modify(request, status):
    if request.method == 'POST':  # 当提交表单时
        form = SecondManagerForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                manager = form.cleaned_data['second_manager_manager']
                user = form.cleaned_data['second_manager_account']
                pw = form.cleaned_data['second_manager_pw']
                name = form.cleaned_data['second_manager_name']
                phone = form.cleaned_data['second_manager_phone']
                company = form.cleaned_data['second_manager_company']
                p = second_manager_modify(manager, user, pw, name, phone, company, status)
                if p:
                    return JsonResponse(success)
                else:
                    return JsonResponse(not_exist)
            except Exception, e:
                print e
                return JsonResponse(not_valid)
        else:
            return JsonResponse(not_valid)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def wuye_search(request):
    try:
        return second_manager_search(request, 'wuye')
    except Exception, e:
        print e
        return JsonResponse(fail)


def mansion_keeper_search(request):
    try:
        return second_manager_search(request, 'mansion')
    except Exception, e:
        print e
        return JsonResponse(fail)


def second_manager_search(request, status):
    company = request.GET.get('second_manager_search_company', "")
    wuye_list = SecondManager.objects.filter(company__icontains=company,
                                             status=status)
    wuye_list = serializers.serialize('json', wuye_list)
    result = {'code': 1,
              'context': wuye_list}
    return JsonResponse(result, safe=False)
#
#
# def post_second_manager_add(request):
#     if request.method == 'POST':  # 当提交表单时
#         form = SecondManagerForm(request.POST)  # form 包含提交的数据
#         if form.is_valid():  # 如果提交的数据合法
#             try:
#                 manager = form.cleaned_data['second_manager_manager']
#                 user = form.cleaned_data['second_manager_user']
#                 pw = form.cleaned_data['second_manager_pw']
#                 name = form.cleaned_data['second_manager_name']
#                 phone = form.cleaned_data['second_manager_phone']
#                 company = form.cleaned_data['second_manager_company']
#                 status = form.cleaned_data['second_manager_status']
#                 p = second_manager_add(manager, user, pw, name, phone, company, status)
#                 return HttpResponse(status=1)
#             except Exception, e:
#                 print e
#                 return HttpResponse(status=0)
#     else:  # 当正常访问时
#         print 'not post'


# 添加一个二级管理员
#
#
# def post_second_manager_modify(request):
#     if request.method == 'POST':  # 当提交表单时
#         form = SecondManagerForm(request.POST)  # form 包含提交的数据
#         if form.is_valid():  # 如果提交的数据合法
#             try:
#                 user = form.cleaned_data['second_manager_user']
#                 pw = form.cleaned_data['second_manager_pw']
#                 name = form.cleaned_data['second_manager_name']
#                 phone = form.cleaned_data['second_manager_phone']
#                 company = form.cleaned_data['second_manager_company']
#                 status = form.cleaned_data['second_manager_status']
#                 p = second_manager_modify(user, pw, name, phone, company, status)
#                 return HttpResponse(status=1)
#             except Exception, e:
#                 print e
#                 return HttpResponse(status=0)
#     else:  # 当正常访问时
#         print 'not post'
#
#
# 修改一个二级管理员


def post_second_manager_delete(request):
    if request.method == 'POST':  # 当提交表单时
        form = SecondManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['id']
                p = SecondManager.objects.get(user=user)
                p.delete()
                print 'delete success!'
                return JsonResponse(success)
            except Exception, e:
                print e
                return JsonResponse(fail)
        else:
            return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


# 删除一个二级管理员


def post_second_manager_logout(request):
    if request.method == 'POST':  # 当提交表单时
        form = SecondManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['id']
                p = second_manager_logout(user)
                if p:
                    return JsonResponse(success)
                else:
                    return JsonResponse(fail)
            except Exception, e:
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_second_manager_active(request):
    if request.method == 'POST':  # 当提交表单时
        form = SecondManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['id']
                p = second_manager_active(user)
                if p:
                    return JsonResponse(success)
                else:
                    return JsonResponse(fail)
            except Exception, e:
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_second_manager_pw(request):
    if request.method == 'POST':
        form = SecondManagerPwdChange(request.POST)
        if form.is_valid():
            try:
                user = form.cleaned_data['second_manager_account']
                oldpw = form.cleaned_data['second_manager_oldpw']
                newpw = form.cleaned_data['second_manager_newpw']
                p = second_manager_pw(user, oldpw, newpw)
                if p:
                    print 'password modify success!'
                    return JsonResponse(success)
                else:
                    print 'password modify fail!'
                    return JsonResponse(fail)
            except Exception, e:
                print e
                return JsonResponse(fail)
        else:
            return JsonResponse(fail)
    else:
        print 'not post'
        return page_not_found(request)


def upload_image(request):
    img_water = "./zhiwu/static/water.png"
    if request.method == 'POST':
        try:
            image = request.FILES['imageDate']
            folder = time.strftime('%Y%m')
            if not os.path.exists(settings.MEDIA_ROOT + "upload/" + folder):
                os.mkdir(settings.MEDIA_ROOT + "upload/" + folder)
            file_name = time.strftime('%Y%m%d%H%M%S')+str(random.randint(000, 999))
            file_ext = image.name.split('.')[-1]
            file_addr = settings.MEDIA_ROOT+"upload/" + folder + "/" + file_name + "." + file_ext
            destination = open(file_addr, 'wb+')
            for chunk in image.chunks():
                destination.write(chunk)
            destination.close()
            watermark(file_addr, img_water, file_addr, 250, 50)
            result = {
                'files': [{
                    'url': "/media/upload/" + folder + "/" + file_name + "." + file_ext,
                    'thumbnailUrl': "/media/upload/" + folder + "/" + file_name + "." + file_ext,
                    'name': file_name+'.'+file_ext,
                    'size': image.size
                }]
            }
            return JsonResponse(result)
        except Exception, e:
            print "image upload error:"
            print e
            return HttpResponse(status=500)
    else:
        fb = ImageForm()
    return render(request, "home.html", {"r": fb})


def post_salehouse_save(request):
    p, num = post_salehouse_add_or_modify(request)
    if p:
        return JsonResponse(success)
    else:
        return JsonResponse(fail)


def post_salehouse_submit(request):
    p, num = post_salehouse_add_or_modify(request)
    if p:
        try:
            room = SaleHouse.objects.get(roomNumber=num)
            # room.achieve = True
            room.exist = True
            room.save()
            return JsonResponse(success)
        except Exception, e:
            print "post_salehouse_submit error:"
            print e
            return JsonResponse(fail)
    else:
        return JsonResponse(fail)


def post_salehouse_add_or_modify(request):
    if request.method == 'POST':
        try:
            manager = request.session.get('user', '')
            identity = request.session.get("identity", "")
            status = request.session.get("status", "")
            user = request.session.get("user", "")
            salehouse_default = {}
            url_list = []
            for key in request.POST:
                value = request.POST.getlist(key)
                if len(value) > 1:
                    value = ','.join(value)
                elif len(value) == 1:
                    value = value[0]
                else:
                    value = ''
                salehouse_default[str(key)] = value
            url_list = str(salehouse_default['imgUrl'])
            url_list = url_list.split('^_^')
            if '' in url_list:
                url_list.remove('')
            salehouse_default.pop('imgUrl')
            salehouse_default['have_image'] = len(url_list) != 0
            if 'roomNumber' not in salehouse_default:
                roomNumber = get_salehouseNumber()
                salehouse_default['roomNumber'] = roomNumber
            else:
                roomNumber = salehouse_default['roomNumber']
            if identity == 'second_manager':
                salehouse_default['contactPerson'] = manager
                salehouse_default['manager'] = SecondManager.objects.get(user=manager).manager.user
            test_list = ['addr_building', 'addr_unit', 'addr_room', 'price']
            for i in test_list:
                if salehouse_default[i] == '':
                    salehouse_default[i] = '0'
            add_or_modify_result = salehouse_add_or_modify(salehouse_default)
            if add_or_modify_result:
                salehouse_picture_remove(roomNumber)
                for i in url_list:
                    salehouse_picture_add(roomNumber, i)
                return True, roomNumber
            else:
                return False, None
        except Exception, e:
            print "post_roominfo_add_or_modify error:"
            print e
            return False, None
    else:
        return False, None


def post_salehouse_logout(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomShortForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['roomNumber']
                p = salehouse_logout(roomNumber)
                if p:
                    print 'logout success!'
                    return JsonResponse(success)
                else:
                    print 'logout fail'
                    return JsonResponse(fail)
            except Exception, e:
                print "salehouse logout error:"
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_salehouse_active(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomShortForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['roomNumber']
                p = salehouse_active(roomNumber)
                if p:
                    print 'active success!'
                    return JsonResponse(success)
                else:
                    print 'active fail!'
                    return JsonResponse(fail)
            except Exception, e:
                print 'active error:'
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_salehouse_sold(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomShortForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['roomNumber']
                p = salehouse_sold(roomNumber)
                if p:
                    print 'salehouse has been sold '
                    return JsonResponse(success)
                else:
                    return JsonResponse(fail)
            except Exception, e:
                print 'post salehouse sold error:'
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_roominfo_logout(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomShortForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['roomNumber']
                p = roominfo_logout(roomNumber)
                if p:
                    print 'logout success!'
                    return JsonResponse(success)
                else:
                    print 'logout fail'
                    return JsonResponse(fail)
            except Exception, e:
                print "roominfo logout error:"
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_roominfo_active(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomShortForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['roomNumber']
                p = roominfo_active(roomNumber)
                if p:
                    print 'active success!'
                    return JsonResponse(success)
                else:
                    print 'active fail!'
                    return JsonResponse(fail)
            except Exception, e:
                print 'active error:'
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_roominfo_save(request):
    p, num = post_roominfo_add_or_modify(request)
    if p:
        return JsonResponse(success)
    else:
        return JsonResponse(fail)


def post_roominfo_submit(request):
    p, num = post_roominfo_add_or_modify(request)
    if p:
        try:
            room = RoomInfo.objects.get(roomNumber=num)
            # room.achieve = True
            room.exist = True
            room.save()
            return JsonResponse(success)
        except Exception, e:
            print "post_roominfo_submit error:"
            print e
            return JsonResponse(fail)
    else:
        return JsonResponse(fail)


def post_roominfo_add_or_modify(request):
    i = request.POST.get('payway', [])
    print len(i)
    if request.method == 'POST':
        try:
            manager = request.session.get('user', '')
            identity = request.session.get("identity", "")
            status = request.session.get("status", "")
            user = request.session.get("user", "")
            roominfo_default = {}
            url_list = []
            for key in request.POST:
                value = request.POST.getlist(key)
                if len(value) > 1:
                    value = ','.join(value)
                elif len(value) == 1:
                    value = value[0]
                else:
                    value = ''
                roominfo_default[str(key)] = value
            url_list = str(roominfo_default['imgUrl'])
            url_list = url_list.split('^_^')
            if '' in url_list:
                url_list.remove('')
            roominfo_default.pop('imgUrl')
            roominfo_default['have_image'] = len(url_list) != 0
            if 'roomNumber' not in roominfo_default:
                roomNumber = get_roomNumber()
                roominfo_default['roomNumber'] = roomNumber
            else:
                roomNumber = roominfo_default['roomNumber']
            if identity == 'second_manager':
                roominfo_default['contactPerson'] = manager
                roominfo_default['manager'] = SecondManager.objects.get(user=manager).manager.user
            test_list = ['addr_building', 'addr_unit', 'addr_room', 'addr_room', 'price', 'mianji']
            for i in test_list:
                if roominfo_default[i] == '':
                    roominfo_default[i] = '0'
            add_or_modify_result = roominfo_add_or_modify(roominfo_default)
            if add_or_modify_result:
                room_picture_remove(roomNumber)
                for i in url_list:
                    room_picture_add(roomNumber, i)
                return True, roomNumber
            else:
                return False, None
        except Exception, e:
            print "post_roominfo_add_or_modify error:"
            print e
            return False, None
    else:
        return False, None


def post_roominfo_sold(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomShortForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['roomNumber']
                p = roominfo_sold(roomNumber)
                if p:
                    print 'room has been sold '
                    return JsonResponse(success)
                else:
                    return JsonResponse(fail)
            except Exception, e:
                print 'post roominfo sold error:'
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


# todo 缺少考虑情况不太对，先这样这把


def roominfo_addr_search(request):
    try:
        return roominfo_addr_search_handle(request)
    except Exception, e:
        print e
        return JsonResponse(fail)


def roominfo_addr_search_handle(request):
    identity = request.session.get("identity", "")
    status = request.session.get("status", "")
    user = request.session.get("user", "")
    addr_xiaoqu = request.GET.get('addr_xiaoqu', '')
    addr_building = request.GET.get('addr_building', '')
    addr_unit = request.GET.get('addr_unit', '')
    addr_room = request.GET.get('addr_room', '')
    addr_floor = request.GET.get('addr_floor', '')
    rooms = RoomInfo.objects.filter(addr_xiaoqu=addr_xiaoqu,
                                    addr_building=addr_building,
                                    addr_unit=addr_unit,
                                    addr_room=addr_room,
                                    addr_floor=addr_floor).order_by('-roomNumber')
    if len(rooms) == 0:
        return JsonResponse(fail)
    else:
        room = rooms[0]
        if room.sold:
            sts = 1
        elif room.exist:
            sts = 0
        else:
            return JsonResponse(fail)
        return JsonResponse({'code': 1,
                             'status': sts,
                             'sm': room.contactPerson,
                             'roomNumber': room.roomNumber})


def salehouse_addr_search(request):
    try:
        return salehouse_addr_search_handle(request)
    except Exception, e:
        print e
        return JsonResponse(fail)


def salehouse_addr_search_handle(request):
    identity = request.session.get("identity", "")
    status = request.session.get("status", "")
    user = request.session.get("user", "")
    addr_xiaoqu = request.GET.get('addr_xiaoqu', '')
    addr_building = request.GET.get('addr_building', '')
    addr_unit = request.GET.get('addr_unit', '')
    addr_room = request.GET.get('addr_room', '')
    rooms = SaleHouse.objects.filter(addr_xiaoqu=addr_xiaoqu,
                                     addr_building=addr_building,
                                     addr_unit=addr_unit,
                                     addr_room=addr_room).order_by('-roomNumber')
    if len(rooms) == 0:
        return JsonResponse(fail)
    else:
        room = rooms[0]
        if room.sold:
            sts = 1
        elif room.exist:
            sts = 0
        else:
            return JsonResponse(fail)
        return JsonResponse({'code': 1,
                             'status': sts,
                             'sm': room.contactPerson,
                             'roomNumber': room.roomNumber})


def salehouse_search_except(request):
    try:
        return room_search(request, True)
    except Exception, e:
        print 'salehouse search error:'
        print e
        return JsonResponse(fail)


def room_search_except(request):
    try:
        return room_search(request, False)
    except Exception, e:
        print 'room search error:'
        print e
        return JsonResponse(fail)


def room_search(request, issalehouse):
    # todo 需要扩大
    page_num = 1
    house_status = request.GET.get('house_status', 'no')  # no active cancel
    house_area = request.GET.get('house_area', 'no')  # no , xxxx
    page = int(request.GET.get('p', 1))
    if house_status == 'no':
        if house_area == 'no':
            if issalehouse:
                rooms = SaleHouse.objects.filter(exist=True).order_by('-roomNumber')
            else:
                rooms = RoomInfo.objects.filter(exist=True).order_by('-roomNumber')
            count = rooms.count()
            rooms = rooms[page*page_num-page_num:page*page_num]
        else:
            ms = Manager.objects.filter(district=house_area)
            sms = SecondManager.objects.filter(manager__in=ms)
            sms_list = []
            for i in sms:
                sms_list.append(i.user)
            if issalehouse:
                rooms = SaleHouse.objects.filter(contactPerson__in=sms_list).order_by('-roomNumber')
            else:
                rooms = RoomInfo.objects.filter(contactPerson__in=sms_list).order_by('-roomNumber')
            count = rooms.count()
            rooms = rooms[page*page_num-page_num:page*page_num]
    elif house_status == 'active':
        if house_area == 'no':
            if issalehouse:
                rooms = SaleHouse.objects.filter(exist=True, sold=False).order_by('-roomNumber')
            else:
                rooms = RoomInfo.objects.filter(exist=True, sold=False).order_by('-roomNumber')
            count = rooms.count()
            rooms = rooms[page*page_num-page_num:page*page_num]
        else:
            ms = Manager.objects.filter(district=house_area)
            sms = SecondManager.objects.filter(manager__in=ms)
            sms_list = []
            for i in sms:
                sms_list.append(i.user)
            if issalehouse:
                rooms = SaleHouse.objects.filter(exist=True, sold=False, contactPerson__in=sms_list).order_by('-roomNumber')
            else:
                rooms = RoomInfo.objects.filter(exist=True, sold=False, contactPerson__in=sms_list).order_by('-roomNumber')
            count = rooms.count()
            rooms = rooms[page*page_num-page_num:page*page_num]
    elif house_status == 'cancel':
        if house_area == 'no':
            if issalehouse:
                rooms = SaleHouse.objects.filter(sold=True).order_by('-roomNumber')
            else:
                rooms = RoomInfo.objects.filter(sold=True).order_by('-roomNumber')
            count = rooms.count()
            rooms = rooms[page*page_num-page_num:page*page_num]
        else:
            ms = Manager.objects.filter(district=house_area)
            sms = SecondManager.objects.filter(manager__in=ms)
            sms_list = []
            for i in sms:
                sms_list.append(i.user)
            if issalehouse:
                rooms = SaleHouse.objects.filter(sold=True, contactPerson__in=sms_list).order_by('-roomNumber')
            else:
                rooms = RoomInfo.objects.filter(sold=True, contactPerson__in=sms_list).order_by('-roomNumber')
            count = rooms.count()
            rooms = rooms[page*page_num-page_num:page*page_num]
    else:
        return page_not_found(request)
    rooms = serializers.serialize('json', rooms)
    result = {'code': 1,
              'context': rooms,
              'count': count}
    return JsonResponse(result, safe=True)


def post_evaluation_add(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomEvaluationForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['roomNumber']
                text = form.cleaned_data['text']
                issalehouse = request.POST.get('issalehouse', 'False')
                p = evaluation_add(roomNumber, text, issalehouse)
                if p:
                    print 'evaluation success'
                    return JsonResponse(success)
                else:
                    print 'evaluation fail'
                    return JsonResponse(fail)
            except Exception, e:
                print 'evaluation error:'
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_evaluation_pass(request):
    if request.method == 'POST':
        form = RoomEvaluationForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                e_id = form.cleaned_data['id']
                issalehouse = request.POST.get('issalehouse', 'False')
                p = evaluation_pass(e_id, issalehouse)
                if p:
                    print 'evaluation pass success'
                    return JsonResponse(success)
                else:
                    print 'evaluation pass fail'
                    return JsonResponse(fail)
            except Exception, e:
                print 'evaluation pass error:'
                print e
                return JsonResponse(fail)
    else:
        print 'not post'
        return page_not_found(request)


def post_evaluation_no_pass(request):
    if request.method == 'POST':
        form = RoomEvaluationForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                e_id = form.cleaned_data['id']
                issalehouse = request.POST.get('issalehouse', 'False')
                p = evaluation_no_pass(e_id, issalehouse)
                if p:
                    print 'evaluation no pass success'
                    return JsonResponse(success)
                else:
                    print 'evaluation no pass fail'
                    return JsonResponse(fail)
            except Exception, e:
                print 'evaluation no pass error:'
                print e
                return JsonResponse(fail)
    else:
        print 'not post'
        return page_not_found(request)


def post_evaluation_delete(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomEvaluationForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                e_id = form.cleaned_data['id']
                issalehouse = request.POST.get('issalehouse', 'False')
                p = evaluation_delete(e_id, issalehouse)
                if p:
                    print 'evaluation success'
                    return JsonResponse(success)
                else:
                    print 'evaluation fail'
                    return JsonResponse(fail)
            except Exception, e:
                print 'evaluation error:'
                print e
                return JsonResponse(fail)
    else:  # 当正常访问时
        print 'not post'
        return page_not_found(request)


def post_evaluation_search(request):
    try:
        page = int(request.GET.get('p', 1))
        issalehouse = request.GET.get('issalehouse', 'false')
        if issalehouse.lower() == 'true':
            e = SaleHouseEvaluation.objects.order_by('-createTime')[page*10-10:page*10]
            count = SaleHouseEvaluation.objects.count()
        else:
            e = RoomEvaluation.objects.order_by('-createTime')[page*10-10:page*10]
            count = RoomEvaluation.objects.count()
        e = serializers.serialize('json', e)
        result = {'code': 1,
                  'count': count,
                  'context': e}
        return JsonResponse(result, safe=False)
    except Exception, e:
        print 'post evaluation search error:'
        print e
        return JsonResponse(fail)


# 增加一条小区信息
def post_community_add(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            manager = form.cleaned_data['xiaoqu_add_manager']
            name = form.cleaned_data['xiaoqu_add_name']
            lng = form.cleaned_data['xiaoqu_add_lng']
            lat = form.cleaned_data['xiaoqu_add_lat']
            # area = form.cleaned_data['xiaoqu_add_area']
            # district = form.cleaned_data['xiaoqu_add_district']
            business = form.cleaned_data['xiaoqu_add_business']
            keyword = form.cleaned_data['xiaoqu_add_keyword']
            type_ = form.cleaned_data['xiaoqu_add_type']
            year = form.cleaned_data['xiaoqu_add_year']
            level = form.cleaned_data['xiaoqu_add_level']
            # facility = form.cleaned_data['xiaoqu_add_facility']
            # green = form.cleaned_data['xiaoqu_add_green']
            security = form.cleaned_data['xiaoqu_add_security']
            p = community_add_or_modify(name, manager, lng, lat, business,
                                        keyword, type_, year, level, security)
            if p:
                return JsonResponse(success)
            else:
                return JsonResponse(fail)
        else:
            return JsonResponse(fail)
    else:
        return page_not_found(request)


# 小区查询，返回一个jason 列表
def post_community_search(request):
    try:
        kw = request.GET.get('xiaoqu_search_name', '')
        c_list = get_community_list(kw)
        c_list = serializers.serialize('json', c_list)
        result = {'code': 1,
                  'context': c_list}
        return JsonResponse(result, safe=False)
    except Exception, e:
        print e
        return JsonResponse(fail)


# 小区删除
def post_community_delete(request):
    if request.method == "POST":
        form = CommunityDeleteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["id"]
            p = community_delete(name)
            if p:
                return JsonResponse(success)
            else:
                return JsonResponse(fail)
        else:
            return JsonResponse(fail)
    else:
        return page_not_found(request)


def download_roominfo(request):
    file_name = 'data.xls'
    attri_list = ['roomNumber', 'manager', 'contactPerson', 'price', 'lng', 'lat',
                  'sold', 'exist', 'create_time', 'sold_time', 'have_image',
                  'orientation', 'balcony', 'mianji', 'addr_xiaoqu', 'addr_building',
                  'addr_unit', 'addr_room', 'addr_floor', 'payway', 'type_room',
                  'type_livingroom', 'type_toilet', 'stay_intime', 'see', 'floor_level',
                  'total_floor', 'elevator', 'canzhuo', 'sofa', 'desk', 'chair', 'closet',
                  'bed', 'aircon', 'washer', 'waterheater', 'refregister', 'tv', 'cookerhood',
                  'gascooker', 'original_house_shi', 'original_house_ting', 'original_house_wei',
                  'decorate_level', 'can_cook', 'merit', 'landlord_req', 'other',]
    attri_title = [u'房源编号', u'一级管理员', u'二级管理员/联系人', u'价格', u'经度', u'纬度',
                   u'是否被出售', u'是否上架', u'创建时间', u'售出时间', u'是否有照片',
                   u'方向', u'阳台', u'面积', u'小区名称', u'幢',
                   u'单元', u'室', u'房', u'付款方式', u'室',
                   u'厅', u'卫', u'入住时间', u'是否可看', u'楼层高低',
                   u'楼层数量', u'电梯', u'餐桌', u'沙发', u'书桌', u'椅子', u'衣柜',
                   u'床', u'空调', u'洗衣机', u'热水器', u'冰箱', u'电视机', u'油烟机',
                   u'燃气灶', u'原户型室', u'原户型厅', u'原户型卫',
                   u'装修档次', u'做饭情况', u'房屋优势', u'房东要求', u'其他描述']
    rs = RoomInfo.objects.all()
    w = Workbook()
    ws = w.add_sheet(u'房源信息')
    for i in range(len(attri_title)):
        ws.write(0, i, attri_title[i])
    i = 1
    for r in rs:
        j = 0
        for item in attri_list:
            ws.write(i, j, r.__getattribute__(item))
            j += 1
        i += 1
    w.save(file_name)
    response = StreamingHttpResponse(readfile(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


def download_salehouse(requset):
    file_name = 'data.xls'
    attri_lisattri_list = ['roomNumber', 'manager', 'contactPerson', 'price', 'lng', 'lat',
                  'sold', 'exist', 'create_time', 'sold_time', 'have_image'
                  'mianji', 'addr_xiaoqu', 'addr_building', 'addr_unit', 'addr_room', 'type_room',
                  'type_livingroom', 'type_toilet', 'type', 'orientation',
                  'floor_level', 'total_floor', 'maner', 'weiyi', 'house_desc']
    attri_title = [u'房源编号', u'一级管理员', u'二级管理员/联系人', u'价格', u'经度', u'纬度',
                   u'是否被出售', u'是否上架', u'创建时间', u'售出时间', u'是否有照片',
                   u'面积', u'小区名称', u'幢', u'单元', u'室', u'室',
                   u'厅', u'卫', u'房屋类型', u'朝向',
                   u'楼层高低', u'楼层数', u'产证满二', u'唯一住房', u'房源描述']
    rs = SaleHouse.objects.all()
    w = Workbook()
    ws = w.add_sheet(u'房源信息')
    for i in range(len(attri_title)):
        ws.write(0, i, attri_title[i])
    i = 1
    for r in rs:
        j = 0
        for item in attri_list:
            ws.write(i, j, r.__getattribute__(item))
            j += 1
        i += 1
    w.save(file_name)
    response = StreamingHttpResponse(readfile(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response
