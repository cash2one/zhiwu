# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from .forms import *
from .help import *
from zhiwu.models import *
import json
import time
import os
# Create your views here.

success = 1
fault = 0


def home(request):
    return render(request, "index.html")


# def home(request):
#     # room = ManagerForm()
#     r = {"user": 2, "kk":3}
#     # return HttpResponseRedirect("admin_manager")
#
#     return render(request, "detail.html", {"r": json.dumps(r)})
#     # return HttpResponse("hello world",status=200)


def work_search(request):
    return render(request, "search.html")


def home_search(request):
    return render(request, "search.html")


def room_detail(request):
    try:
        roomNum = request.GET.get('roomNumber')
        room = Room.objects.get(roomNumber = roomNum)
        roomP = get_room_picture(room)
        roomC = get_room_configuration(room)
        roomD = get_room_description(room)
        roomE = get_room_evaluation(room)
        environ = get_environment(room.environment)
        return render(request, "detail.html", {"room": room,
                                               "picture": roomP,
                                               "configuration": roomC,
                                               "description": roomD,
                                               "evaluation": roomE,
                                               "ecvironment": environ})
    except Exception, e:
        print e
        return HttpResponse(status=404)


def admin_manager_login(request):
    if request.method == "POST":
        form = AdminLogin(request.POST)
        if form.is_valid():
            try:
                user = form.cleaned_data['login_user']
                pw = form.cleaned_data['login_pw']
                status = form.cleaned_data['login_type']
                if status == "manager":
                    tag, m = get_manager(user, pw)
                elif status == "second_manager":
                    tag, m = get_second_manager(user, pw)
                elif status == "root":
                    request.session['user'] = "root"
                    request.session['status'] = "root"
                    return HttpResponseRedirect("admin_manager/")
                    # todo 完善root的数据库
                else:
                    return HttpResponse(status=-1)
                    # 身份不正确
                if tag:
                    request.session['user'] = m.user
                    request.session['status'] = m.status
                    if m.status == "manager":
                        return HttpResponseRedirect("admin_manager/")
                    else:
                        return HttpResponseRedirect("admin_second_manager/")
                else:
                    return HttpResponse(status=0)
                    # 账号密码错误
            except Exception, e:
                print e
    return render(request, "manager_login.html")


def admin_login(request):
    return render(request, "index.html")


def admin_root(request):
    status = request.session.get("status", "")
    user = request.session.get("user", "")
    if is_root(status):
        m_list = get_manager_list()
        return render(request, "backend.html", {"managers": m_list,
                                                "status": status,
                                                "user": user})
    else:
        return HttpResponseRedirect(reverse("manager_login"))


def admin_manager(request):
    managerget = request.GET.get("manager", "")
    status = request.session.get("status", "")
    user = request.session.get("user", "")
    if is_manager(status):
        mu = request.session.get("user", "")
    elif is_root(status) and managerget != "":
        mu = managerget
    else:
        return HttpResponseRedirect(reverse("manager_login"))
    try:
        manager = Manager.objects.get(user=mu)
    except:
        return HttpResponseRedirect(reverse("manager_login"))
    m_list = get_second_manager_list(manager)
    return render(request, "backendL1.html", {"second_managers": m_list,
                                              "status": status,
                                              "user": user})


def admin_second_manager(request):
    secondmanagerget = request.GET.get("second_manager", "")
    status = request.session.get("status", "")
    user = request.session.get("user", "")
    if is_second_manager(status):
        smu = request.session.get("user", "")
    elif (is_root(status) or is_manager(status)) and secondmanagerget != "":
        smu = secondmanagerget
    else:
        return HttpResponseRedirect(reverse("manager_login"))
    rooms = Room.objects.filter(contactPerson=smu)
    return render(request, "backendL2.html", {"second_managers": rooms,
                                              "status": status,
                                              "user": user})


def new_house(request):
    user = request.session.get("user")
    status = request.session.get("status", "")
    if is_second_manager(status):
        return render(request, "newHouse.html", {"user": user})
    else:
        return HttpResponseRedirect(reverse("manager_login"))


def client_back(request):
    return render(request, "clientBackend.html")


def client_back_account(request):
    return render(request, "myAccount.html")


def client_back_list(request):
    return render(request, "mylist.html")


def client_back_comment(request):
    return render(request, "serviceContact.html")


def map_search(request):
    return render(request, "")


def room_collection(request):
    return render(request, "")


# post
# JianDing


def manager_search(request):
    user = request.GET.get('manager_search_account', None)
    name = request.GET.get('manager_search_name', None)
    phone = request.GET.get('manager_search_phone', None)
    result = Manager.objects.filter(user__icontains=user,
                                    name__icontains=name,
                                    phone__icontains=phone,
                                    exist=True)
    # todo

#code from here
def post_manager_add(request):
    if request.method == 'POST':  # 当提交表单时
        form = ManagerForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['manager_account']
                pw = form.cleaned_data['manager_pw']
                name = form.cleaned_data['manager_name']
                phone = form.cleaned_data['manager_phone']
                status = form.cleaned_data['manager_status']
                district = form.cleaned_data['manager_district']
                p = manager_add(user, pw, name, phone, status, district)
                return HttpResponse(p)
            except Exception, e:
                print e
    else:  # 当正常访问时
        print 'not post'
# 添加一条一级管理员


def post_manager_modify(request):
    if request.method == 'POST':  # 当提交表单时
        form = ManagerForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['manager_account']
                pw = form.cleaned_data['manager_pw']
                name = form.cleaned_data['manager_name']
                phone = form.cleaned_data['manager_phone']
                status = form.cleaned_data['manager_status']
                district = form.cleaned_data['manager_district']
                p = manager_modify(user, pw, name, phone, status, district)
                print 'modify success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'
# 修改一条一级管理员


def post_manager_create(request):
    if request.method == 'POST':  # 当提交表单时
        form = ManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['manager_account']
                p, flag = Manager.objects.get_or_create(user=user)
                if not flag:
                    p.exist = True
                print 'create success!'
                return HttpResponse(status=1)  #add return
            except Exception, e:
                print e
                return HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'
# 创建一个空的一级管理员


def post_manager_delete(request):
    if request.method == 'POST':  # 当提交表单时
        form = ManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['manager_account']
                p = Manager.objects.get(user=user)
                p.delete()
                print 'delete success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'

# 删除一个一级管理员

#code from here
def post_manager_logout(request):
     if request.method == 'POST':  # 当提交表单时
        form = ManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['manager_account']
                p=manager_logout(user)
                print 'logout success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return HttpResponse(status=0)
     else:
         print 'not post'
#管理员登出


def post_manager_active(request):
        if request.method == 'POST':  # 当提交表单时
            form = ManagerUserForm(request.POST)  # form 包含提交的数据
            if form.is_valid():  # 如果提交的数据合法
                try:
                    user = form.cleaned_data['manager_account']
                    p=manager_active(user)
                    print 'active success!'
                    return HttpResponse(status=1)
                except Exception, e:
                    print e
                    return HttpResponse(status=0)
        else:
            print 'not post'
#激活一个管理员账号



def post_manager_pw(request):
    if request.method == 'POST':
        form = ManagerPwdChange(request.POST)
        if form.is_valid():
            try:
                user = form.cleaned_data['manager_account']
                oldpw = form.cleaned_data['manager_oldpw']
                newpw = form.cleaned_data['manager_newpw']
                p = manager_pw(user, oldpw, newpw)
                print 'password modify success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:
        print 'not post'



def post_second_manager_add(request):
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
                status = form.cleaned_data['second_manager_status']
                p = second_manager_add(manager, user, pw, name, phone, company, status)
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'
# 添加一个二级管理员


def post_second_manager_modify(request):
    if request.method == 'POST':  # 当提交表单时
        form = SecondManagerForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['second_manager_account']
                pw = form.cleaned_data['second_manager_pw']
                name = form.cleaned_data['second_manager_name']
                phone = form.cleaned_data['second_manager_phone']
                company = form.cleaned_data['second_manager_company']
                status = form.cleaned_data['second_manager_status']
                p = second_manager_modify(user, pw, name, phone, company, status)
                print 'modify success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'
# 修改一个二级管理员


def post_second_manager_delete(request):
    if request.method == 'POST':  # 当提交表单时
        form = SecondManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['second_manager_account']
                p = SecondManager.objects.get(user=user)
                p.delete()
                print 'delete success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'
# 删除一个二级管理员


def post_second_manager_logout(request):
    if request.method == 'POST':  # 当提交表单时
        form = SecondManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['second_manager_account']
                p = second_manager_logout(user)
                print 'logout success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'


def post_second_manager_active(request):
    if request.method == 'POST':  # 当提交表单时
        form = SecondManagerUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['second_manager_account']
                p = second_manager_active(user)
                print 'active success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'



def post_second_manager_pw(request):
    if request.method == 'POST':
        form = SecondManagerPwdChange(request.POST)
        if form.is_valid():
            try:
                user = form.cleaned_data['second_manager_account']
                oldpw = form.cleaned_data['second_manager_oldpw']
                newpw = form.cleaned_data['second_manager_newpw']
                p = second_manager_pw(user, oldpw, newpw)
                print 'password modify success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:
        print 'not post'


def upload_image(request):
    if request.method == 'POST':
        try:
            image = request.FILES['imageDate']
            folder = time.strftime('%Y%m')
            if not os.path.exists(settings.MEDIA_ROOT+"upload/"+folder):
                os.mkdir(settings.MEDIA_ROOT+"upload/"+folder)
            file_name = time.strftime('%Y%m%d%H%M%S')
            file_ext = image.name.split('.')[-1]
            file_addr = settings.MEDIA_ROOT+"upload/"+folder+"/"+file_name+"."+file_ext
            destination = open(file_addr, 'wb+')
            for chunk in image.chunks():
                destination.write(chunk)
            destination.close()
            return HttpResponse(file_addr)
        except Exception, e:
            print "image upload error:"
            print e
            return HttpResponse(status=500)
    else:
        fb = ImageForm()
    return render(request, "home.html", {"r": fb})


def post_room_logout(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['room_roomNumber']
                p = room_logout(roomNumber)
                print 'logout success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'



def post_room_active(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['room_roomNumber']
                p = room_active(roomNumber)
                print 'active success!'
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'


def post_room_save(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['room_roomNumber']
                #房屋信息
                room_longitude = form.cleaned_data['room_longitude']
                room_latitude = form.cleaned_data['room_latitude']
                room_community = form.cleaned_data['room_community']
                room_shi = form.cleaned_data['room_shi']
                room_ting = form.cleaned_data['room_ting']
                room_wei = form.cleaned_data['room_wei']
                room_rent = form.cleaned_data['room_rent']
                room_area = form.cleaned_data['room_area']
                room_direction = form.cleaned_data['room_direction']
                room_DateToLive = form.cleaned_data['room_DateToLive']
                room_lookAble = form.cleaned_data['lookAble']
                room_contactPerson = form.cleaned_data['room_contactPerson']
                room_environment = form.cleaned_data['room_environment']
                 #出租信息
                rentDate = form.cleaned_data['rentDate']
                #房屋图片
                picture = form.cleaned_data['picture']
                #房屋配置
                level = form.cleaned_data['level']
                elevator = form.cleaned_data['elevator']
                canZhuo = form.cleaned_data['canZhuo']
                shaFa = form.cleaned_data['shaFa']
                shuZhuo = form.cleaned_data['shuZhuo']
                yiZi = form.cleaned_data['yiZi']
                yiGui = form.cleaned_data['yiGui']
                chuang = form.cleaned_data['chuang']
                kongTiao = form.cleaned_data['kongTiao']
                xiYiJi = form.cleaned_data['xiYiJi']
                reShuiQi = form.cleaned_data['reShuiQi']
                bingXiang = form.cleaned_data['bingXiang']
                dianShiJi = form.cleaned_data['dianShiJi']
                xiYouYanJi = form.cleaned_data['xiYouYanJi']
                ranQiZao = form.cleaned_data['ranQiZao']
                #房屋描述
                roomType = form.cleaned_data['roomType']
                decoration = form.cleaned_data['decoration']
                configuration = form.cleaned_data['configuration']
                cook = form.cleaned_data['cook']
                light = form.cleaned_data['light']
                wind = form.cleaned_data['wind']
                sound = form.cleaned_data['sound']
                requirement = form.cleaned_data['requirement']
                suitable = form.cleaned_data['suitable']
                p = room_save(roomNumber,room_longitude,room_latitude,room_community,room_shi,\
                             room_ting, room_wei,room_rent,room_area,room_direction,room_DateToLive,\
                              room_lookAble,room_contactPerson,room_environment,rentDate,picture,\
                        level,elevator,canZhuo,shaFa,shuZhuo,yiZi,yiGui,chuang,kongTiao,xiYiJi,reShuiQi,\
                        bingXiang,dianShiJi,xiYouYanJi,ranQiZao,roomType,decoration,configuration,cook,\
                        light,wind,sound,requirement,suitable)
                print 'room info is saved '
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'



def post_room_sub(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['room_roomNumber']
                #房屋信息
                room_longitude = form.cleaned_data['room_longitude']
                room_latitude = form.cleaned_data['room_latitude']
                room_community = form.cleaned_data['room_community']
                room_shi = form.cleaned_data['room_shi']
                room_ting = form.cleaned_data['room_ting']
                room_wei = form.cleaned_data['room_wei']
                room_rent = form.cleaned_data['room_rent']
                room_area = form.cleaned_data['room_area']
                room_direction = form.cleaned_data['room_direction']
                room_DateToLive = form.cleaned_data['room_DateToLive']
                room_lookAble = form.cleaned_data['lookAble']
                room_contactPerson = form.cleaned_data['room_contactPerson']
                room_environment = form.cleaned_data['room_environment']
                 #出租信息
                rentDate = form.cleaned_data['rentDate']
                #房屋图片
                picture = form.cleaned_data['picture']
                #房屋配置
                level = form.cleaned_data['level']
                elevator = form.cleaned_data['elevator']
                canZhuo = form.cleaned_data['canZhuo']
                shaFa = form.cleaned_data['shaFa']
                shuZhuo = form.cleaned_data['shuZhuo']
                yiZi = form.cleaned_data['yiZi']
                yiGui = form.cleaned_data['yiGui']
                chuang = form.cleaned_data['chuang']
                kongTiao = form.cleaned_data['kongTiao']
                xiYiJi = form.cleaned_data['xiYiJi']
                reShuiQi = form.cleaned_data['reShuiQi']
                bingXiang = form.cleaned_data['bingXiang']
                dianShiJi = form.cleaned_data['dianShiJi']
                xiYouYanJi = form.cleaned_data['xiYouYanJi']
                ranQiZao = form.cleaned_data['ranQiZao']
                #房屋描述
                roomType = form.cleaned_data['roomType']
                decoration = form.cleaned_data['decoration']
                configuration = form.cleaned_data['configuration']
                cook = form.cleaned_data['cook']
                light = form.cleaned_data['light']
                wind = form.cleaned_data['wind']
                sound = form.cleaned_data['sound']
                requirement = form.cleaned_data['requirement']
                suitable = form.cleaned_data['suitable']
                p = room_sub(roomNumber,room_longitude,room_latitude,room_community,room_shi,\
                             room_ting, room_wei,room_rent,room_area,room_direction,room_DateToLive,\
                              room_lookAble,room_contactPerson,room_environment,rentDate,picture,\
                        level,elevator,canZhuo,shaFa,shuZhuo,yiZi,yiGui,chuang,kongTiao,xiYiJi,reShuiQi,\
                        bingXiang,dianShiJi,xiYouYanJi,ranQiZao,roomType,decoration,configuration,cook,\
                        light,wind,sound,requirement,suitable)
                print 'room info is submitted '
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'


def post_room_sold(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['room_roomNumber']
                p = room_sold(roomNumber)
                print 'room has been sold '
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'

def post_room_evaluation(request):
    if request.method == 'POST':  # 当提交表单时
        form = RoomEvaluation(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                roomNumber = form.cleaned_data['room_roomNumber']
                creatTime = form.cleaned_data['creatTime']
                text = form.cleaned_data['text']
                p = room_evaluation(roomNumber,creatTime,text)
                print 'evaluation success '
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return  HttpResponse(status=0)
    else:  # 当正常访问时
        print 'not post'