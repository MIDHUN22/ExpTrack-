from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
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