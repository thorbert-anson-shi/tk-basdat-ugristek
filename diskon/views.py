from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse
from datetime import datetime as dt
from datetime import timedelta as td
import json

# Fungsi untuk tampilkan halaman diskon beserta data voucher dan promo.
def show_hal_diskon(request):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public,sijarta;")
        cursor.execute("SELECT * FROM diskon d JOIN voucher v ON d.Kode = v.Kode;")
        vouchers = cursor.fetchall()
        cursor.execute("SELECT * FROM promo;")
        promo = cursor.fetchall()

    context = {
        'data_voucher': vouchers,
        'data_promo': promo,
        'saldo_pengguna': get_user_balance(request)
    }

    return render(request, "diskon/hal_diskon.html", context)

# Fungsi untuk insert TR_PEMBELIAN_VOUCHER baru dan update saldo pengguna.
def insert_pembelian_voucher(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data sent in the request body
            data = json.loads(json.loads(request.body.decode('utf-8')))

            # Akses nilai dari dictionary json supaya bisa dipakai.
            kode_voucher = data["kode_voucher"]
            harga_beli_voucher = data["harga_beli_voucher"]
            hari_berlaku = data["hari_berlaku"]
            metode_pembayaran = data["metode_pembayaran"]
            
            # Raw SQL query to insert the voucher status
            sql_query_insert = '''
                INSERT INTO tr_pembelian_voucher (TglAwal, TglAkhir, TelahDigunakan, IdPelanggan, IdVoucher, idMetodeBayar) VALUES
                (%s, %s, 0, %s, %s, %s);
            '''
            tgl_awal = dt.date(dt.now())
            tgl_akhir = dt.date(dt.now()) + td(days = hari_berlaku)
            id_pelanggan = get_user_id(request)
            id_voucher = kode_voucher

            sql_query_cari_id_metode = '''
                SELECT Id FROM metode_bayar WHERE Nama = %s;
            '''

            with connection.cursor() as cursor:
                cursor.execute("SET search_path TO public,sijarta;")
                cursor.execute(sql_query_cari_id_metode, [metode_pembayaran])
                hasil_cari_id = cursor.fetchone()
                if hasil_cari_id:
                    id_metode_bayar = hasil_cari_id[0]
                    cursor.execute(sql_query_insert, [tgl_awal, tgl_akhir, id_pelanggan, id_voucher, id_metode_bayar])
                    update_user_balance(request, -harga_beli_voucher, id_pelanggan)

                # Kembalikan pesan error ketika tidak menemukan id yang dicari.
                else: 
                    return JsonResponse({'status': 'error', 'message': 'Metode pembayaran tidak ditemukan'}, status=404)
                
            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'Voucher purchase data received successfully'})

        except json.JSONDecodeError:
            # Handle errors if JSON is malformed
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# Fungsi untuk mengambil saldo dan id user
def get_user_balance(request):
    balance = request.session["user"]["saldo"]
    return balance

def get_user_id(request):
    user_id = request.session["user"]["id"]
    return user_id

# Fungsi untuk update saldo user di sesi dan backend sql.
def update_user_balance(request, delta, id_pelanggan):
    # Periksa apakah user ada dalam sesi ini.
    if "user" in request.session:
        
        # Eksekusi query untuk update saldo my pay user
        query_ambil_saldo_mypay = '''
            SELECT saldoMyPay FROM users WHERE Id = %s;
        '''
        query_update_saldo_mypay = '''
            UPDATE users SET SaldoMyPay = %s WHERE Id = %s;
        '''
        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public,sijarta;")
            cursor.execute(query_ambil_saldo_mypay, [id_pelanggan])
            new_balance = cursor.fetchone()[0] + delta
            cursor.execute(query_update_saldo_mypay, [new_balance, id_pelanggan])
            cursor.execute(query_ambil_saldo_mypay, [id_pelanggan])
            new_balance_yare = cursor.fetchone()[0]
            request.session["user"]["saldo"] = new_balance_yare

        # Kembalikan pesan sesuai hasilnya, antara sukses atau error.
        return JsonResponse({'status': 'success', 'message': 'User balance updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'User session not found'}, status=400)


def update_voucher_usage(request, kode_diskon):
    user_id = get_user_id(request)
    kode_diskon_yare = kode_diskon
    query_cari_voucher_update = '''
        SELECT Id FROM tr_pembelian_voucher WHERE IdPelanggan = %s AND IdVoucher = %s LIMIT 1;
    '''
    query_update_voucher_usage = '''
        UPDATE tr_pembelian_voucher SET TelahDigunakan = TelahDigunakan + 1 WHERE Id = %s;
    '''

    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public,sijarta;")
        cursor.execute(query_cari_voucher_update, [user_id, kode_diskon_yare])
        id_transaksi = cursor.fetchone()[0]
        cursor.execute(query_update_voucher_usage, [id_transaksi])
