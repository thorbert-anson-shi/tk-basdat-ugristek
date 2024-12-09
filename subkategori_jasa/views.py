from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .queries import *
from uuid import UUID
import uuid
from datetime import datetime

def run(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [col[0] for col in cursor.description]
        return [
            dict(
                zip(
                    columns, 
                    [str(col) if isinstance(col, UUID) else col for col in row]
                )
            )
            for row in cursor.fetchall()
            ]

# yang bisa akses subkategori jasa cuman yg udah login
# @login_required
def subkategori_jasa(request, subkategori_id):
    with connection.cursor() as cursor:
        cursor.execute(set_syntax())

    subkategori = run(
        subkategori_syntax(subkategori_id)
        )
    
    if subkategori:
        subkategori = subkategori[0]
    
    kategori = run(
        kategori_syntax(subkategori_id)
        )
    
    if kategori:
        kategori = kategori[0]
    
    sesi_layanan = run(
        sesi_layanan_syntax(subkategori_id)
        )
    
    pekerja_list = run(
        pekerja_list_syntax(subkategori_id)
        )
    
    terdaftar = run(
        terdaftar_syntax(
            request.session.get('user').get('id'), 
            subkategori['kategorijasaid']
            )
        )
    testimoni_list = run(
        testimoni_list_syntax(subkategori_id)
        )
    
    metode_bayar_list = run(
        metode_bayar_list_syntax()
        )
        
    context = {
        'subkategori': subkategori,
        'kategori': kategori,
        'sesi_layanan': sesi_layanan,
        'pekerja_list': pekerja_list,
        'terdaftar': terdaftar,
        'testimoni_list': testimoni_list,
        'metode_bayar_list': metode_bayar_list,
        "user": request.session.get("user", None),
        'subkategori_id': subkategori_id,
    }

    # print(kategori)
    print("====================")
    # print(sesi_layanan)
    print(testimoni_list)

    return render(request, "subkategori_jasa/display_subkategori.html", context)

# @login_required
def pesan_jasa(request):
    if request.method == "POST":
        subkategori_id = request.POST.get('subkategori_id')
        sesi_harga = int(request.POST.get('sesi_harga'))
        metode_bayar = request.POST.get('metode_bayar')
        kode_diskon = request.POST.get('kode_diskon', None)
        tanggal_pemesanan = request.POST.get('tanggal_pemesanan')
        sesi_sesi = request.POST.get('sesi_sesi')

        transaksi_baru_id = uuid.uuid4()
        curr_tgl = datetime.now()

        try:
            curr_potongan = 0
            if kode_diskon:
                with connection.cursor() as cursor:
                    diskon = run(select_diskon_val_syntax(kode_diskon))
                    print(diskon)

                if diskon:
                    potongan = diskon["potongan"]
                    min_tr = diskon["mintrpemesanan"]

                    if sesi_harga >= min_tr:
                        curr_potongan = potongan
                    else:
                        return JsonResponse({
                            "success": False,
                            "message": "Transaksi kurang dari syarat minimum harga transaksi untuk mengaplikasikan potongan",
                        },
                        status=400
                        )
                else:
                    return JsonResponse({
                        "success": False,
                        "message": "Kode diskon invalid atau sudah expired"
                    },
                    status=400
                    )
            
            final_harga = max(0, sesi_harga-curr_potongan)

            # nanti ganti id-nya
            if metode_bayar == 'daedfde6-91df-4090-b40a-e0dd26650696':
                id_status_pesanan = '877a2841-c396-451c-a51b-915fd36731ed'
            else:
                id_status_pesanan = ''

            with connection.cursor() as cursor:
                if kode_diskon:
                    cursor.execute(tambah_tr_pemesanan_jasa_berdiskon(), (
                        transaksi_baru_id,
                        request.session.get('user').get('id'),
                        subkategori_id,
                        sesi_sesi,
                        tanggal_pemesanan,
                        final_harga,
                        tanggal_pemesanan,
                        tanggal_pemesanan,
                        metode_bayar,
                        kode_diskon,
                    ))
                else:
                    cursor.execute(tambah_tr_pemesanan_jasa_tanpadiskon(), (
                        transaksi_baru_id,
                        request.session.get('user').get('id'),
                        subkategori_id,
                        sesi_sesi,
                        tanggal_pemesanan,
                        final_harga,
                        tanggal_pemesanan,
                        tanggal_pemesanan,
                        metode_bayar,
                    ))

                cursor.execute(tr_tambah_pemesanan_status(),
                                (transaksi_baru_id, 
                                 id_status_pesanan,
                                 curr_tgl)
                               )
            
            return redirect('subkategori_jasa:form_pemesanan_jasa')
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse(
                {
                    "success": False,
                    "message": "Terjadi galat saat pesan jasa"
                }
            )
        
    return JsonResponse({
        "success": False,
        "message": "Metode pembayaran invalid",
    })

# @login_required
def bergabung(request, kategori_id):
    if request.method=="POST":
        user_id = request.session.get('user').get("id")

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    cek_pekerja(),
                    (user_id, kategori_id)
                )

                telah_bergabung = cursor.fetchone()[0]

                if telah_bergabung:
                    return JsonResponse({
                        "success": False,
                        "message": "Anda sudah bergabung di kategori ini"
                    })
                
                cursor.execute(
                    tambah_pekerja(),
                    (user_id, kategori_id)
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Anda berhasil bergabung di kategori ini'
            })
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                'success': False,
                'message': "Terjadi galat saat bergabung"
            })
        
    return JsonResponse({
        'success': False,
        'message': 'Invalid request. Please try it again'
    },
    status=405
    )


# @login_required
def form_pemesanan_jasa(request):
    user_id = request.session.get('user').get("id")
    daftar_pesanan, filter_subkategori, filter_status = [], [], []

    selected_subkategori=request.GET.get("subkategori", "")
    selected_status=request.GET.get("status", "")

    try:
        with connection.cursor() as cursor:
            display_daftar_pemesanan_syntax = """
                SELECT 
                    SKJ.namasubkategori AS subkategori,
                    TPJ.sesi AS sesi_sesi,
                    TPJ.totalbiaya AS sesi_harga,
                    COALESCE(U.nama, "Belum Ada Pekerja") AS nama_pekerja,
                    TPSSP.status AS statuspesanan,
                    TPJ.id AS pesanan_id,
                    (CASE WHEN EXISTS (
                        SELECT 1
                        FROM testimoni T
                        WHERE T.idtrpemesanan = TPJ.id
                    ) THEN TRUE ELSE FALSE END
                    ) AS testimonidibuat
                FROM tr_pemesanan_jasa TPJ
                LEFT JOIN subkategori_jasa SKJ ON SKJ.id = TPJ.idkategorijasa
                LEFT JOIN pekerja P ON P.id = TPJ.idpekerja
                LEFT JOIN users U ON U.id = P.id
                LEFT JOIN (
                    SELECT DISTINCT
                        ON (TPS.idtrpemesanan)
                        TPS.idtrpemesanan,
                        SP.status
                    FROM tr_pemesanan_status TPS
                    JOIN status_pesanan SP ON SP.id = TPS.idstatus
                    ORDER BY TPS.idtrpemesanan, TPS.tglwaktu DESC
                ) TPSSP ON TPJ.id = TPSSP.idtrpemesanan
                WHERE TPJ.idpelanggan = %s
            """

            filter_subkategori_query = """
                SELECT DISTINCT namasubkategori
                FROM subkategori_jasa;
            """

            filter_status_query = """
                SELECT DISTINCT status
                FROM status_pesanan;
            """

            params=[user_id]

            if selected_subkategori:
                display_daftar_pemesanan_syntax+=" AND SKJ.namasubkategori = %s"
                params.append(selected_subkategori)
            if selected_status:
                display_daftar_pemesanan_syntax+=" AND TPSSP.status = %s"
                params.append(selected_status)

            cursor.execute(display_daftar_pemesanan_syntax, params)
            rows = cursor.fetchall()

            for row in rows:
                daftar_pesanan.append({
                    'subkategori': row[0],
                    'sesi_sesi': row[1],
                    'sesi_harga': row[2],
                    'nama_pekerja': row[3],
                    'status': row[4],
                    'pesanan_id': row[5],
                    'testimoni_dibuat': row[6],
                })

            cursor.execute(filter_subkategori_query)
            filter_subkategori = [row[0] for row in cursor.fetchall()]

            cursor.execute(filter_status_query)
            filter_status = [row[0] for row in cursor.fetchall()]

    except Exception as e:
        print(f"Error: {e}")

    context = {
        "daftar_pesanan": daftar_pesanan,
        "filter_subkategori": filter_subkategori,
        "filter_status": filter_status,
        "selected_subkategori": selected_subkategori,
        "selected_status": selected_status,
    }

    return render(request, "subkategori_jasa/form_pemesanan_jasa.html", context)
    


# @login_required
def batalkan_pesanan(request):
    if request.method == "POST":
        pesanan_id = request.POST.get("pesanan_id")

        if not pesanan_id:
            return JsonResponse({
                "success": False,
                "message": "Invalid ID Pesanan"
            })
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(delete_status_syntax, (pesanan_id))
                cursor.execute(delete_pesanan_syntax, (pesanan_id))

            return JsonResponse({
                "success": True,
                "message": "Pesanan berhasil di-cancel"
            })
        
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                "success":False,
                "message": "Terjadi galat saat percobaan cancel pesanan dilakukan"
            })
        
    return JsonResponse({
        "success": False,
        "message": "Metode request invalid"
    })

# @login_required
def show_form_testimoni(request):
    return render(request, "subkategori_jasa/form_testimoni.html")