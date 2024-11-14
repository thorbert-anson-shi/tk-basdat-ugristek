from django.shortcuts import render
from django.db import connection

# Fungsi untuk tampilkan halaman diskon beserta data voucher dan promo.
def show_hal_diskon(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM diskon d JOIN voucher v ON d.Kode = v.Kode")
        voucher = cursor.fetchall()
        cursor.execute("SELECT * FROM promo")
        promo = cursor.fetchall()

    context = {
        'data_voucher': voucher,
        'data_promo': promo,
    }

    return render(request, "hal_diskon.html", context)