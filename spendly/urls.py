from django.urls import path
from . import views

urlpatterns = [
    path("",views.login,name="login"),
    path("register/", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("home_test", views.home, name="home"),
]