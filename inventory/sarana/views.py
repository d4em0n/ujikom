from django.shortcuts import render
from django.views import generic
from .models import Barang, PinjamBarang
from .mixins import GroupRequiredMixin
from .forms import BarangCreateForm, PeminjamanCreateForm
from django.urls import reverse_lazy, reverse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'admin.html')

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

class BarangUpdateView(GroupRequiredMixin, generic.UpdateView):
    model = Barang
    template_name = 'entri_barang.html'
    group_required = ["Manajemen", "Administrator"]
    form_class = BarangCreateForm

    def get_success_url(self):
        return reverse_lazy('detail_barang', kwargs={'pk': self.object.pk})

class PeminjamanCreateView(GroupRequiredMixin, generic.CreateView):
    model = PinjamBarang
    form_class = PeminjamanCreateForm
    group_required = ["Manajemen", "Administrator"]
    template_name = 'pinjam_barang.html'

    def get_context_data(self, **kwargs):
        context = super(PeminjamanCreateView, self).get_context_data(**kwargs)
        context['barang'] = Barang.objects.get(id_barang=self.kwargs['id_barang'])
        return context
    
    def form_valid(self, form):
        form.instance.peminjam = self.request.user
        form.instance.barang = Barang.objects.get(id_barang=self.kwargs['id_barang'])
        print(form.instance.jml_dipinjam)
        form.save()
        return super(PeminjamanCreateView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return response