from django.shortcuts import render
from django.views import generic
from .models import Barang, PinjamBarang, StokBarang, Suplier, BarangMasuk, BarangKeluar, User
from .mixins import GroupRequiredMixin
from .forms import BarangCreateForm, PeminjamanCreateForm, SuplierCreateForm, BarangKeluarCreateForm
from django.urls import reverse_lazy, reverse
from django.db.models import Sum
from django.contrib.auth.models import Group

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

# Create your views here.
def index(request):
    return render(request, 'index.html')

class DashboardView(GroupRequiredMixin, generic.View):
    template_name = 'admin.html'
    group_required = ["Manajemen", "Administrator", "Peminjam"]
    
    def get_context_data(self, request, **kwargs):
        context = dict() 
        context.update(BarangKeluar.objects.aggregate(total_keluar=Sum('jml_keluar')))
        context.update(BarangMasuk.objects.aggregate(total_masuk=Sum('jml_masuk')))
        context.update(Barang.objects.aggregate(total_barang=Sum('jumlah_barang')))
        context.update({'total_user': User.objects.count()})
        context.update({'user_full_name': request.user.get_full_name() or request.user.username })
        context.update({'request': request})
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

class SuplierListView(GroupRequiredMixin, generic.ListView):
    model = Suplier
    group_required = ["Manajemen", "Administrator"]
    context_object_name = 'data_suplier'
    template_name = 'data_suplier.html'

class SuplierCreateView(GroupRequiredMixin, generic.CreateView):
    template_name = 'entri_suplier.html'
    group_required = ["Manajemen", "Administrator"]
    form_class = SuplierCreateForm

class SuplierDetailView(GroupRequiredMixin, generic.DetailView):
    model = Suplier
    group_required = ["Manajemen", "Administrator"]
    template_name = 'detail_suplier.html'
    context_object_name = 'suplier'

    def get_context_data(self, **kwargs):
        context = super(SuplierDetailView, self).get_context_data(**kwargs)
        context['data_barang_masuk'] = context['suplier'].barang_masuk.all()
        return context

class SuplierUpdateView(GroupRequiredMixin, generic.UpdateView):
    model = Suplier
    group_required = ["Manajemen", "Administrator"]
    template_name = 'entri_suplier.html'
    context_object_name = 'suplier'
    form_class = SuplierCreateForm

class SuplierDeleteView(GroupRequiredMixin, generic.DeleteView):
    model = Suplier 
    template_name = 'entri_suplier.html'
    group_required = ["Manajemen", "Administrator"]
    form_class = SuplierCreateForm
    success_url = reverse_lazy('suplier')

class BarangMasukCreateView(GroupRequiredMixin, generic.CreateView):
    template_name = 'entri_barang.html'
    group_required = ["Manajemen", "Administrator"]
    form_class = BarangCreateForm

    def form_valid(self, form):
        form.save()
        stok = StokBarang(total_stok=form.instance.jumlah_barang, 
                          jml_masuk=form.instance.jumlah_barang, 
                          jml_keluar=0, 
                          jml_dipinjam=0, 
                          barang=form.instance)
        suplier = Suplier.objects.get(id_suplier=self.kwargs['id_suplier'])
        barang_masuk = BarangMasuk(barang=form.instance, 
                                   jml_masuk=form.instance.jumlah_barang, 
                                   suplier=suplier)
        stok.save()
        barang_masuk.save()
        return super(BarangMasukCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('detail_suplier', kwargs={'pk': self.kwargs['id_suplier']})

class BarangKeluarCreateView(GroupRequiredMixin, generic.CreateView):
    template_name = 'entri_barang_keluar.html'
    group_required = ["Manajemen", "Administrator"]
    form_class = BarangKeluarCreateForm

    def get_context_data(self, **kwargs):
        context = super(BarangKeluarCreateView, self).get_context_data(**kwargs)
        context['barang'] = Barang.objects.get(id_barang=self.kwargs['id_barang'])
        context['stok'] = context['barang'].stok.get()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        jml_keluar = form.instance.jml_keluar
        barang = context['barang']
        stok = context['stok']
        form.instance.barang = barang
        form.save()
        barang.jumlah_barang -= jml_keluar
        stok.jml_keluar += jml_keluar
        stok.total_stok -= jml_keluar
        barang.save()
        stok.save()
        return super(BarangKeluarCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('detail_barang', kwargs={'pk': self.kwargs['id_barang']})

class BarangListView(GroupRequiredMixin, generic.ListView):
    model = Barang
    group_required = ["Manajemen", "Administrator", "Peminjam"]
    context_object_name = 'daftar_barang'
    template_name = 'data_barang.html'

    def get_queryset(self):
        return Barang.objects.all().prefetch_related('stok')

class BarangDetailView(GroupRequiredMixin, generic.DetailView):
    model = Barang
    group_required = ["Manajemen", "Administrator", "Peminjam"]
    template_name = 'detail_barang.html'
    context_object_name = 'barang'
    
    def get_context_data(self, **kwargs):
        context = super(BarangDetailView, self).get_context_data(**kwargs)
        stok = context['barang'].stok.get()
        context['stok'] = stok
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
    group_required = ["Manajemen", "Administrator", "Peminjam"]
    template_name = 'data_pinjam.html'
    context_object_name = 'data_pinjam'

    def get_queryset(self):
        if has_group(self.request.user, "Peminjam"):
            queryset = self.request.user.pinjaman.all()
        else:
            queryset = super(PeminjamanListView, self).get_queryset()
        return queryset

class DataBarangKeluarListView(GroupRequiredMixin, generic.ListView):
    model = Barang
    group_required = ["Manajemen", "Administrator"]
    template_name = 'daftar_barang_keluar.html'
    context_object_name = 'daftar_barang'

class DataPinjamBarangListView(GroupRequiredMixin, generic.ListView):
    model = Barang
    group_required = ["Manajemen", "Administrator", "Peminjam"]
    template_name = 'daftar_data_pinjam.html'
    context_object_name = 'daftar_barang'

class PeminjamanDetailView(GroupRequiredMixin, generic.DeleteView):
    model = PinjamBarang
    group_required = ["Manajemen", "Administrator", "Peminjam"]
    template_name = 'detail_pinjam.html'
    context_object_name = 'pinjam'

    def get_queryset(self):
        if has_group(self.request.user, "Peminjam"):
            queryset = self.request.user.pinjaman.all()
        else:
            queryset = super(PeminjamanListView, self).get_queryset()
        return queryset

class PeminjamanCreateView(GroupRequiredMixin, generic.CreateView):
    model = PinjamBarang
    form_class = PeminjamanCreateForm
    group_required = ["Manajemen", "Administrator", "Peminjam"]
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
        return super(PeminjamanCreateView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response

class PeminjamanUpdateView(GroupRequiredMixin, generic.UpdateView):
    model = PinjamBarang
    form_class = PeminjamanCreateForm
    group_required = ["Manajemen", "Administrator", "Peminjam"]
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

    def get_queryset(self):
        if has_group(self.request.user, "Peminjam"):
            queryset = self.request.user.pinjaman.all()
        else:
            queryset = super(PeminjamanListView, self).get_queryset()
        return queryset

class PeminjamanDeleteView(GroupRequiredMixin, generic.DeleteView):
    model = PinjamBarang
    group_required = ["Manajemen", "Administrator"]
    success_url = reverse_lazy('pinjam')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        stok = self.object.barang.stok.get()
        stok.total_stok += self.object.jml_dipinjam
        stok.jml_dipinjam -= self.object.jml_dipinjam
        stok.save()
        return super(PeminjamanDeleteView, self).delete(*args, **kwargs)

    def get_queryset(self):
        if has_group(self.request.user, "Peminjam"):
            queryset = self.request.user.pinjaman.all()
        else:
            queryset = super(PeminjamanListView, self).get_queryset()
        return queryset

class BarangKeluarListView(GroupRequiredMixin, generic.ListView):
    model = BarangKeluar
    group_required = ["Manajemen", "Administrator"]
    context_object_name = 'data_barang_keluar'
    template_name = 'data_barang_keluar.html'

class BarangMasukListView(GroupRequiredMixin, generic.ListView):
    model = BarangMasuk
    group_required = ["Manajemen", "Administrator"]
    context_object_name = 'data_barang_masuk'
    template_name = 'data_barang_masuk.html'

class DataEntriBarangMasukListView(GroupRequiredMixin, generic.ListView):
    model = Suplier
    group_required = ["Manajemen", "Administrator"]
    context_object_name = 'data_suplier'
    template_name = 'data_entri_barang_masuk.html'