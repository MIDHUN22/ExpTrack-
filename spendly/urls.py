from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.login_view,name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin_dashboard/",views.adminDashboard, name='admin_dashboard'),
    path("logout/",views.logout_view,name='logout'),
    path("home_test", views.home, name="home"),
]