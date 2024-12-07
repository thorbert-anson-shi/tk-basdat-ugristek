from django.urls import path
from . import views

app_name = 'subkategori_jasa'

urlpatterns = [
    path('pelanggan/', views.subkategori_jasa_pelanggan, name='subkategori_jasa_pelanggan'),
    path('pekerja/', views.subkategori_jasa_pekerja, name='subkategori_jasa_pekerja'),
    # path('pekerja/bergabung/', views.bergabung_subkategori_jasa, name='bergabung_subkategori_jasa'),
    # path('buat_pemesanan_jasa/', views.buat_pemesanan_jasa, name='buat_pemesanan_jasa'),

    # path('profil_pekerja/<str:pekerja_id>/', views.profil_pekerja, name='profil_pekerja'),#bakal dilink ke danniel punya
    # path('view_pemesanan_jasa/', views.view_pemesanan_jasa, name='view_pemesanan_jasa'),
    # path('batalkan_pemesanan_jasa/<str:pemesanan_id>/', views.batalkan_pemesanan_jasa, name='batalkan_pemesanan_jasa'),

    path('form_testimoni/<str:subkategori_id>/', views.show_form_testimoni, name='form_testimoni'),
]
