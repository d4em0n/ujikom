from django.shortcuts import render
from django.views import generic
from .models import Barang
from .mixins import GroupRequiredMixin
from .forms import BarangCreateForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'admin.html')

def base(request):
    return render(request, 'base_admin.html')

def barang(request):
    return render(request, 'data_barang.html')

def entri_barang(request):
    return render(request, 'entri_barang.html')

class BarangListView(GroupRequiredMixin, generic.ListView):
    model = Barang
    group_required = ["Manajemen", "Administrator"]
    context_object_name = 'daftar_barang'
    template_name = 'data_barang.html'

class BarangDetailView(GroupRequiredMixin, generic.DeleteView):
    model = Barang
    group_required = ["Manajemen", "Administrator"]
    template_name = 'detail_barang.html'
    context_object_name = 'barang'

class BarangCreateView(GroupRequiredMixin, generic.CreateView):
    template_name = 'entri_barang.html'
    group_required = ["Manajemen", "Administrator"]
    form_class = BarangCreateForm