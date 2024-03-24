from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Person
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/login")
def Home(request):
    person = Person.objects.all()
    return render(request, "home.html", {"persons": person})


def add_person(request):
    if request.method == "GET":
        return render(request, "add.html")
    elif request.method == "POST":
        data = request.POST
        if not data.get("id"):
            user = request.user
            person = Person.objects.create(
                name=data.get("name"),
                email=data.get("email"),
                bio=data.get("bio"),
                birth_date=data.get("birth_date"),
                phone=data.get("phone"),
                gender=data.get("gender"),
                user=user,
            )
            return redirect("view_person", email=person.email)
        else:
            person = Person.objects.get(id=data.get("id"))
            person.name = data.get("name")
            person.email = data.get("email")
            person.bio = data.get("bio")
            person.birth_date = data.get("birth_date")
            person.phone = data.get("phone")
            person.gender = data.get("gender")
            person.save()
        return redirect("view_person", email=person.email)


def update_person(request, id):
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist as msg:
        return HttpResponse(msg)
    else:
        return render(request, "add.html", {"all_person": person})


def view_person(request, email):
    try:
        person = Person.objects.get(email=email)
    except Person.DoesNotExist:
        return render(request, "add.html")
    else:
        return render(request, "card.html", {"all_persons": person})


def delete_Person(request, id):
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist as msg:
        return HttpResponse(msg)
    else:
        person.delete()
        return redirect("add_person")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "register.html", {"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if (
                    hasattr(user, "email")
                    and user.email is not None
                    and user.is_superuser == 1
                ):
                    return redirect("Home")
                elif hasattr(user, "email") and user.email is not None:
                    return redirect("view_person", email=user.email)
                else:
                    return redirect("Home", email=user.email)
    form = AuthenticationForm()
    return render(request, "login.html", {"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")
