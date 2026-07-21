from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.login_view,name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin_dashboard/",views.adminDashboard, name='admin_dashboard'),
    path("logout/",views.logout_view,name='logout'),
    path("income-category/",views.income_category_list,name="income_category_list",),

    path("income-category/add/",views.income_category_add,name="income_category_add",),

    path("income-category/edit/<int:id>/",views.income_category_edit,name="income_category_edit",),

    path("income-category/delete/<int:id>/",views.income_category_delete,name="income_category_delete",),
    path("expense-category/",views.expense_category_list,name="expense_category_list",),
]