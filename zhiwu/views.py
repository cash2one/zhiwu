from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "home.html")


def search(request):
    return render(request, "search.html")


def room_detail(request):
    return render(request, "room_detail.html")
