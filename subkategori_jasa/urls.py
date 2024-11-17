from django.urls import path
from . import views

urlpatterns = [
    path('pelanggan/<uuid:subkategori_id>/', views.subkategori_jasa_pelanggan, name='subkategori_jasa_pelanggan'),
    path('pekerja/<uuid:subkategori_id>/', views.subkategori_jasa_pekerja, name='subkategori_jasa_pekerja'),
    path('pekerja/<uuid:subkategori_id>/bergabung/', views.bergabung_kategori_jasa, name='bergabung_kategori_jasa'),
    path('buat_pemesanan_jasa/', views.buat_pemesanan_jasa, name='buat_pemesanan_jasa'),
    path('profil_pekerja/<uuid:pekerja_id>/', views.profil_pekerja, name='pekerja_profil'),
    path('view_pemesanan_jasa/', views.view_pemesanan_jasa, name='view_pemesanan_jasa'),
    path('batalkan_pemesanan_jasa/<uuid:pemesanan_id>/', views.batalkan_pemesanan_jasa, name='batalkan_pemesanan_jasa'),

]
