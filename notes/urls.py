from django.contrib.auth import login
from django.urls import path
from . import views

urlpatterns = [
     path("", views.index, name="index"),
     path("login", views.login_view, name="login"),
     path("logout", views.logout_view, name="logout"),
     path("register", views.register, name="register"),
     path("create", views.create, name="create"),
     path("edit/<int:id>", views.edit, name="edit"),
     path("view/<int:id>", views.view_note, name="view_note"),
     path("change_password", views.change_password, name="change_password"),
     path("favorite/<int:id>", views.favorite, name="favorite"),
     path("favorites", views.list_favorites, name="favorites")
 ]