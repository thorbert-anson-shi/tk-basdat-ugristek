from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .dummy_data import (
    DUMMY_PENGGUNA,
    DUMMY_PELANGGAN,
    DUMMY_PEKERJA,
    DUMMY_KATEGORI_JASA,
    DUMMY_SUBKATEGORI_JASA,
    DUMMY_PEKERJA_KATEGORI_JASA,
    DUMMY_SESI_LAYANAN,
    DUMMY_METODE_BAYAR,
    DUMMY_DISKON,
    DUMMY_VOUCHER,
    DUMMY_PROMO,
    DUMMY_TR_PEMESANAN_JASA,
    DUMMY_TESTIMONI,
    DUMMY_STATUS_PESANAN,
    DUMMY_TR_PEMESANAN_STATUS,
    DUMMY_MYPAY
)
import uuid
from datetime import datetime


def get_user_by_id(user_id):
    for user in DUMMY_PENGGUNA:
        if user["id"] == user_id:
            return user
    return None

def get_pelanggan_by_id(user_id):
    for pelanggan in DUMMY_PELANGGAN:
        if pelanggan["id"] == user_id:
            return pelanggan
    return None

def get_pekerja_by_id(pekerja_id):
    for pekerja in DUMMY_PEKERJA:
        if pekerja["id"] == pekerja_id:
            return pekerja
    return None

def get_subkategori_jasa_by_id(subkategori_id):
    for subkategori in DUMMY_SUBKATEGORI_JASA:
        if subkategori["id"] == subkategori_id:
            return subkategori
    return None

def get_kategori_jasa_by_id(kategori_jasa_id):
    for kategori in DUMMY_KATEGORI_JASA:
        if kategori["id"] == kategori_jasa_id:
            return kategori
    return None

def get_sesi_layanan_by_subkategori(subkategori_id):
    return [sesi for sesi in DUMMY_SESI_LAYANAN if sesi["subkategori_id"] == subkategori_id]

def get_metode_bayar():
    return DUMMY_METODE_BAYAR

def get_diskon_by_kode(kode_diskon):
    for diskon in DUMMY_DISKON:
        if diskon["kode"] == kode_diskon:
            return diskon
    return None

def get_voucher_by_kode(kode_voucher):
    for voucher in DUMMY_VOUCHER:
        if voucher["kode"] == kode_voucher:
            return voucher
    return None

def get_tr_pemesanan_jasa_by_id(pemesanan_id):
    for pemesanan in DUMMY_TR_PEMESANAN_JASA:
        if pemesanan["id"] == pemesanan_id:
            return pemesanan
    return None

def get_status_pesanan_by_keterangan(keterangan):
    for status in DUMMY_STATUS_PESANAN:
        if status["keterangan"] == keterangan:
            return status
    return None

def get_tr_pemesanan_status_by_id_tr_pemesanan(pemesanan_id):
    for status in DUMMY_TR_PEMESANAN_STATUS:
        if status["id_tr_pemesanan"] == pemesanan_id:
            return status
    return None

def get_testimoni_by_id_tr_pemesanan(pemesanan_id):
    return [testimoni for testimoni in DUMMY_TESTIMONI if testimoni["id_tr_pemesanan"] == pemesanan_id]

def get_pekerja_list_by_kategori_jasa(kategori_jasa_id):
    pekerja_ids = [pkj["pekerja_id"] for pkj in DUMMY_PEKERJA_KATEGORI_JASA if pkj["kategori_jasa_id"] == kategori_jasa_id]
    return [pekerja for pekerja in DUMMY_PEKERJA if pekerja["id"] in pekerja_ids]

def get_pemesanan_jasa_by_pelanggan(pelanggan_id):
    return [p for p in DUMMY_TR_PEMESANAN_JASA if p["id_pelanggan"] == pelanggan_id]


def get_user_role(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return 'unknown'
    
    if user["role"] == "pelanggan":
        return 'pelanggan'
    elif user["role"] == "pekerja":
        return 'pekerja'
    else:
        return 'unknown'


def subkategori_jasa_pelanggan(request, subkategori_id):
    user = get_user_by_id(request.user.id)
    if not user:
        return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
    user_role = get_user_role(request.user.id)
    if user_role != 'pelanggan':
        return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")

    subkategori = get_subkategori_jasa_by_id(subkategori_id)
    if not subkategori:
        return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})
    
    nama_subkategori = subkategori["nama_subkategori"]
    deskripsi = subkategori["deskripsi"]
    kategori_jasa_id = subkategori["kategori_jasa_id"]

    pekerja_list = get_pekerja_list_by_kategori_jasa(kategori_jasa_id)
    sesi_layanan = get_sesi_layanan_by_subkategori(subkategori_id)
    metode_bayar = get_metode_bayar()

    context = {
        'nama_subkategori': nama_subkategori,
        'deskripsi': deskripsi,
        'pekerja_list': pekerja_list,
        'sesi_layanan': sesi_layanan,
        'subkategori_id': subkategori_id,
        'metode_bayar_list': metode_bayar,
    }

    return render(request, 'subkategori_jasa/pelanggan.html', context)


def subkategori_jasa_pekerja(request, subkategori_id):
    user = get_user_by_id(request.user.id)
    if not user:
        return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
    user_role = get_user_role(request.user.id)
    if user_role != 'pekerja':
        return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")

    subkategori = get_subkategori_jasa_by_id(subkategori_id)
    if not subkategori:
        return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})
    
    nama_subkategori = subkategori["nama_subkategori"]
    deskripsi = subkategori["deskripsi"]
    kategori_jasa_id = subkategori["kategori_jasa_id"]

    pekerja_list = get_pekerja_list_by_kategori_jasa(kategori_jasa_id)
    testimoni = []
    for pemesanan in get_pemesanan_jasa_by_pelanggan(user["id"]):
        testimoni += get_testimoni_by_id_tr_pemesanan(pemesanan["id"])

    sesi_layanan = get_sesi_layanan_by_subkategori(subkategori_id)

    # Cek apakah pekerja sudah bergabung dengan kategori jasa ini
    is_joined = any(
        pkj for pkj in DUMMY_PEKERJA_KATEGORI_JASA 
        if pkj["pekerja_id"] == user["id"] and pkj["kategori_jasa_id"] == kategori_jasa_id
    )

    context = {
        'nama_subkategori': nama_subkategori,
        'deskripsi': deskripsi,
        'pekerja_list': pekerja_list,
        'testimoni': testimoni,
        'sesi_layanan': sesi_layanan,
        'subkategori_id': subkategori_id,
        'is_joined': is_joined,
    }

    return render(request, 'subkategori_jasa/pekerja.html', context)

def bergabung_kategori_jasa(request, subkategori_id):
    user = get_user_by_id(request.user.id)
    if not user:
        return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
    user_role = get_user_role(request.user.id)
    if user_role != 'pekerja':
        return HttpResponseForbidden("Not Allowed!")
    
    subkategori = get_subkategori_jasa_by_id(subkategori_id)
    if not subkategori:
        return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})
    kategori_jasa_id = subkategori["kategori_jasa_id"]
    
    # Cek apakah pekerja sudah bergabung
    already_joined = any(
        pkj for pkj in DUMMY_PEKERJA_KATEGORI_JASA 
        if pkj["pekerja_id"] == user["id"] and pkj["kategori_jasa_id"] == kategori_jasa_id
    )
    
    if already_joined:
        return redirect('subkategori_jasa_pekerja', subkategori_id=subkategori_id)
    
    # Bergabung dengan kategori jasa
    new_pkj = {
        "pekerja_id": user["id"],
        "kategori_jasa_id": kategori_jasa_id
    }
    DUMMY_PEKERJA_KATEGORI_JASA.append(new_pkj)
    
    return redirect('subkategori_jasa_pekerja', subkategori_id=subkategori_id)

def buat_pemesanan_jasa(request):
    user = get_user_by_id(request.user.id)
    if not user:
        return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
    user_role = get_user_role(request.user.id)
    if user_role != 'pelanggan':
        return HttpResponseForbidden("Anda tidak memiliki izin untuk melakukan aksi ini.")
    
    if request.method == 'POST':
        subkategori_id = request.POST.get('subkategori_id')
        sesi = request.POST.get('sesi')
        harga = request.POST.get('harga')
        tanggal_pemesanan = request.POST.get('tanggal_pemesanan')
        kode_diskon = request.POST.get('kode_diskon').strip() or None
        id_metode_bayar = request.POST.get('metode_bayar')
        
        # Validasi input
        if not all([subkategori_id, sesi, harga, tanggal_pemesanan, id_metode_bayar]):
            return render(request, 'subkategori_jasa/error.html', {'message': 'Data pemesanan tidak lengkap.'})
        
        # Validasi subkategori_jasa
        subkategori = get_subkategori_jasa_by_id(subkategori_id)
        if not subkategori:
            return render(request, 'subkategori_jasa/error.html', {'message': 'Subkategori tidak ditemukan.'})
        
        # Inisialisasi variabel diskon
        potongan = 0.0
        id_diskon = None

        # Validasi voucher atau promo
        if kode_diskon:
            diskon = get_diskon_by_kode(kode_diskon)
            if not diskon:
                return render(request, 'subkategori_jasa/error.html', {'message': 'Kode diskon tidak valid.'})
            
            potongan = diskon["potongan"]
            min_tr_pemesanan = diskon["min_tr_pemesanan"]
            
            # Cek syarat pemesanan minimal
            pemesanan_sebelumnya = get_pemesanan_jasa_by_pelanggan(user["id"])
            if len(pemesanan_sebelumnya) < min_tr_pemesanan:
                return render(request, 'subkategori_jasa/error.html', {'message': 'Tidak memenuhi syarat pemesanan minimal untuk diskon ini.'})
            
            # Cek voucher
            voucher = get_voucher_by_kode(kode_diskon)
            if not voucher:
                return render(request, 'subkategori_jasa/error.html', {'message': 'Voucher tidak ditemukan.'})
            
            # Memeriksa pembatasan penggunaan voucher
            if voucher["jml_hari_berlaku"] <= 0:
                return render(request, 'subkategori_jasa/error.html', {'message': 'Voucher sudah kedaluwarsa.'})
            
            if voucher["kuota_penggunaan"] <= 0:
                return render(request, 'subkategori_jasa/error.html', {'message': 'Kuota penggunaan voucher sudah habis.'})
            
            # Hitung potongan (asumsi potongan adalah persentase)
            total_biaya = float(harga) - (potongan * float(harga) / 100)
            id_diskon = kode_diskon
            
            # Kurangi kuota penggunaan voucher
            for v in DUMMY_VOUCHER:
                if v["kode"] == kode_diskon:
                    v["kuota_penggunaan"] -= 1
                    break
        else:
            total_biaya = float(harga)
        
        if total_biaya < 0:
            total_biaya = 0.0
        
        # Ambil pekerja pertama yang tersedia
        pekerja_list = get_pekerja_list_by_kategori_jasa(subkategori["kategori_jasa_id"])
        if not pekerja_list:
            return render(request, 'subkategori_jasa/error.html', {'message': 'Tidak ada pekerja yang tersedia untuk subkategori ini.'})
        
        pekerja_id = pekerja_list[0]["id"]
        
        # Buat ID unik untuk pemesanan
        pemesanan_id = str(uuid.uuid4())
        
        # Buat pemesanan baru
        new_pemesanan = {
            "id": pemesanan_id,
            "tgl_pemesanan": datetime.strptime(tanggal_pemesanan, "%Y-%m-%d"),
            "tgl_pekerjaan": datetime.strptime(tanggal_pemesanan, "%Y-%m-%d"),  # Asumsi sama dengan tgl_pemesanan
            "waktu_pekerjaan": datetime.strptime(tanggal_pemesanan, "%Y-%m-%d").replace(hour=12, minute=0, second=0),
            "total_biaya": total_biaya,
            "id_pelanggan": user["id"],
            "id_pekerja": pekerja_id,
            "id_kategori_jasa": subkategori["kategori_jasa_id"],
            "sesi": sesi,
            "id_diskon": id_diskon,
            "id_metode_bayar": id_metode_bayar
        }
        DUMMY_TR_PEMESANAN_JASA.append(new_pemesanan)
        
        # Buat status pemesanan "Mencari Pekerja Terdekat"
        status_mencari = get_status_pesanan_by_keterangan("Mencari Pekerja Terdekat")
        if not status_mencari:
            return render(request, 'subkategori_jasa/error.html', {'message': 'Status pesanan "Mencari Pekerja Terdekat" tidak ditemukan.'})
        
        new_tr_pemesanan_status = {
            "id_tr_pemesanan": pemesanan_id,
            "id_status": status_mencari["id"],
            "tgl_waktu": datetime.now()
        }
        DUMMY_TR_PEMESANAN_STATUS.append(new_tr_pemesanan_status)
        
        # Kurangi saldo MyPay pelanggan
        for mypay in DUMMY_MYPAY:
            if mypay["id"] == user["id"]:
                mypay["saldo"] -= total_biaya
                break
        
        return redirect('view_pemesanan_jasa')
    else:
        return HttpResponseForbidden("Metode tidak diizinkan.")




def profil_pekerja(request, pekerja_id):
    pekerja = get_pekerja_by_id(pekerja_id)
    if not pekerja:
        return render(request, 'subkategori_jasa/not_found.html', {'message': 'Pekerja tidak ditemukan.'})
    
    user = get_user_by_id(pekerja_id)
    nama = user["nama"] if user else "Tidak Diketahui"
    
    context = {
        'nama': nama,
        'nama_bank': pekerja["nama_bank"],
        'nomor_rekening': pekerja["nomor_rekening"],
        'npwp': pekerja["npwp"],
        'link_foto': pekerja["link_foto"],
        'rating': pekerja["rating"],
        'jml_pesanan_selesai': pekerja["jml_pesanan_selesai"],
    }

    return render(request, 'subkategori_jasa/profil_pekerja.html', context)


def view_pemesanan_jasa(request):
    user = get_user_by_id(request.user.id)
    if not user:
        return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
    user_role = get_user_role(request.user.id)
    if user_role != 'pelanggan':
        return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")
    
    pemesanan_jasa = get_pemesanan_jasa_by_pelanggan(user["id"])
    
    # Mengambil semua testimoni yang sudah dibuat oleh pengguna
    testimoni_dibuat = [testimoni["id_tr_pemesanan"] for testimoni in DUMMY_TESTIMONI if testimoni["id_tr_pemesanan"] in [p["id"] for p in pemesanan_jasa]]
    
    context = {
        'pemesanan_jasa': pemesanan_jasa,
        'testimoni_terkait': testimoni_dibuat,
    }

    return render(request, 'subkategori_jasa/view_pemesanan_jasa.html', context)
def batalkan_pemesanan_jasa(request, pemesanan_id):
    user = get_user_by_id(request.user.id)
    if not user:
        return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
    user_role = get_user_role(request.user.id)
    if user_role != 'pelanggan':
        return HttpResponseForbidden("Anda tidak memiliki izin untuk melakukan aksi ini.")
    
    pemesanan = get_tr_pemesanan_jasa_by_id(pemesanan_id)
    if not pemesanan:
        return render(request, 'subkategori_jasa/error.html', {'message': 'Pemesanan tidak ditemukan.'})
    
    if pemesanan["id_pelanggan"] != user["id"]:
        return HttpResponseForbidden("Anda tidak memiliki izin untuk membatalkan pemesanan ini.")
    
    # Mendapatkan status pemesanan
    tr_pemesanan_status = get_tr_pemesanan_status_by_id_tr_pemesanan(pemesanan_id)
    if not tr_pemesanan_status:
        return render(request, 'subkategori_jasa/error.html', {'message': 'Status pemesanan tidak ditemukan.'})
    
    current_status = None
    for status in DUMMY_STATUS_PESANAN:
        if status["id"] == tr_pemesanan_status["id_status"]:
            current_status = status["keterangan"]
            break
    
    if current_status not in ["Menunggu Pembayaran", "Mencari Pekerja Terdekat"]:
        return render(request, 'subkategori_jasa/error.html', {'message': 'Tidak dapat membatalkan pemesanan ini.'})
    
    # Update status pemesanan menjadi "Dibatalkan"
    status_dibatalkan = get_status_pesanan_by_keterangan("Dibatalkan")
    if not status_dibatalkan:
        return render(request, 'subkategori_jasa/error.html', {'message': 'Status "Dibatalkan" tidak ditemukan.'})
    
    tr_pemesanan_status["id_status"] = status_dibatalkan["id"]
    tr_pemesanan_status["tgl_waktu"] = datetime.now()
    
    # Mengembalikan saldo MyPay pengguna
    for mypay in DUMMY_MYPAY:
        if mypay["id"] == user["id"]:
            mypay["saldo"] += pemesanan["total_biaya"]
            break
    
    return redirect('view_pemesanan_jasa')




# def get_user_role(user_id):
#     with connection.cursor() as cursor:
#         # Cek apakah user adalah pelanggan
#         cursor.execute("""
#             SELECT Level FROM PELANGGAN WHERE Id = %s
#         """, [str(user_id)])
#         pelanggan = cursor.fetchone()
#         if pelanggan:
#             return 'pelanggan'
        
#         # Cek apakah user adalah pekerja
#         cursor.execute("""
#             SELECT NamaBank FROM PEKERJA WHERE Id = %s
#         """, [str(user_id)])
#         pekerja = cursor.fetchone()
#         if pekerja:
#             return 'pekerja'
        
#         return 'unknown'

# # Untuk bagian PELANGGAN
# # @login_required
# def subkategori_jasa_pelanggan(request, subkategori_id):
#     user_role = get_user_role(request.user.id)
#     if user_role != 'pelanggan':
#         return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")

#     with connection.cursor() as cursor:
#         # Mengambil informasi subkategori jasa
#         cursor.execute("""
#             SELECT NamaSubkategori, Deskripsi
#             FROM SUBKATEGORI_JASA
#             WHERE Id = %s
#         """, [str(subkategori_id)])
#         subkategori = cursor.fetchone()
        
#         if not subkategori:
#             return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})
        
#         nama_subkategori, deskripsi = subkategori

#         # Mengambil daftar pekerja dalam subkategori jasa
#         cursor.execute("""
#             SELECT 
#                 p.Id, u.Nama, p.Rating, p.JmlPsnananSelesai
#             FROM 
#                 PEKERJA p
#             JOIN 
#                 USER u 
#             ON 
#                 p.Id = u.Id
#             JOIN 
#                 PEKERJA_KATEGORI_JASA pkj 
#             ON 
#                 p.Id = pkj.PekerjaId
#             WHERE 
#                 pkj.KategoriJasaId = (
#                     SELECT KategoriJasaId FROM SUBKATEGORI_JASA WHERE Id = %s
#                 )
#         """, [str(subkategori_id)])
#         pekerja_list = cursor.fetchall()

#         # Mengambil daftar sesi layanan
#         cursor.execute("""
#             SELECT 
#                 sl.Sesi, sl.Harga
#             FROM 
#                 SESI_LAYANAN sl
#             WHERE 
#                 sl.SubkategoriId = %s
#             ORDER BY 
#                 sl.Sesi
#         """, [str(subkategori_id)])
#         sesi_layanan = cursor.fetchall()

#         # Mengambil daftar metode bayar
#         cursor.execute("""
#             SELECT Id, Nama FROM METODE_BAYAR ORDER BY Nama;
#         """)
#         metode_bayar = cursor.fetchall()

#     context = {
#         'nama_subkategori': nama_subkategori,
#         'deskripsi': deskripsi,
#         'pekerja_list': pekerja_list,
#         'sesi_layanan': sesi_layanan,
#         'subkategori_id': subkategori_id,
#         'metode_bayar_list': metode_bayar,
#     }

#     return render(request, 'subkategori_jasa/pelanggan.html', context)

# # Untuk bagian PEKERJA
# # @login_required
# def subkategori_jasa_pekerja(request, subkategori_id):
#     user_role = get_user_role(request.user.id)
#     if user_role != 'pekerja':
#         return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")

#     user_id = request.user.id

#     with connection.cursor() as cursor:
#         # Mengambil informasi subkategori jasa
#         cursor.execute("""
#             SELECT NamaSubkategori, Deskripsi
#             FROM SUBKATEGORI_JASA
#             WHERE Id = %s
#         """, [str(subkategori_id)])
#         subkategori = cursor.fetchone()
        
#         if not subkategori:
#             return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})
        
#         nama_subkategori, deskripsi = subkategori

#         # Mengambil daftar pekerja dalam subkategori jasa
#         cursor.execute("""
#             SELECT 
#                 p.Id, u.Nama, p.Rating, p.JmlPsnananSelesai
#             FROM 
#                 PEKERJA p
#             JOIN 
#                 USER u 
#             ON 
#                 p.Id = u.Id
#             JOIN 
#                 PEKERJA_KATEGORI_JASA pkj 
#             ON 
#                 p.Id = pkj.PekerjaId
#             WHERE 
#                 pkj.KategoriJasaId = (
#                     SELECT KategoriJasaId FROM SUBKATEGORI_JASA WHERE Id = %s
#                 )
#         """, [str(subkategori_id)])
#         pekerja_list = cursor.fetchall()

#         # Mengambil testimoni terkait subkategori jasa
#         cursor.execute("""
#             SELECT 
#                 t.Tgl, t.Teks, t.Rating, u.Nama
#             FROM 
#                 TESTIMONI t
#             JOIN 
#                 TR_PEMESANAN_JASA tpj 
#             ON 
#                 t.IdTrPemesanan = tpj.Id
#             JOIN 
#                 PELANGGAN pl 
#             ON 
#                 tpj.IdPelanggan = pl.Id
#             JOIN 
#                 USER u 
#             ON 
#                 pl.Id = u.Id
#             WHERE 
#                 tpj.IdKategoriJasa = (
#                     SELECT KategoriJasaId FROM SUBKATEGORI_JASA WHERE Id = %s
#                 )
#             ORDER BY 
#                 t.Tgl DESC
#         """, [str(subkategori_id)])
#         testimoni = cursor.fetchall()

#         # Mengambil daftar sesi layanan
#         cursor.execute("""
#             SELECT 
#                 sl.Sesi, sl.Harga
#             FROM 
#                 SESI_LAYANAN sl
#             WHERE 
#                 sl.SubkategoriId = %s
#             ORDER BY 
#                 sl.Sesi
#         """, [str(subkategori_id)])
#         sesi_layanan = cursor.fetchall()

#         # Cek apakah pekerja sudah bergabung dengan kategori jasa ini
#         cursor.execute("""
#             SELECT 1 FROM PEKERJA_KATEGORI_JASA
#             WHERE PekerjaId = %s AND KategoriJasaId = (
#                 SELECT KategoriJasaId FROM SUBKATEGORI_JASA WHERE Id = %s
#             )
#         """, [str(user_id), str(subkategori_id)])
#         is_joined = cursor.fetchone() is not None

#     context = {
#         'nama_subkategori': nama_subkategori,
#         'deskripsi': deskripsi,
#         'pekerja_list': pekerja_list,
#         'testimoni': testimoni,
#         'sesi_layanan': sesi_layanan,
#         'subkategori_id': subkategori_id,
#         'is_joined': is_joined,
#     }

#     return render(request, 'subkategori_jasa/pekerja.html', context)

# # Untuk Button Bergabung bagi PEKERJA
# # @login_required
# def bergabung_kategori_jasa(request, subkategori_id):
#     user_role = get_user_role(request.user.id)
#     if user_role != 'pekerja':
#         return HttpResponseForbidden("Not Allowed!")
    
#     user_id = request.user.id

#     with connection.cursor() as cursor:
#         # Cek apakah pekerja sudah bergabung
#         cursor.execute("""
#             SELECT 1 FROM PEKERJA_KATEGORI_JASA
#             WHERE PekerjaId = %s AND KategoriJasaId = (
#                 SELECT KategoriJasaId FROM SUBKATEGORI_JASA WHERE Id = %s
#             )
#         """, [str(user_id), str(subkategori_id)])
#         if cursor.fetchone():
#             return redirect('subkategori_jasa_pekerja', subkategori_id=subkategori_id)
        
#         # Bergabung dengan kategori jasa
#         cursor.execute("""
#             INSERT INTO PEKERJA_KATEGORI_JASA (PekerjaId, KategoriJasaId)
#             VALUES (
#                 %s, 
#                 (SELECT KategoriJasaId FROM SUBKATEGORI_JASA WHERE Id = %s)
#             )
#         """, [str(user_id), str(subkategori_id)])
    
#     return redirect('subkategori_jasa_pekerja', subkategori_id=subkategori_id)

# # @login_required
# def buat_pemesanan_jasa(request):
#     user_role = get_user_role(request.user.id)
#     if user_role != 'pelanggan':
#         return HttpResponseForbidden("Anda tidak memiliki izin untuk melakukan aksi ini.")
    
#     if request.method == 'POST':
#         subkategori_id = request.POST.get('subkategori_id')
#         sesi = request.POST.get('sesi')
#         harga = request.POST.get('harga')
#         tanggal_pemesanan = request.POST.get('tanggal_pemesanan')
#         kode_diskon = request.POST.get('kode_diskon').strip() or None
#         id_metode_bayar = request.POST.get('metode_bayar')

#         # Validasi input
#         if not subkategori_id or not sesi or not harga or not tanggal_pemesanan or not id_metode_bayar:
#             return render(request, 'subkategori_jasa/error.html', {'message': 'Data pemesanan tidak lengkap.'})
        
#         # Inisialisasi variabel diskon
#         potongan = 0
#         id_diskon = None

#         with connection.cursor() as cursor:
#             if kode_diskon:
#                 # Validasi voucher atau promo
#                 cursor.execute("""
#                     SELECT d.Id, d.Potongan, d.MinTrPemesanan, v.JmlHariBerlaku, v.KuotaPenggunaan
#                     FROM DISKON d
#                     LEFT JOIN VOUCHER v ON d.Kode = v.Kode
#                     LEFT JOIN PROMO p ON d.Kode = p.Kode
#                     WHERE d.Kode = %s
#                 """, [kode_diskon])
#                 diskon = cursor.fetchone()
#                 if not diskon:
#                     return render(request, 'subkategori_jasa/error.html', {'message': 'Kode diskon tidak valid.'})
                
#                 _, potongan, min_tr_pemesanan, jml_hari_berlaku, kuota_penggunaan = diskon

#                 # Cek syarat pemesanan minimal
#                 if min_tr_pemesanan > 0:
#                     cursor.execute("""
#                         SELECT COUNT(*) FROM TR_PEMESANAN_JASA
#                         WHERE IdPelanggan = %s AND TglPemesanan >= CURRENT_DATE - INTERVAL '%s days'
#                     """, [str(request.user.id), min_tr_pemesanan])
#                     count = cursor.fetchone()[0]
#                     if count < min_tr_pemesanan:
#                         return render(request, 'subkategori_jasa/error.html', {'message': 'Tidak memenuhi syarat pemesanan minimal untuk diskon ini.'})
                
#                 # Cek kuota penggunaan dan hari berlaku
#                 if jml_hari_berlaku is not None and jml_hari_berlaku <= 0:
#                     return render(request, 'subkategori_jasa/error.html', {'message': 'Voucher sudah kedaluwarsa.'})
#                 if kuota_penggunaan is not None and kuota_penggunaan <= 0:
#                     return render(request, 'subkategori_jasa/error.html', {'message': 'Kuota penggunaan voucher sudah habis.'})
                
#                 # Hitung potongan
#                 potongan = float(potongan)
#                 id_diskon = kode_diskon

#             # Hitung total biaya setelah potongan
#             total_biaya = float(harga) - potongan
#             if total_biaya < 0:
#                 total_biaya = 0

#             # Ambil pekerja pertama yang tersedia
#             cursor.execute("""
#                 SELECT p.Id
#                 FROM PEKERJA p
#                 JOIN PEKERJA_KATEGORI_JASA pkj 
#                 ON p.Id = pkj.PekerjaId
#                 WHERE pkj.KategoriJasaId = (
#                     SELECT KategoriJasaId FROM SUBKATEGORI_JASA WHERE Id = %s
#                 )
#                 LIMIT 1
#             """, [str(subkategori_id)])
#             pekerja = cursor.fetchone()
#             if not pekerja:
#                 return render(request, 'subkategori_jasa/error.html', {'message': 'Tidak ada pekerja yang tersedia untuk subkategori ini.'})
#             pekerja_id = pekerja[0]

#             # Buat ID unik untuk pemesanan
#             pemesanan_id = uuid.uuid4()

#             # Insert ke TR_PEMESANAN_JASA
#             cursor.execute("""
#                 INSERT INTO TR_PEMESANAN_JASA (
#                     Id, TglPemesanan, TglPekerjaan, WaktuPekerjaan, TotalBiaya, 
#                     IdPelanggan, IdPekerja, IdKategoriJasa, Sesi, IdDiskon, IdMetodeBayar
#                 )
#                 VALUES (
#                     %s, %s, %s, NOW(), %s, 
#                     %s, %s, 
#                     (SELECT KategoriJasaId FROM SUBKATEGORI_JASA WHERE Id = %s), 
#                     %s, %s, %s
#                 )
#             """, [
#                 str(pemesanan_id),
#                 tanggal_pemesanan,
#                 tanggal_pemesanan,  # Asumsi TglPekerjaan sama dengan TglPemesanan
#                 total_biaya,
#                 str(request.user.id),
#                 str(pekerja_id),
#                 str(subkategori_id),
#                 sesi,
#                 id_diskon,
#                 str(id_metode_bayar),
#             ])

#             # Trigger akan mengatur pengurangan kuota penggunaan voucher jika ada
#             # Pastikan trigger sudah diatur dengan benar di database
    
#         return redirect('subkategori_jasa:view_pemesanan_jasa')
#     else:
#         return HttpResponseForbidden("Metode tidak diizinkan.")

# # @login_required
# def profil_pekerja(request, pekerja_id):
#     with connection.cursor() as cursor:
#         # Mengambil informasi pekerja
#         cursor.execute("""
#             SELECT u.Nama, p.NamaBank, p.NomorRekening, p.NPWP, p.LinkFoto, p.Rating, p.JmlPsnananSelesai
#             FROM PEKERJA p
#             JOIN USER u 
#             ON p.Id = u.Id
#             WHERE p.Id = %s
#         """, [str(pekerja_id)])
#         pekerja = cursor.fetchone()
        
#         if not pekerja:
#             return render(request, 'subkategori_jasa/not_found.html', {'message': 'Pekerja tidak ditemukan.'})
        
#         nama, nama_bank, nomor_rekening, npwp, link_foto, rating, jml_pesanan_selesai = pekerja

#     context = {
#         'nama': nama,
#         'nama_bank': nama_bank,
#         'nomor_rekening': nomor_rekening,
#         'npwp': npwp,
#         'link_foto': link_foto,
#         'rating': rating,
#         'jml_pesanan_selesai': jml_pesanan_selesai,
#     }

#     return render(request, 'subkategori_jasa/profil_pekerja.html', context)

# # @login_required
# def view_pemesanan_jasa(request):
#     user_role = get_user_role(request.user.id)
#     if user_role != 'pelanggan':
#         return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")
    
#     with connection.cursor() as cursor:
#         # Mengambil semua pemesanan jasa
#         cursor.execute("""
#             SELECT 
#                 pj.Id, pj.TglPemesanan, pj.TglPekerjaan, pj.WaktuPekerjaan, pj.TotalBiaya, 
#                 sp.Keterangan
#             FROM 
#                 TR_PEMESANAN_JASA pj
#             JOIN 
#                 TR_PEMESANAN_STATUS tps 
#             ON 
#                 pj.Id = tps.IdTrPemesanan
#             JOIN 
#                 STATUS_PESANAN sp 
#             ON 
#                 tps.IdStatus = sp.Id
#             WHERE 
#                 pj.IdPelanggan = %s
#             ORDER BY 
#                 pj.TglPemesanan DESC
#         """, [str(request.user.id)])
#         pemesanan_jasa = cursor.fetchall()

#         # Mengambil semua testimoni yang sudah dibuat oleh pengguna
#         cursor.execute("""
#             SELECT IdTrPemesanan FROM TESTIMONI
#             WHERE IdTrPemesanan IN (
#                 SELECT Id FROM TR_PEMESANAN_JASA WHERE IdPelanggan = %s
#             )
#         """, [str(request.user.id)])
#         testimoni_dibuat = cursor.fetchall()
#         testimoni_ids = [testimoni[0] for testimoni in testimoni_dibuat]

#     context = {
#         'pemesanan_jasa': pemesanan_jasa,
#         'testimoni_terkait': testimoni_ids,
#     }

#     return render(request, 'subkategori_jasa/view_pemesanan_jasa.html', context)


# # @login_required
# def batalkan_pemesanan_jasa(request, pemesanan_id):
#     user_role = get_user_role(request.user.id)
#     if user_role != 'pelanggan':
#         return HttpResponseForbidden("Anda tidak memiliki izin untuk melakukan aksi ini.")
    
#     if request.method == 'POST':
#         with connection.cursor() as cursor:
#             # Cek status pemesanan
#             cursor.execute("""
#                 SELECT sp.Keterangan
#                 FROM TR_PEMESANAN_JASA pj
#                 JOIN TR_PEMESANAN_STATUS tps 
#                 ON pj.Id = tps.IdTrPemesanan
#                 JOIN STATUS_PESANAN sp 
#                 ON tps.IdStatus = sp.Id
#                 WHERE pj.Id = %s
#             """, [str(pemesanan_id)])
#             status = cursor.fetchone()
#             if not status:
#                 return render(request, 'subkategori_jasa/error.html', {'message': 'Pemesanan tidak ditemukan.'})
#             status_keterangan = status[0]
            
#             if status_keterangan not in ["Menunggu Pembayaran", "Mencari Pekerja Terdekat"]:
#                 return render(request, 'subkategori_jasa/error.html', {'message': 'Tidak dapat membatalkan pemesanan ini.'})
            
#             # Update status pemesanan menjadi "Dibatalkan"
#             cursor.execute("""
#                 UPDATE TR_PEMESANAN_STATUS tps
#                 SET IdStatus = (
#                     SELECT Id FROM STATUS_PESANAN WHERE Keterangan = 'Dibatalkan'
#                 ), TglWaktu = NOW()
#                 WHERE tps.IdTrPemesanan = %s
#             """, [str(pemesanan_id)])
        
#         return redirect('subkategori_jasa:view_pemesanan_jasa')
#     else:
#         return HttpResponseForbidden("Metode tidak diizinkan.")
    
'''
Fungsi untuk mengembalikan saldo MyPay saat pemesanan dibatalkan

CREATE OR REPLACE FUNCTION handle_order_cancellation() RETURNS TRIGGER 
AS $$
DECLARE
    pelanggan_id UUID;
    total_biaya NUMERIC;
    id_status_dibatalkan INTEGER;
    id_status_mencari_pekerja INTEGER;
BEGIN
    SELECT Id INTO id_status_dibatalkan FROM STATUS_PESANAN WHERE Keterangan = 'Dibatalkan';
    SELECT Id INTO id_status_mencari_pekerja FROM STATUS_PESANAN WHERE Keterangan = 'Mencari Pekerja Terdekat';
    
    IF NEW.IdStatus = id_status_dibatalkan THEN
        IF OLD.IdStatus = id_status_mencari_pekerja THEN
            SELECT IdPelanggan, TotalBiaya INTO pelanggan_id, total_biaya
            FROM TR_PEMESANAN_JASA
            WHERE Id = NEW.IdTrPemesanan;
            
            UPDATE MYPAY
            SET Saldo = Saldo + total_biaya
            WHERE Id = pelanggan_id;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_handle_order_cancellation
AFTER UPDATE ON TR_PEMESANAN_STATUS
FOR EACH ROW
EXECUTE FUNCTION handle_order_cancellation();
'''