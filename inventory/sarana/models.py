from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls.base import reverse

# Create your models here.

class User(AbstractUser):
    PERM_LEVEL = (
        (0, 'Administrator'),
        (1, 'Manajemen'),
        (2, 'Peminjam')
    )
    level = models.IntegerField(default=2, choices=PERM_LEVEL)

class Barang(models.Model):
    KONDISI_BARANG = (
        ('A', 'Baik'),
        ('B', 'Kurang baik berfungsi'),
        ('C', 'Rusak'),
    )
    id_barang = models.AutoField(primary_key=True)
    nama_barang = models.CharField(max_length=100)
    spesifikasi = models.CharField(max_length=255)
    lokasi = models.CharField(max_length=60)
    kondisi = models.CharField(max_length=1, default='A', choices=KONDISI_BARANG)
    jumlah_barang = models.IntegerField(default=1)
    sumber_dana = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('detail_barang', args=[self.id_barang])

class PinjamBarang(models.Model):
    id_pinjam = models.AutoField(primary_key=True)
    peminjam = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pinjaman')
    tgl_pinjam = models.DateField(auto_now_add=True)
    jml_dipinjam = models.IntegerField(default=1)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, related_name='dipinjam')
    tgl_kembali = models.DateField()

    def get_absolute_url(self):
        return reverse('detail_barang', args=[self.barang.id_barang])

class StokBarang(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, related_name='stok')
    jml_masuk = models.IntegerField()
    jml_keluar = models.IntegerField()

class BarangKeluar(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, related_name='barang_keluar')
    tgl_keluar = models.DateField(auto_now_add=True)
    jml_keluar = models.IntegerField(default=1)
    lokasi = models.CharField(max_length=100)
    penerima = models.ForeignKey(User, on_delete=models.CASCADE, related_name='barang_keluar')

class Suplier(models.Model):
    id_suplier = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    alamat = models.CharField(max_length=70)
    telepon = models.CharField(max_length=15)
    
class BarangMasuk(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, related_name='barang_masuk')
    tgl_masuk = models.DateField(auto_now_add=True)
    jml_masuk = models.IntegerField(default=1)
    suplier = models.ForeignKey(Suplier, on_delete=models.CASCADE, related_name='barang_masuk')