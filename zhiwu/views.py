from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "home.html")


def search(request):
    return render(request, "search.html")


def room_detail(request):
    return render(request, "room_detail.html")


def admin_login(request):
    return render(request, "admin_login.html")


def admin_assessor(request):
    return render(request, "admin_assessor.html")


def admin_uploader(request):
    return render(request, "admin_uploader.html")
