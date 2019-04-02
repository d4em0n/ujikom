from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, UserCreationForm, UserChangeForm
from .models import User, Barang, PinjamBarang, BarangMasuk, BarangKeluar, Suplier, StokBarang
from django.utils.translation import ugettext_lazy as _


# Register your models here.

class CustomUserChangeForm(UserChangeForm):
    # TODO
    # Fitur untuk membuat field group permission otomatis terubah ketika field
    # level berubah
    pass

class CustomUserCreationForm(UserCreationForm):
    def save(self, commit=True):
        perm_level = ['Administrator', 'Manajemen', 'Peminjam']
        user = super().save(commit=True)
        user.groups.add(Group.objects.get(name=perm_level[user.level]))
        user.save()
        return user

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'level')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'level')}
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Barang)
admin.site.register(PinjamBarang)
admin.site.register(BarangMasuk)
admin.site.register(BarangKeluar)
admin.site.register(StokBarang)
admin.site.register(Suplier)
