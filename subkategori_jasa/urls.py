from django.urls import path
from subkategori_jasa.views import *

app_name = 'subkategori_jasa'

urlpatterns = [
    path('pesan_jasa/', pesan_jasa, name='pesan_jasa'),
    path('<str:subkategori_id>/', subkategori_jasa, name='subkategori_jasa'),
    path('bergabung/<str:kategori_id>/', bergabung, name='bergabung'),
    path('form_pemesanan_jasa/', form_pemesanan_jasa, name='form_pemesanan_jasa'),
    path('form_pemesanan_jasa/batalkan_pesanan', batalkan_pesanan, name='batalkan_pesanan'),
    path('form_testimoni/<str:subkategori_id>/', show_form_testimoni, name='form_testimoni'),
]
