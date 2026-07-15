from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    return render(request,"auth/login.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["email"],  # Using email as username
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                password=form.cleaned_data["password"],
            )

            return redirect("login")  # Change 'login' to your login URL name

    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})
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


