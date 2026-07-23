from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.login_view,name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin_dashboard/",views.adminDashboard, name='admin_dashboard'),
    path("logout/",views.logout_view,name='logout'),

    path("all-users/",views.get_all_users,name='all_users'),
    path("all-users/edit/<int:id>",views.user_edit,name='user_edit'),
    path("all-users/toggle/<int:id>/",views.user_toggle,name="user_toggle",),
    path("all-users/delete/<int:id>",views.user_delete,name='user_delete'),


    path("income-category/",views.income_category_list,name="income_category_list",),
    path("income-category/add/",views.income_category_add,name="income_category_add",),
    path("income-category/edit/<int:id>/",views.income_category_edit,name="income_category_edit",),
    path("income-category/delete/<int:id>/",views.income_category_delete,name="income_category_delete",),
    path("income-category/toggle/<int:id>/",views.income_category_toggle,name="income_category_toggle"),
    path("income-category-export/",views.income_category_export,name="income_category_export"),


    path("expense-category/",views.expense_category_list,name="expense_category_list",),
    path("expense-category/add/",views.expense_category_add,name="expense_category_add",),
    path("expense-category/edit/<int:id>/",views.expense_category_edit,name="expense_category_edit",),
    path("expense-category/delete/<int:id>/",views.expense_category_delete,name="expense_category_delete",),
    path("expense-category/toggle/<int:id>/",views.expense_category_toggle,name="expense_category_toggle"),
    path("expense-category-export/",views.expense_category_export,name="expense_category_export"),

    path("income/",views.income,name="income_list"),
    path("income/add/",views.income_add,name="income_add"),
    path("income/edit/<int:id>/",views.income_edit,name="income_edit"),
    path("income/delete/<int:id>/",views.income_delete,name="income_delete"),

    path("expense/",views.expense,name="expense_list"),
    path("expense/add/",views.expense_add,name="expense_add"),
    path("expense/edit/<int:id>/",views.expense_edit,name="expense_edit"),
    path("expense/delete/<int:id>/",views.expense_delete,name="expense_delete"),




]