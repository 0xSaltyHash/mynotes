from django.shortcuts import redirect, render
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User, Notes
from .forms import newNote
# Create your views here.

@login_required(login_url='/login')
def index(request):
    userNotes = Notes.objects.filter(creator=request.user)
    return render(request, "notes/index.html", {
        "notes": userNotes

    })

@login_required(login_url='/login')
def create(request):
    if request.method == "GET":
        return render(request, "notes/create.html", {
            "notesForm": newNote
        })
    elif request.method == "POST":
        form = newNote(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.creator = request.user
            note.save()
        return redirect(index)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "notes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "notes/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "notes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "notes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "notes/register.html")