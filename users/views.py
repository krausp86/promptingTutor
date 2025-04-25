from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task")  # <- hier geht’s zur ersten Aufgabe
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("task")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

