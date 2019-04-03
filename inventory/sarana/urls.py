from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),
    path('dashboard/barang/', views.BarangListView.as_view(), name='barang'),
    path('dashboard/barang/<int:pk>/', views.BarangDetailView.as_view(), name='detail_barang'),
    path('dashboard/barang/<int:pk>/edit', views.BarangUpdateView.as_view(), name='edit_barang'),
    path('dashboard/barang/entri/', views.BarangCreateView.as_view(), name='entri_barang'),
]
