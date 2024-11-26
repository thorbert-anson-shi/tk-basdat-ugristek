from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse
from datetime import datetime as dt
from datetime import timedelta as td

# Fungsi untuk tampilkan halaman diskon beserta data voucher dan promo.
def show_hal_diskon(request):

    # TODO: Uncomment after fixing front end.
    # with connection.cursor() as cursor:
    #     cursor.execute(
        
    #       "SELECT * FROM diskon d JOIN voucher v ON d.Kode = v.Kode";)
    #     voucher = cursor.fetchall()
    #     cursor.execute("SELECT * FROM promo";)
    #     promo = cursor.fetchall()

    # context = {
    #     'data_voucher': voucher,
    #     'data_promo': promo,
    # }

    # return render(request, "hal_diskon.html", context)
    return render(request, "hal_diskon.html")

# Fungsi untuk insert TR_PEMBELIAN_VOUCHER baru.
def insert_pembelian_voucher(request):
    # Get voucher ID from POST request data
    voucher_id = request.POST.get('voucherId')
    user_id = request.POST.get('userId')
    payment_method_id = request

    # Check if voucher_id is provided
    if not voucher_id:
        return JsonResponse({'success': False, 'message': 'Voucher id required'}, status=400)
    
    if not user_id:
        return JsonResponse({'success': False, 'message': 'User id required'}, status=400)

    '''
    INSERT INTO tr_pembelian_voucher (TglAwal, TglAkhir, TelahDigunakan, IdPelanggan, IdVoucher, IdMetodeBayar) VALUES
    ('2024-09-10', '2024-10-10', 0, (SELECT Id FROM pelanggan WHERE Id = (SELECT Id FROM users WHERE Nama = 'Dengklek')), 'VOUC1000', (SELECT Id FROM metode_bayar WHERE Nama = 'MyPay')),
    '''

    # TODO: Figure out how to increment during usage
    # Raw SQL query to inserta the voucher status
    sql_query = '''
        INSERT INTO tr_pembelian_voucher (TglAwal, TglAkhir, TelahDigunakan, IdPelanggan, IdVoucher, idMetodeBayar) VALUES
        ('%s', '%s', 0, '%s', '%s', '%s');
    '''

    # TODO: Extract idMetodeBayar
    # Execute the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [dt.date(dt.now()), dt.date(dt.now()) + td(days=30), user_id, voucher_id])

    return JsonResponse({'success': True, 'message': 'Voucher updated successfully'})

# TODO: Get the user's balance later after auth is fix
def get_user_balance(request):
    return HttpResponse(1)