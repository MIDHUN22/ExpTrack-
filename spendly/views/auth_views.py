from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error(None, "Invalid email or password.")
            else:
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )

                if user is not None:

                    login(request, user)

                    if user.is_staff:
                        return redirect("admin_dashboard")

                    return redirect("dashboard")

                form.add_error(None, "Invalid email or password.")

    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            if User.objects.filter(email=form.cleaned_data["email"]).exists():
                form.add_error("email", "Email already exists.")

            else:
                User.objects.create_user(
                    username=form.cleaned_data["email"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    email=form.cleaned_data["email"],
                    phone=form.cleaned_data["phone"],
                    password=form.cleaned_data["password"],
                )

                messages.success(request, "Registration successful. Please log in.")
                return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})


@login_required(login_url='login')
def dashboard(request):
    return render(request, "dashboard.html", {

    })

@login_required(login_url="login")
def adminDashboard(request):
    return render(request, "admin/dashboard.html", {
        "message": "Under Development",
    })
@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")