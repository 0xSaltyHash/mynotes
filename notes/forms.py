from django import forms
from .models import Notes


class newNote(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'body']
