from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        "name": "Midhun"
    }
    return render(request, "home.html", context)