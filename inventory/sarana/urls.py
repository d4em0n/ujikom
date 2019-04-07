from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),
    path('dashboard/barang/', views.BarangListView.as_view(), name='barang'),
    path('dashboard/barang/<int:pk>/', views.BarangDetailView.as_view(), name='detail_barang'),
    path('dashboard/barang/<int:pk>/edit', views.BarangUpdateView.as_view(), name='edit_barang'),
    path('dashboard/barang/<int:pk>/delete', views.BarangDeleteView.as_view(), name='delete_barang'),
    path('dashboard/barang/entri/', views.BarangCreateView.as_view(), name='entri_barang'),
    path('dashboard/barang/<int:id_barang>/pinjam', views.PeminjamanCreateView.as_view(), name='pinjam_barang'),
    path('dashboard/barang_keluar/', views.DataBarangKeluarListView.as_view(), name='data_barang_keluar'),
    path('dashboard/barang/<int:id_barang>/keluar', views.BarangKeluarCreateView.as_view(), name='keluar_barang'),
    path('dashboard/pinjam/', views.PeminjamanListView.as_view(), name='pinjam'),
    path('dashboard/data_pinjam/', views.DataPinjamBarangListView.as_view(), name='data_barang_pinjam'),
    path('dashboard/pinjam/<int:pk>/', views.PeminjamanDetailView.as_view(), name='detail_pinjam'),
    path('dashboard/pinjam/<int:pk>/edit', views.PeminjamanUpdateView.as_view(), name='edit_pinjam'),
    path('dashboard/pinjam/<int:pk>/delete', views.PeminjamanDeleteView.as_view(), name='delete_pinjam'),
    path('dashboard/suplier/', views.SuplierListView.as_view(), name='suplier'),
    path('dashboard/suplier/create', views.SuplierCreateView.as_view(), name='entri_suplier'),
    path('dashboard/suplier/<int:pk>/', views.SuplierDetailView.as_view(), name='detail_suplier'),
    path('dashboard/suplier/<int:pk>/edit', views.SuplierUpdateView.as_view(), name='edit_suplier'),
    path('dashboard/suplier/<int:pk>/delete', views.SuplierDeleteView.as_view(), name='delete_suplier'),
    path('dashboard/suplier/<int:id_suplier>/entri_barang_masuk', views.BarangMasukCreateView.as_view(), name='entri_barang_masuk'),
]