# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
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


def test(request):
    if request.method == "POST":
        print 1
    else:
        ff = RoomForm()
    return render(request, "home.html", {"ff": ff})

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
    return render(request, "detail.html")


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
    return render(request, "admin_login.html")


def admin_root(request):
    return render(request, "backend.html")


def admin_manager(request):
    return render(request, "backendL1.html")


def admin_second_manager(request):
    return render(request, "backendL2.html")

def new_house(request):
    return render(request, "newHouse.html")

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


def mapsearch(request):
    return render(request, "")


def mapsearch(request):
    return render(request, "")


def mapsearch(request):
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
                return HttpResponse(status=1)
            except Exception, e:
                print e
                return HttpResponse(status=0)

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
                return HttpResponse(p)
            except Exception, e:
                print e
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
            except Exception, e:
                print e
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
            except Exception, e:
                print e
    else:  # 当正常访问时
        print 'not post'
# 删除一个一级管理员


def post_manager_logout(request):
    return render(request, "")


def post_manager_active(request):
    return render(request, "")


def post_manager_pw(request):
    return render(request, "")


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
                return HttpResponse(p)
            except Exception, e:
                print e
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
                return HttpResponse(p)
            except Exception, e:
                print e
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
            except Exception, e:
                print e
    else:  # 当正常访问时
        print 'not post'
# 删除一个二级管理员


def post_second_manager_logout(request):
    return render(request, "")


def post_second_manager_active(request):
    return render(request, "")


def post_second_manager_pw(request):
    return render(request, "")


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
    return render(request, "")


def post_room_active(request):
    return render(request, "")


def post_room_save(request):
    return render(request, "")


def post_room_sub(request):
    return render(request, "")


def post_room_sold(request):
    return render(request, "")