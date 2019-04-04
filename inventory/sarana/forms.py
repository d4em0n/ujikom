from django import forms
from .models import Barang, PinjamBarang, Suplier

class BarangCreateForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = '__all__'

class PeminjamanCreateForm(forms.ModelForm):
    class Meta:
        model = PinjamBarang
        fields = ['jml_dipinjam', 'tgl_kembali']

class SuplierCreateForm(forms.ModelForm):
    class Meta:
        model = Suplier
        fields = '__all__'