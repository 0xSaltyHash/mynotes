from django import forms
from .models import Notes


class newNote(forms.ModelFORM):
    class Meta:
        model = Notes
        fields = ['title', 'body']
