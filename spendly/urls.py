from django.urls import path
from . import views

urlpatterns = [
    path("",views.login,name="login"),
    path("home_test", views.home, name="home"),
    path("dashboard", views.dashboard, name="dashboard"),
]