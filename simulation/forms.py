from django.forms import ModelForm
from .models import *
from django import forms

class CustomerForm(ModelForm):
    class Meta:
        model = CustomerModel
        fields = '__all__'

class PlaceForm(ModelForm):
    class Meta:
        model = PlaceModel
        fields = '__all__'

class MyForm(forms.Form):
    CHOICES = [("", 'Περιφέρεια'), ('option1', 'Αττική'), ('option2', 'Ανατολική Μακεδονία &amp; Θράκη'),
               ('option3', 'Βόρειο Αιγαίο'), ('option4', 'Δυτική Ελλάδα'), ('option5', 'Δυτική Μακεδονία'),
               ('option6', 'Ήπειρος'),  ('option7', 'Θεσσαλία'), ('option8', 'Ιόνιοι Νήσοι'),
               ('option9', 'Κεντρική Μακεδονία'), ('option10', 'Κρήτη'), ('option11', 'Νότιο Αιγαίο'),
               ('option12', 'Πελοπόννησος'), ('option13', 'Στερεά Ελλάδα')]
    select = forms.ChoiceField(choices=CHOICES)
