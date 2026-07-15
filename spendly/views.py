from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return render(request,"auth/login.html")

def register(request):
    return render(request,"auth/register.html")

def home(request):
    context = {
        "name": "Midhun"
    }
    return render(request, "home.html", context)

def dashboard(request):
    context={
        "name":"spendly",
        "need":"project"
    }
    return render(request,"dashboard.html",context)


