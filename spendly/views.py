from django.shortcuts import render, redirect,get_object_or_404
from .forms import RegisterForm, LoginForm,IncomeCategoryForm, ExpenseCategoryForm, UserEditForm,IncomeForm,ExpenseForm
from django.db.models import Sum,Count
from decimal import Decimal
from .utils import export_to_csv
from .models import User,IncomeCategory,ExpenseCategory,Income,Expense
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models.functions import Coalesce



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



@login_required(login_url="login")
def adminDashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    total_users = User.objects.count()
    total_income_categories = IncomeCategory.objects.count()
    total_expense_categories = ExpenseCategory.objects.count()
    active_users = User.objects.filter(is_active=True).count()

    total_income = Income.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expense = Expense.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    context = {
        "total_users": total_users,
        "total_income_categories": total_income_categories,
        "total_expense_categories": total_expense_categories,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "active_users": User.objects.filter(is_staff=False, is_active=True).count(),
    }

    return render(request, "admin/dashboard.html", context)
@login_required(login_url="login")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")
#_________________________________________ADMIN VIEWS___________________________________

def get_all_users(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    exp_users = User.objects.all()

    return render(
        request,
        "admin/all_users/list.html",
        {"exp_users": exp_users}
    )


def user_edit(request, id):

    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    user = get_object_or_404(User, id=id)

    if request.method == "POST":

        form = UserEditForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("all_users")

    else:
        form = UserEditForm(instance=user)

    return render(
        request,
        "admin/all_users/edit.html",
        {
            "form": form
        }
    )

def user_toggle(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    user = get_object_or_404(User, id=id)

    # Prevent disabling yourself
    if user == request.user:
        return redirect("all_users")

    user.is_active = not user.is_active
    user.save()

    return redirect("all_users")

def user_delete(request, id):

    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.delete()
        return redirect("all_users")

    return render(
        request,
        "admin/all_users/delete.html",
        {"user": user}
    )

def income_category_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")
    categories = IncomeCategory.objects.all().order_by("id")

    return render(
        request,
        "admin/income_category/list.html",
        {"categories": categories}
    )
    

def income_category_add(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    if request.method == "POST":
        form = IncomeCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("income_category_list")

    else:
        form = IncomeCategoryForm()

    return render(
        request,
        "admin/income_category/form.html",
        {"form": form}
    )


# def income_category_edit(request,id):
#     if not request.user.is_staff:
#         return HttpResponseForbidden("Permission denied")
#     if request.method == "POST":
#         print(request.POST)

def income_category_edit(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    category = get_object_or_404(IncomeCategory, id=id)

    if request.method == "POST":
        form = IncomeCategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect("income_category_list")

    else:
        form = IncomeCategoryForm(instance=category)

    return render(
        request,
        "admin/income_category/form.html",
        {"form": form}
    )

def income_category_toggle(request, id):

    if not request.user.is_staff:
        return HttpResponseForbidden("Permission Denied")

    category = get_object_or_404(IncomeCategory, id=id)

    category.is_active = not category.is_active
    category.save()

    return redirect("income_category_list")

def income_category_delete(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    category = get_object_or_404(IncomeCategory, id=id)

    if request.method == "POST":
        category.delete()
        return redirect("income_category_list")

    return render(
        request,
        "admin/income_category/delete.html",
        {"category": category}
    )


def income_category_export(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    categories = IncomeCategory.objects.order_by("id")

    return export_to_csv(
        filename="income_categories",
        headers=[
            "ID",
            "Category",
            "Description",
            "Status",
            "Created At",
            "Updated At",
        ],
        queryset=categories,
        row_builder=lambda c: [
            c.id,
            c.name,
            c.description,
            "Active" if c.is_active else "Inactive",
            c.created_at.strftime("%d-%m-%Y"),
            c.updated_at.strftime("%d-%m-%Y"),
        ],
    )

def expense_category_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")
    categories = ExpenseCategory.objects.all().order_by("id")

    return render(
        request,
        "admin/expense_category/list.html",
        {"categories": categories}
    )
 
def expense_category_add(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    if request.method == "POST":
        form = ExpenseCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("expense_category_list")

    else:
        form = ExpenseCategoryForm()

    return render(
        request,
        "admin/expense_category/form.html",
        {"form": form}
    )

def expense_category_edit(request,id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")
    category = get_object_or_404(ExpenseCategory, id=id)

    if request.method == "POST":
        form = ExpenseCategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect("expense_category_list")

    else:
        form = ExpenseCategoryForm(instance=category)

    return render(
        request,
        "admin/expense_category/form.html",
        {"form": form}
    )
def expense_category_delete(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    category = get_object_or_404(ExpenseCategory, id=id)

    if request.method == "POST":
        category.delete()
        return redirect("expense_category_list")

    return render(
        request,
        "admin/expense_category/delete.html",
        {"category": category}
    )

def expense_category_toggle(request,id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission Denied")

    category = get_object_or_404(ExpenseCategory, id=id)

    category.is_active = not category.is_active
    category.save()

    return redirect("expense_category_list")

def expense_category_export(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Permission denied")

    categories = ExpenseCategory.objects.order_by("id")

    return export_to_csv(
        filename="expense_categories",
        headers=[
            "ID",
            "Category",
            "Description",
            "Status",
            "Created At",
            "Updated At",
        ],
        queryset=categories,
        row_builder=lambda c: [
            c.id,
            c.name,
            c.description,
            "Active" if c.is_active else "Inactive",
            c.created_at.strftime("%d-%m-%Y"),
            c.updated_at.strftime("%d-%m-%Y"),
        ],
    )
# ------------------------------------------------- USER VIEWS---------------------------------

@login_required(login_url="login")
def dashboard(request):

    # Total Income
    total_income = (
        Income.objects
        .filter(user=request.user)
        .aggregate(total=Coalesce(Sum("amount"), Decimal("0.00")))
    )["total"]

    total_transactions = Expense.objects.filter(
        user=request.user
    ).count()

    # Total Expense
    total_expense = (
        Expense.objects
        .filter(user=request.user)
        .aggregate(total=Coalesce(Sum("amount"), Decimal("0.00")))
    )["total"]

    # Available Balance
    available_balance = total_income - total_expense

    # Income by Category (Chart)
    income_by_category = (
        Income.objects
        .filter(user=request.user)
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("category__name")
    )

    income_labels = []
    income_totals = []

    for item in income_by_category:
        income_labels.append(item["category__name"])
        income_totals.append(float(item["total"]))

    # Expense by Category (Chart)   ← NEW
    expense_by_category = (
        Expense.objects
        .filter(user=request.user)
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("category__name")
    )

    expense_labels = []
    expense_totals = []

    for item in expense_by_category:
        expense_labels.append(item["category__name"])
        expense_totals.append(float(item["total"]))

    context = {
        "total_income": total_income,
        "total_expense": total_expense,
        "available_balance": available_balance,
        "total_transactions": total_transactions,
        "income_labels": income_labels,
        "income_totals": income_totals,
        "expense_labels": expense_labels,   # ← NEW
        "expense_totals": expense_totals,   # ← NEW
    }

    return render(request, "users/dashboard.html", context)


@login_required(login_url="login")
def income(request):
    incomes = Income.objects.filter(
        user=request.user
    ).order_by("id")

    return render(
        request,
        "users/income/list.html",
        {"incomes":incomes}
    )
    pass

@login_required(login_url="login")
def income_add(request):
    if request.method=="POST":
        form=IncomeForm(request.POST)
    
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect("income_list")
    else:
        form=IncomeForm()
    return render(
        request,
        'users/income/form.html',
        {"form":form}
        )
    
@login_required(login_url="login")
def income_edit(request,id):
    income=get_object_or_404(Income,id=id, user=request.user)

    if request.method=='POST':
        form=IncomeForm(request.POST,instance=income)

        if form.is_valid():
            form.save()
            return redirect("income_list")
    else:
        form=IncomeForm(instance=income)
    return render(
        request,
        "users/income/form.html",
        {"form":form}
    )
    

@login_required(login_url="login")
def income_delete(request,id):
    income=get_object_or_404(Income,id=id, user=request.user)

    if request.method=="POST":
        income.delete()
        return redirect("income_list")

    return render(
        request,
        "users/income/list.html",
        {"income":income}
    )

def income_export(request):
   
    incomes = Income.objects.filter(user=request.user).order_by("id")
    return export_to_csv(
        filename="income",
        headers=[
            "ID",
            "Amount",
            "Description",
            "Date",
            "Created At",
            "Updated At",
        ],
        queryset=incomes,
        row_builder=lambda c: [
            c.id,
            c.amount,
            c.description,
            c.date,
            c.created_at.strftime("%d-%m-%Y"),
            c.updated_at.strftime("%d-%m-%Y"),
        ],
    )    

@login_required(login_url="login")
def expense(request):
    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "users/expense/list.html",
        {"expenses": expenses}
    )


@login_required(login_url="login")
def expense_add(request):

    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            return redirect("expense_list")

    else:
        form = ExpenseForm()

    return render(
        request,
        "users/expense/form.html",
        {"form": form}
    )


@login_required(login_url="login")
def expense_edit(request, id):

    expense = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            return redirect("expense_list")

    else:
        form = ExpenseForm(instance=expense)

    return render(
        request,
        "users/expense/form.html",
        {"form": form}
    )


@login_required(login_url="login")
def expense_delete(request,id):

    expense = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        expense.delete()

    return redirect("expense_list")

def expense_export(request):
   
    expenses = Expense.objects.filter(user=request.user).order_by("id")
    return export_to_csv(
        filename="expense",
        headers=[
            "ID",
            "Amount",
            "Description",
            "Date",
            "Created At",
            "Updated At",
        ],
        queryset=expenses,
        row_builder=lambda c: [
            c.id,
            c.amount,
            c.description,
            c.date,
            c.created_at.strftime("%d-%m-%Y"),
            c.updated_at.strftime("%d-%m-%Y"),
        ],
    )  

def savings_list(request):
    pass

def savings_add(request):
    pass

def savings_edit(request):
    pass

def savings_delete(request):
    pass