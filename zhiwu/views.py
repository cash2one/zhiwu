# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from zhiwu.models import *
from .forms import *
# Create your views here.


def insert(request):
    Room.objects.create(roomNumber='HZ10001',
                        longitude=120.200,
                        latitude=30.300,
                        community='COMMUNITY',
                        shi=3,
                        ting=2,
                        wei=1,
                        rent=1500,
                        area=110,
                        direction='南',
                        level=7,
                        elevator=True,
                        DateToLive="2015-10-11",
                        lookAble=True,
                        contactPerson='Leon',
                        environment='123ENI',
                        exist=True
                        )
    return HttpResponse(u"欢迎光临 自强学堂!")


def home(request):
    return render(request, "home.html")


def admin_root(request):
    return render(request, "backend.html")


def search(request):
    return render(request, "search.html")


def room_detail(request):
    r = Room.objects.get(roomNumber='HZ10001')
    return render(request, "detail.html", {'R': r})


def admin_login(request):
    return render(request, "admin_login.html")


def admin_assessor(request):
    return render(request, "admin_assessor.html")


def admin_uploader(request):
    return render(request, "admin_uploader.html")


# post
# JianDing


def jianding_search(request):
    user = request.GET.get('jianding_search_account', None)
    name = request.GET.get('jianding_search_name', None)
    phone = request.GET.get('jianding_search_phone', None)
    result = Assessor.objects.filter(user__icontains=user,
                                     name__icontains=name,
                                     phone__icontains=phone,
                                     exist=True)
    # todo


def assessor_add(user, pw, name, phone, status, district):
    try:
        Assessor.objects.create(user=user,
                                pw=pw,
                                name=name,
                                phone=phone,
                                status=status,
                                district=district)
        print "Assessor_add ok!"
        return True
    except Exception, e:
        print "Assessor add error:"
        print e
        return False


def jianding_add(request):
    if request.method == 'POST':  # 当提交表单时
        form = AssessorForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['jianding_account']
                pw = form.cleaned_data['jianding_pw']
                name = form.cleaned_data['jianding_name']
                phone = form.cleaned_data['jianding_phone']
                Assessor.objects.create(user=user,
                                        pw=pw,
                                        name=name,
                                        phone=phone)
                print 'add success'
            except Exception, e:
                print e
    else:  # 当正常访问时
        print 'not post'


def jianding_modify(request):
    if request.method == 'POST':  # 当提交表单时
        form = AssessorForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['jianding_account']
                pw = form.cleaned_data['jianding_pw']
                name = form.cleaned_data['jianding_name']
                phone = form.cleaned_data['jianding_phone']
                p = Assessor.objects.get(user=user)
                p.pw = pw
                p.name = name
                p.phone = phone
                p.save()
                print 'modify success!'
            except Exception, e:
                print e
    else:  # 当正常访问时
        print 'not post'


def jianding_create(request):
    if request.method == 'POST':  # 当提交表单时
        form = AssessorUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['jianding_account']
                p, flag = Assessor.objects.get_or_create(user=user)
                if not flag:
                    p.exist = True
                print 'create success!'
            except Exception, e:
                print e
    else:  # 当正常访问时
        print 'not post'


def jianding_delete(request):
    if request.method == 'POST':  # 当提交表单时
        form = AssessorUserForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            try:
                user = form.cleaned_data['jianding_account']
                p = Assessor.objects.get(user=user)
                p.exist = False
                print 'delete success!'
            except Exception, e:
                print e
    else:  # 当正常访问时
        print 'not post'


