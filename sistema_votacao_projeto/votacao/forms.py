from django import forms
from .models import Vereador

class VereadorForm(forms.ModelForm):
    class Meta:
        model = Vereador
        fields = '__all__'