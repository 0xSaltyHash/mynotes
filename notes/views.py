from django.shortcuts import redirect, render
from django.db import IntegrityError
from django.contrib import messages
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

@login_required(login_url='/login')
def edit(request, id):
    try:
        note = Notes.objects.get(pk=id)
    except Notes.DoesNotExist:
        messages.error(request, 'Note doesn\'t exist')
        return redirect(index)
    
    if request.user != note.creator:
        messages.error(request, 'You cannot edit this note')
        return redirect(index)
    
    if request.method == "GET":
        notesForm = newNote(instance=note)
        return render(request, "notes/edit.html", {
            "notesForm": notesForm,
            "note": note
        })

    if request.method == "POST":
        form = newNote(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note edited successfuly')
            return redirect(index)

def note(request, id):
    if request.method == "GET":
        try:
             note = Notes.objects.get(pk=id)
        except Notes.DoesNotExist:
            messages.error(request, 'Note doesn\'t exist')
            return redirect(index)
        if (note.is_public == False) and (request.user != note.creator):
            messages.error(request, 'You cannot view this note')
            return redirect(index)

        return render(request, "notes/note.html", {
            "note": note
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            return render(request, "notes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "notes/login.html")

def logout_view(request):
    logout(request)
    return redirect(index)

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
        return redirect(index)
    else:
        return render(request, "notes/register.html")