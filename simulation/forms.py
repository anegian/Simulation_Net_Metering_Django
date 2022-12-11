from django.forms import ModelForm
from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model = CustomerModel
        fields = '__all__'

class PlaceForm(ModelForm):
    class Meta:
        model = PlaceModel
        fields = '__all__'
