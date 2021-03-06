# Generated by Django 2.1.7 on 2019-04-01 04:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sarana', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barang',
            fields=[
                ('id_barang', models.AutoField(primary_key=True, serialize=False)),
                ('nama_barang', models.CharField(max_length=100)),
                ('spesifikasi', models.CharField(max_length=255)),
                ('lokasi', models.CharField(max_length=60)),
                ('kondisi', models.CharField(choices=[('A', 'Baik'), ('B', 'Kurang baik berfungsi'), ('C', 'Rusak')], default='A', max_length=1)),
                ('jumlah_barang', models.IntegerField(default=1)),
                ('sumber_dana', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BarangKeluar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl_keluar', models.DateField(auto_now_add=True)),
                ('jml_keluar', models.IntegerField(default=1)),
                ('lokasi', models.CharField(max_length=100)),
                ('barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barang_keluar', to='sarana.Barang')),
                ('penerima', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barang_keluar', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BarangMasuk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl_masuk', models.DateField(auto_now_add=True)),
                ('jml_masuk', models.IntegerField(default=1)),
                ('barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barang_masuk', to='sarana.Barang')),
            ],
        ),
        migrations.CreateModel(
            name='PinjamBarang',
            fields=[
                ('id_pinjam', models.AutoField(primary_key=True, serialize=False)),
                ('tgl_pinjam', models.DateField(auto_now_add=True)),
                ('jml_dipinjam', models.IntegerField(default=1)),
                ('tgl_kembali', models.DateField()),
                ('barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dipinjam', to='sarana.Barang')),
                ('peminjam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pinjaman', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StokBarang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jml_masuk', models.IntegerField()),
                ('jml_keluar', models.IntegerField()),
                ('barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stok', to='sarana.Barang')),
            ],
        ),
        migrations.CreateModel(
            name='Suplier',
            fields=[
                ('id_suplier', models.AutoField(primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=50)),
                ('alamat', models.CharField(max_length=70)),
                ('telepon', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='barangmasuk',
            name='suplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barang_masuk', to='sarana.Suplier'),
        ),
    ]
