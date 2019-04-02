from django import forms
from .models import Barang

class BarangCreateForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = '__all__'