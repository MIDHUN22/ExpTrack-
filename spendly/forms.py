from django import forms
from django.forms import ValidationError
from .models import IncomeCategory, ExpenseCategory,User

def validate_name(value):
    if len(value.strip()) < 2:
        raise ValidationError("Enter a valid name.")
def validate_mail(value):
    if "@" not in value:
        raise ValidationError("Enter a valid email address.")
def validate_phone(value):
    if len(value) != 10:
        raise ValidationError("Phone number must be exactly 10 digits.")

    if not value.isdigit():
        raise ValidationError("Phone number must contain only digits.")
        
def validate_password(value):
     if len(value)<4:
        raise ValidationError("Password Must Contain At Least 4 Digit")

class RegisterForm(forms.Form):
    first_name = forms.CharField(validators=[validate_name])
    last_name = forms.CharField(validators=[validate_name])
    email=forms.EmailField(validators=[validate_mail])
    phone = forms.CharField(validators=[validate_phone])
    password=forms.CharField(validators=[validate_password])

from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )

# ****************************************************Admin Form*****************
class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model=IncomeCategory
        fields=["name","description","is_active"]
        widgets={
            "name":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Enter An Income Category"
            }),
            "description":forms.Textarea(attrs={
                "class":"form-control",
                "rows":3,
                "placeholder":"Enter a Meaningfull Description(optional)"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"}) 
            
            }

class ExpenseCategoryForm(forms.ModelForm):

    class Meta:
        model = ExpenseCategory
        fields = ["name", "description", "is_active"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter expense category"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter a short description"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
            }),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }