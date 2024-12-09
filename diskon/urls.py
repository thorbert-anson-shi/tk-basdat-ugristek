from django.urls import path
from diskon.views import show_hal_diskon, insert_pembelian_voucher

app_name = 'diskon'

urlpatterns = [
    path('', show_hal_diskon, name='show_hal_diskon'),
    path('insert-pembelian-voucher/', insert_pembelian_voucher, name='insert_pembelian_voucher'),
]