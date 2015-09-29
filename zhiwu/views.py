# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import *
from .help import *
from zhiwu.models import *
# Create your views here.

success = 1
fault = 0


# def home(request):
#     if request.method == "POST":
#         uf = ManagerForm(request.POST)
#         if uf.is_valid():
#             #获取表单信息
#             im = uf.cleaned_data['image']
#             print "ok"
#             #写入数据库
#             # user = Image.objects.create(image=im)
#             return HttpResponse('upload ok!')
#     else:
#         uf = RoomForm()
#     return render(request, 'home.html', {"room": uf})


def home(request):
    room = ManagerForm()
    # return HttpResponseRedirect("admin_manager")

    return render(request, "backend.html", {"room": room})
    # return HttpResponse("hello world",status=200)

def search(request):
    return render(request, "search.html")


def room_detail(request):
    r = Room.objects.get(roomNumber='HZ10001')
    return render(request, "detail.html", {'R': r})


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
