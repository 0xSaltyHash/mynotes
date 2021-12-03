from django.contrib import admin
from notes.models import User, Notes, Favorites
# Register your models here.
admin.site.register(Notes)
admin.site.register(User)
admin.site.register(Favorites)