from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    # return HttpResponse('homepage')
    return render(request, 'homepage.html')

def login(request):
    # return HttpResponse('about')
    return render(request, 'login.html')

def ChangePass(request):
    # return HttpResponse('about')
    return render(request, 'ChangePass.html')
def consulterSimple(request):
    return render(request, 'viewconsult.html')

def index(request):
    return render(request, 'index.html')

def consulter(request):
    # return HttpResponse('about')
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent
    print(BASE_DIR) 
    return render(request, 'consultation.html')

def adduser(request):
    return render(request, 'adduser.html')

def get_first(request):
    return render(request, 'first.html')
def admin(request):
    return render(request, 'admin.html')
def test(request):
    return render(request, 'test.html')
