from django import forms
from django.forms import ValidationError

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