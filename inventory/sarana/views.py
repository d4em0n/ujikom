from django.shortcuts import render
from django.views import generic
from .models import Barang, PinjamBarang, StokBarang
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
    
    def get_context_data(self, **kwargs):
        context = super(BarangDetailView, self).get_context_data(**kwargs)
        stok = context['barang'].stok.get()
        context['total_stok'] = stok.total_stok
        return context

class BarangCreateView(GroupRequiredMixin, generic.CreateView):
    template_name = 'entri_barang.html'
    group_required = ["Manajemen", "Administrator"]
    form_class = BarangCreateForm

    def form_valid(self, form):
        form.save()
        stok = StokBarang(total_stok=form.instance.jumlah_barang, jml_masuk=0, jml_keluar=0, jml_dipinjam=0, barang=form.instance)
        stok.save()
        return super(BarangCreateView, self).form_valid(form)

class BarangUpdateView(GroupRequiredMixin, generic.UpdateView):
    model = Barang
    template_name = 'entri_barang.html'
    group_required = ["Manajemen", "Administrator"]
    form_class = BarangCreateForm

    def get_success_url(self):
        return reverse_lazy('detail_barang', kwargs={'pk': self.object.pk})

class BarangDeleteView(GroupRequiredMixin, generic.DeleteView):
    model = Barang
    template_name = 'entri_barang.html'
    group_required = ["Manajemen", "Administrator"]
    form_class = BarangCreateForm
    success_url = reverse_lazy('barang')

class PeminjamanListView(GroupRequiredMixin, generic.ListView):
    model = PinjamBarang
    group_required = ["Manajemen", "Administrator"]
    template_name = 'data_pinjam.html'
    context_object_name = 'data_pinjam'

class PeminjamanDetailView(GroupRequiredMixin, generic.DeleteView):
    model = PinjamBarang
    group_required = ["Manajemen", "Administrator"]
    template_name = 'detail_pinjam.html'
    context_object_name = 'pinjam'

class PeminjamanCreateView(GroupRequiredMixin, generic.CreateView):
    model = PinjamBarang
    form_class = PeminjamanCreateForm
    group_required = ["Manajemen", "Administrator"]
    template_name = 'pinjam_barang.html'

    def get_context_data(self, **kwargs):
        context = super(PeminjamanCreateView, self).get_context_data(**kwargs)
        context['barang'] = Barang.objects.get(id_barang=self.kwargs['id_barang'])
        stok = context['barang'].stok.get()
        context['total_stok'] = stok.total_stok
        return context
    
    def form_valid(self, form):
        barang = Barang.objects.get(id_barang=self.kwargs['id_barang'])
        stok = barang.stok.get()
        stok.total_stok -= form.instance.jml_dipinjam
        stok.jml_dipinjam += form.instance.jml_dipinjam
        stok.save() 
        form.instance.peminjam = self.request.user
        form.instance.barang = barang
        print(form.instance.jml_dipinjam)
        return super(PeminjamanCreateView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return response

class PeminjamanUpdateView(GroupRequiredMixin, generic.UpdateView):
    model = PinjamBarang
    form_class = PeminjamanCreateForm
    group_required = ["Manajemen", "Administrator"]
    template_name = 'edit_pinjam_barang.html'
    context_object_name = 'pinjam'

    def get_context_data(self, **kwargs):
        context = super(PeminjamanUpdateView, self).get_context_data(**kwargs)
        stok = context['pinjam'].barang.stok.get()
        context['total_stok'] = stok.total_stok
        return context

    def form_valid(self, form):
        pinjam = PinjamBarang.objects.get(pk=self.object.pk) # Get old data
        stok = pinjam.barang.stok.get()
        distance = form.instance.jml_dipinjam - pinjam.jml_dipinjam
        stok.total_stok -= distance
        stok.jml_dipinjam += distance
        stok.save() 
        return super(PeminjamanUpdateView, self).form_valid(form)