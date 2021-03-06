from django.shortcuts import redirect, render
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls.base import reverse
from .models import Favorites, User, Notes
from .forms import newNote
# Create your views here.

@require_http_methods(['GET'])
@login_required(login_url='/login')
def index(request):
    userNotes = Notes.objects.filter(creator=request.user)
    return render(request, "notes/index.html", {
        "notes": userNotes

    })

@require_http_methods(['GET', 'POST'])
@login_required(login_url='/login')
def create(request):
    if request.method == "GET":
        return render(request, "notes/create.html", {
            "notesForm": newNote
        })
    elif request.method == "POST":
        form = newNote(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.creator = request.user
            new_note.save()
        return redirect(view_note, id=new_note.id)

@require_http_methods(['GET', 'POST'])
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
            updated_note = form.save()
            messages.success(request, 'Note edited successfuly')
            return redirect(view_note, id=updated_note.id)

@require_http_methods(['GET'])
def view_note(request, id):
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

@require_http_methods(['GET', 'POST'])
@login_required(login_url='/login')
def change_password(request):
    if request.method == "GET":
        return render(request, "notes/change_password.html", {
            "form": PasswordChangeForm(request.user)
        })

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, "Couldn't change Password")
            return redirect('change_password')

@require_http_methods(['GET', 'POST'])
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

@require_http_methods(['GET', 'POST'])
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

@require_http_methods(['POST'])
@login_required(login_url='/login')
def favorite(request, id):
    if request.method == "POST":
        note = Notes.objects.get(pk=id)
        Favorites.objects.create(user=request.user, favorite_note=note)
        return render(request, "notes/note.html", {
            "note": note
        })

@require_http_methods(['GET'])
@login_required(login_url='/login')
def list_favorites(request):
    if request.method == "GET":
        favorites = Favorites.objects.filter(user=request.user)
        return render(request, "notes/favorites.html", {
            "notes": favorites
        })