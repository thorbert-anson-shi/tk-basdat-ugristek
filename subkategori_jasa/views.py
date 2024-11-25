from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
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
    DUMMY_MYPAY,
)
import uuid
from datetime import datetime


# def get_user_by_id(user_id):
#     user = next((user for user in DUMMY_PENGGUNA if user["id"] == user_id), None)
#     if not user:
#         return {"nama": "Tidak Diketahui"}
#     return user

def get_user_by_id(user_id):
    print("Mencari pengguna dengan ID:", user_id)  # Debugging
    print("Mencari pengguna dengan ID:", user_id)  # Debugging
    for user in DUMMY_PENGGUNA:
        if str(user["id"]) == str(user_id):  # Cocokkan sebagai string
            print("Pengguna ditemukan:", user)
        if str(user["id"]) == str(user_id):  # Cocokkan sebagai string
            print("Pengguna ditemukan:", user)
            return user
    print("Pengguna tidak ditemukan.")
    print("Pengguna tidak ditemukan.")
    return None



def get_pelanggan_by_id(user_id):
    for pelanggan in DUMMY_PELANGGAN:
        if pelanggan["id"] == user_id:
            return pelanggan
    return None


def get_pekerja_by_id(pekerja_id):
    pekerja = next((pekerja for pekerja in DUMMY_PEKERJA if pekerja["id"] == pekerja_id), None)
    if not pekerja:
        return {"nama": "Tidak Diketahui"}
    return pekerja


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
    return [
        sesi for sesi in DUMMY_SESI_LAYANAN if sesi["subkategori_id"] == subkategori_id
    ]


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


def get_status_pesanan_by_id_tr_pemesanan(pemesanan_id):
    status = next(
        (s for s in DUMMY_TR_PEMESANAN_STATUS if s["id_tr_pemesanan"] == pemesanan_id),
        None,
    )
    if status:
        return next((st for st in DUMMY_STATUS_PESANAN if st["id"] == status["id_status"]), None)
    return None


def get_tr_pemesanan_status_by_id_tr_pemesanan(pemesanan_id):
    for status in DUMMY_TR_PEMESANAN_STATUS:
        if status["id_tr_pemesanan"] == pemesanan_id:
            return status
    return None


def get_testimoni_by_id_tr_pemesanan(pemesanan_id):
    return [
        testimoni
        for testimoni in DUMMY_TESTIMONI
        if testimoni["id_tr_pemesanan"] == pemesanan_id
    ]


def get_pekerja_list_by_kategori_jasa(kategori_jasa_id):
    pekerja_ids = [
        pkj["pekerja_id"]
        for pkj in DUMMY_PEKERJA_KATEGORI_JASA
        if pkj["kategori_jasa_id"] == kategori_jasa_id
    ]
    return [pekerja for pekerja in DUMMY_PEKERJA if pekerja["id"] in pekerja_ids]


def get_pemesanan_jasa_by_pelanggan(pelanggan_id):
    return [p for p in DUMMY_TR_PEMESANAN_JASA if p["id_pelanggan"] == pelanggan_id]


def get_user_role(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return 'unknown'

    if user["role"] == "pelanggan":
        return "pelanggan"
    elif user["role"] == "pekerja":
        return "pekerja"
    else:
        return "unknown"




# def subkategori_jasa_pelanggan(request, subkategori_id):
#     # Ambil subkategori berdasarkan ID
#     subkategori = next((s for s in DUMMY_SUBKATEGORI_JASA if s["id"] == str(subkategori_id)), None)
#     if not subkategori:
#         return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})

#     # Ambil data kategori jasa
#     kategori = next((k for k in DUMMY_KATEGORI_JASA if k["id"] == subkategori["kategori_jasa_id"]), None)

#     # Ambil data sesi layanan
#     sesi_layanan = [s for s in DUMMY_SESI_LAYANAN if s["subkategori_id"] == str(subkategori_id)]

#     # Ambil pekerja yang terkait dengan kategori jasa ini
#     pekerja_list = [p for p in DUMMY_PEKERJA if p["id"] in [
#         pkj["pekerja_id"] for pkj in DUMMY_PEKERJA if pkj["kategori_jasa_id"] == subkategori["kategori_jasa_id"]
#     ]]

#     # Ambil testimoni terkait
#     testimoni = [t for t in DUMMY_TESTIMONI if t["id_tr_pemesanan"] in [
#         pemesanan["id"] for pemesanan in DUMMY_TESTIMONI
#     ]]

#     context = {
#         'nama_subkategori': subkategori["nama_subkategori"],
#         'deskripsi': subkategori["deskripsi"],
#         'kategori': kategori,
#         'sesi_layanan': sesi_layanan,
#         'pekerja_list': pekerja_list,
#         'testimoni': testimoni,
#         'subkategori_id': subkategori_id,
#     }
#     return render(request, 'subkategori_jasa/pelanggan.html', context)

def subkategori_jasa_pelanggan(request, subkategori_id):
    # Cari subkategori berdasarkan ID
    subkategori = get_subkategori_jasa_by_id(subkategori_id)
    if not subkategori:
        return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})

    # Cari kategori jasa yang sesuai
    kategori = get_kategori_jasa_by_id(subkategori["kategori_jasa_id"])

    # Ambil pekerja terkait subkategori
    pekerja_list = get_pekerja_list_by_kategori_jasa(subkategori["kategori_jasa_id"])

    # Ambil testimoni terkait subkategori
    testimoni = [
        {
            "nama_pengguna": get_user_by_id(p["id_pelanggan"])["nama"],
            "teks": t["teks"],
            "tgl": t["tgl"],
            "nama_pekerja": get_user_by_id(p["id_pekerja"])["nama"],
            "rating": t["rating"]
        }
        for t in DUMMY_TESTIMONI
        for p in DUMMY_TR_PEMESANAN_JASA
        if t["id_tr_pemesanan"] == p["id"] and p["id_kategori_jasa"] == subkategori["kategori_jasa_id"]
    ]

    # Data untuk sesi layanan (filter berdasarkan subkategori_id)
    sesi_layanan = [sesi for sesi in DUMMY_SESI_LAYANAN if sesi["subkategori_id"] == subkategori_id]

    # Ambil metode pembayaran
    metode_bayar_list = DUMMY_METODE_BAYAR

    # Data context
    context = {
        'nama_subkategori': subkategori["nama_subkategori"],
        'deskripsi': subkategori["deskripsi"],
        'kategori': kategori,
        'sesi_layanan': sesi_layanan,
        'pekerja_list': pekerja_list,
        'testimoni': testimoni,
        'metode_bayar_list': metode_bayar_list,
        'subkategori_id': subkategori_id,
    }

    return render(request, "subkategori_jasa/pelanggan.html", context)






def subkategori_jasa_pekerja(request, subkategori_id):
    # Ambil data subkategori
    subkategori = get_subkategori_jasa_by_id(subkategori_id)
    if not subkategori:
        return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})

    # Ambil data kategori
    kategori = get_kategori_jasa_by_id(subkategori["kategori_jasa_id"])

    # Ambil sesi layanan
    sesi_layanan = [sesi for sesi in DUMMY_SESI_LAYANAN if sesi["subkategori_id"] == subkategori_id]

    # Ambil pekerja yang tergabung di kategori ini
    pekerja_list = [
        pekerja for pekerja in DUMMY_PEKERJA
        if any(pk["pekerja_id"] == pekerja["id"] and pk["kategori_jasa_id"] == subkategori["kategori_jasa_id"]
               for pk in DUMMY_PEKERJA_KATEGORI_JASA)
    ]

    # Ambil testimoni terkait subkategori ini
    testimoni_list = [
        {
            "nama_pengguna": get_user_by_id(tr["id_pelanggan"])["nama"],
            "teks": testimoni["teks"],
            "tgl": testimoni["tgl"],
            "nama_pekerja": get_user_by_id(tr["id_pekerja"])["nama"],
            "rating": testimoni["rating"]
        }
        for testimoni in DUMMY_TESTIMONI
        for tr in DUMMY_TR_PEMESANAN_JASA
        if tr["id"] == testimoni["id_tr_pemesanan"] and tr["id_kategori_jasa"] == subkategori["kategori_jasa_id"]
    ]

    # Cek apakah user ini adalah pekerja yang belum bergabung
    user = get_user_by_id(request.user.id)
    button_bergabung = False
    if user and user["role"] == "pekerja":
        button_bergabung = not any(
            pk["pekerja_id"] == user["id"] and pk["kategori_jasa_id"] == subkategori["kategori_jasa_id"]
            for pk in DUMMY_PEKERJA_KATEGORI_JASA
        )

    context = {
        "subkategori": subkategori,
        "kategori": kategori,
        "sesi_layanan": sesi_layanan,
        "pekerja_list": pekerja_list,
        "testimoni_list": testimoni_list,
        "button_bergabung": button_bergabung,
    }
    return render(request, 'subkategori_jasa/pekerja.html', context)






# def bergabung_kategori_jasa(request, subkategori_id):
#     if request.method == 'POST':
#         user = get_user_by_id(request.user.id)
#         if not user or get_user_role(request.user.id) != 'pekerja':
#             return HttpResponseForbidden("Anda tidak memiliki izin untuk melakukan aksi ini.")
        
#         # Tambahkan pekerja ke kategori jasa
#         pekerja_id = request.user.id
#         subkategori = get_subkategori_jasa_by_id(int(subkategori_id))
#         if not subkategori:
#             return render(request, 'subkategori_jasa/error.html', {'message': 'Subkategori tidak ditemukan.'})
        
#         # Tambahkan ke DUMMY_PEKERJA_KATEGORI_JASA
#         DUMMY_PEKERJA_KATEGORI_JASA.append({
#             "pekerja_id": pekerja_id,
#             "kategori_jasa_id": subkategori["kategori_jasa_id"]
#         })

#         return redirect('subkategori_jasa:subkategori_jasa_pekerja', subkategori_id=subkategori_id)

#     return HttpResponseForbidden("Metode tidak diizinkan.")


# def bergabung_kategori_jasa(request, subkategori_id):
#     if request.user.is_authenticated and get_user_role(request.user.id) == 'pekerja':
#         pekerja_id = request.user.id
#         subkategori = next((sub for sub in DUMMY_SUBKATEGORI_JASA if sub["id"] == subkategori_id), None)
#         if subkategori:
#             kategori_jasa_id = subkategori["kategori_jasa_id"]
#             # Tambah relasi pekerja-kategori jika belum ada
#             if not any(
#                 rel["pekerja_id"] == pekerja_id and rel["kategori_jasa_id"] == kategori_jasa_id
#                 for rel in DUMMY_PEKERJA_KATEGORI_JASA
#             ):
#                 DUMMY_PEKERJA_KATEGORI_JASA.append({"pekerja_id": pekerja_id, "kategori_jasa_id": kategori_jasa_id})
#         return redirect('subkategori_jasa:subkategori_jasa_pekerja', subkategori_id=subkategori_id)
#     else:
#         return HttpResponseForbidden("Anda tidak memiliki izin untuk bergabung.")

# def bergabung_kategori_jasa(request, subkategori_id):
#     user = get_user_by_id(request.user.id)
#     if user["role"] != "pekerja":
#         return HttpResponseForbidden("Hanya pekerja yang dapat bergabung.")

#     subkategori = get_subkategori_jasa_by_id(subkategori_id)
#     if not subkategori:
#         return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})

#     DUMMY_PEKERJA_KATEGORI_JASA.append({
#         "pekerja_id": user["id"],
#         "kategori_jasa_id": subkategori["kategori_jasa_id"]
#     })
#     return redirect('subkategori_jasa:subkategori_jasa_pekerja', subkategori_id=subkategori_id)

def bergabung_kategori_jasa(request, subkategori_id):
    if request.method == "POST":
        # Periksa apakah pengguna adalah pekerja
        user = get_user_by_id(request.user.id)
        if user and user["role"] == "pekerja":
            # Periksa apakah subkategori ada
            subkategori = get_subkategori_jasa_by_id(subkategori_id)
            if not subkategori:
                return render(request, 'subkategori_jasa/not_found.html', {'message': 'Subkategori tidak ditemukan.'})
            
            # Periksa apakah sudah tergabung
            already_joined = any(
                pk["pekerja_id"] == user["id"] and pk["kategori_jasa_id"] == subkategori["kategori_jasa_id"]
                for pk in DUMMY_PEKERJA_KATEGORI_JASA
            )
            
            if not already_joined:
                # Tambahkan pekerja ke kategori
                DUMMY_PEKERJA_KATEGORI_JASA.append({
                    "pekerja_id": user["id"],
                    "kategori_jasa_id": subkategori["kategori_jasa_id"]
                })
                return redirect('subkategori_jasa:subkategori_jasa_pekerja', subkategori_id=subkategori_id)
            else:
                return HttpResponse("Anda sudah tergabung di kategori ini.", status=200)
    return HttpResponseForbidden("Metode tidak diizinkan.")





import logging
logger = logging.getLogger(__name__)

# def buat_pemesanan_jasa(request):
#     user = get_user_by_id(request.user.id)
#     if not user:
#         return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
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
#         if not all([subkategori_id, sesi, harga, tanggal_pemesanan, id_metode_bayar]):
#             return render(request, 'subkategori_jasa/error.html', {'message': 'Data pemesanan tidak lengkap.'})
        
#         # Validasi subkategori_jasa
#         subkategori = get_subkategori_jasa_by_id(subkategori_id)
#         if not subkategori:
#             return render(request, 'subkategori_jasa/error.html', {'message': 'Subkategori tidak ditemukan.'})
        
#         # Inisialisasi variabel diskon
#         potongan = 0.0
#         id_diskon = None

#         # Validasi voucher atau promo
#         if kode_diskon:
#             diskon = get_diskon_by_kode(kode_diskon)
#             if not diskon:
#                 return render(request, 'subkategori_jasa/error.html', {'message': 'Kode diskon tidak valid.'})
            
#             potongan = diskon["potongan"]
#             min_tr_pemesanan = diskon["min_tr_pemesanan"]
            
#             # Cek syarat pemesanan minimal
#             pemesanan_sebelumnya = get_pemesanan_jasa_by_pelanggan(user["id"])
#             if len(pemesanan_sebelumnya) < min_tr_pemesanan:
#                 return render(request, 'subkategori_jasa/error.html', {'message': 'Tidak memenuhi syarat pemesanan minimal untuk diskon ini.'})
            
#             # Cek voucher
#             voucher = get_voucher_by_kode(kode_diskon)
#             if not voucher:
#                 return render(request, 'subkategori_jasa/error.html', {'message': 'Voucher tidak ditemukan.'})
            
#             # Memeriksa pembatasan penggunaan voucher
#             if voucher["jml_hari_berlaku"] <= 0:
#                 return render(request, 'subkategori_jasa/error.html', {'message': 'Voucher sudah kedaluwarsa.'})
            
#             if voucher["kuota_penggunaan"] <= 0:
#                 return render(request, 'subkategori_jasa/error.html', {'message': 'Kuota penggunaan voucher sudah habis.'})
            
#             # Hitung potongan (asumsi potongan adalah persentase)
#             total_biaya = float(harga) - (potongan * float(harga) / 100)
#             id_diskon = kode_diskon
            
#             # Kurangi kuota penggunaan voucher
#             for v in DUMMY_VOUCHER:
#                 if v["kode"] == kode_diskon:
#                     v["kuota_penggunaan"] -= 1
#                     break
#         else:
#             total_biaya = float(harga)
        
#         if total_biaya < 0:
#             total_biaya = 0.0
        
#         # Ambil pekerja pertama yang tersedia
#         pekerja_list = get_pekerja_list_by_kategori_jasa(subkategori["kategori_jasa_id"])
#         if not pekerja_list:
#             return render(request, 'subkategori_jasa/error.html', {'message': 'Tidak ada pekerja yang tersedia untuk subkategori ini.'})
        
#         pekerja_id = pekerja_list[0]["id"]
        
#         # Buat ID unik untuk pemesanan
#         pemesanan_id = str(uuid.uuid4())
        
#         # Buat pemesanan baru
#         new_pemesanan = {
#             "id": pemesanan_id,
#             "tgl_pemesanan": datetime.strptime(tanggal_pemesanan, "%Y-%m-%d"),
#             "tgl_pekerjaan": datetime.strptime(tanggal_pemesanan, "%Y-%m-%d"),  # Asumsi sama dengan tgl_pemesanan
#             "waktu_pekerjaan": datetime.strptime(tanggal_pemesanan, "%Y-%m-%d").replace(hour=12, minute=0, second=0),
#             "total_biaya": total_biaya,
#             "id_pelanggan": user["id"],
#             "id_pekerja": pekerja_id,
#             "id_kategori_jasa": subkategori["kategori_jasa_id"],
#             "sesi": sesi,
#             "id_diskon": id_diskon,
#             "id_metode_bayar": id_metode_bayar
#         }
#         DUMMY_TR_PEMESANAN_JASA.append(new_pemesanan)
        
#         # Buat status pemesanan "Mencari Pekerja Terdekat"
#         status_mencari = get_status_pesanan_by_keterangan("Mencari Pekerja Terdekat")
#         if not status_mencari:
#             return render(request, 'subkategori_jasa/error.html', {'message': 'Status pesanan "Mencari Pekerja Terdekat" tidak ditemukan.'})
        
#         new_tr_pemesanan_status = {
#             "id_tr_pemesanan": pemesanan_id,
#             "id_status": status_mencari["id"],
#             "tgl_waktu": datetime.now()
#         }
#         DUMMY_TR_PEMESANAN_STATUS.append(new_tr_pemesanan_status)
        
#         # Kurangi saldo MyPay pelanggan
#         for mypay in DUMMY_MYPAY:
#             if mypay["id"] == user["id"]:
#                 mypay["saldo"] -= total_biaya
#                 break
        
#         return redirect('subkategori_jasa:view_pemesanan_jasa')
#     else:
#         return HttpResponseForbidden("Metode tidak diizinkan.")

def buat_pemesanan_jasa(request):
    # Ambil data user
    print("Request User:", request.user)
    print("Request User ID:", getattr(request.user, "id", None))
    print("Data POST:", request.POST)

    user = get_user_by_id("1")  # ID pelanggan
    print("User ditemukan:", user)
    # user = get_user_by_id(request.user.id)
    # user = get_user_by_id(request.user.id if request.user else "1")
    if not user:
        return HttpResponseForbidden("Pengguna tidak ditemukan.")

    # Pastikan hanya pelanggan yang dapat memesan
    if user["role"] != "pelanggan":
        return HttpResponseForbidden("Hanya pelanggan yang dapat memesan jasa.")

    if request.method == "POST":
        # Ambil data dari form
        subkategori_id = request.POST.get("subkategori_id")
        sesi = request.POST.get("sesi")
        harga = request.POST.get("harga")
        tanggal_pemesanan = request.POST.get("tanggal_pemesanan")
        id_metode_bayar = request.POST.get("metode_bayar")

        # Validasi input
        if not all([subkategori_id, sesi, harga, tanggal_pemesanan, id_metode_bayar]):
            return render(request, "subkategori_jasa/error.html", {"message": "Data pemesanan tidak lengkap."})

        # Validasi subkategori
        subkategori = get_subkategori_jasa_by_id(subkategori_id)
        if not subkategori:
            return render(request, "subkategori_jasa/error.html", {"message": "Subkategori tidak ditemukan."})

        # Cari pekerja pertama
        pekerja_list = get_pekerja_list_by_kategori_jasa(subkategori["kategori_jasa_id"])
        if not pekerja_list:
            return render(request, "subkategori_jasa/error.html", {"message": "Tidak ada pekerja yang tersedia."})

        pekerja_id = pekerja_list[0]["id"]

        # Tambahkan pemesanan ke dummy data

        # Tambahkan pemesanan ke dummy data
        pemesanan_id = str(uuid.uuid4())
        new_pemesanan = {
            "id": pemesanan_id,
            "tgl_pemesanan": datetime.strptime(tanggal_pemesanan, "%Y-%m-%d"),
            "tgl_pekerjaan": datetime.strptime(tanggal_pemesanan, "%Y-%m-%d"),
            "waktu_pekerjaan": datetime.now(),
            "total_biaya": float(harga),
            "tgl_pekerjaan": datetime.strptime(tanggal_pemesanan, "%Y-%m-%d"),
            "waktu_pekerjaan": datetime.now(),
            "total_biaya": float(harga),
            "id_pelanggan": user["id"],
            "id_pekerja": pekerja_id,
            "id_kategori_jasa": subkategori["kategori_jasa_id"],
            "sesi": sesi,
            "id_diskon": None,
            "id_metode_bayar": id_metode_bayar
        }
        DUMMY_TR_PEMESANAN_JASA.append(new_pemesanan)

        # Update status pemesanan

        # Update status pemesanan
        status_mencari = get_status_pesanan_by_keterangan("Mencari Pekerja Terdekat")
        DUMMY_TR_PEMESANAN_STATUS.append({
            "id_tr_pemesanan": pemesanan_id,
            "id_status": status_mencari["id"],
            "tgl_waktu": datetime.now()
        })

        # Redirect ke halaman view pemesanan jasa
        return redirect("subkategori_jasa:view_pemesanan_jasa")
    else:
        return HttpResponseForbidden("Metode tak diizinkan")





def profil_pekerja(request, pekerja_id):
    pekerja = get_pekerja_by_id(pekerja_id)
    if not pekerja:
        return render(request, 'subkategori_jasa/not_found.html', {'message': 'Pekerja tidak ditemukan.'})

    user = get_user_by_id(pekerja_id)
    nama = user["nama"] if user else "Tidak Diketahui"

    # Tambahkan subkategori_id ke context (gunakan subkategori pertama dari pekerja jika relevan)
    subkategori_id = "1"  # Atur sesuai data dummy Anda jika ada relasi pekerja dengan subkategori

    context = {
        'nama': nama,
        'rating': pekerja["rating"],
        'jml_pesanan_selesai': pekerja["jml_pesanan_selesai"],
        'no_hp': user["no_hp"],
        'tanggal_lahir': user["tanggal_lahir"],
        'alamat': user["alamat"],
        'subkategori_id': subkategori_id,  # Pastikan subkategori_id diteruskan
    }

    return render(request, "subkategori_jasa/profil_pekerja.html", context)






# def view_pemesanan_jasa(request):
#     user = get_user_by_id(request.user.id)
#     if not user:
#         return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
#     # Filter inputs
#     selected_subkategori = request.GET.get('subkategori', '')
#     selected_status = request.GET.get('status', '')

#     # Fetch relevant pemesanan
#     pemesanan_list = [
#         {
#             "id": p["id"],
#             "subkategori": get_subkategori_jasa_by_id(p["id_kategori_jasa"]),
#             "sesi": p["sesi"],
#             "total_biaya": p["total_biaya"],
#             "pekerja": get_pekerja_by_id(p["id_pekerja"]),
#             "status": get_status_pesanan_by_id_tr_pemesanan(p["id"]),
#             "testimoni_dibuat": p["id"] in [t["id_tr_pemesanan"] for t in DUMMY_TESTIMONI],
#         }
#         for p in get_pemesanan_jasa_by_pelanggan(user["id"])
#     ]

#     # Apply filters
#     if selected_subkategori:
#         pemesanan_list = [p for p in pemesanan_list if str(p["subkategori"]["id"]) == selected_subkategori]
#     if selected_status:
#         pemesanan_list = [p for p in pemesanan_list if str(p["status"]["id"]) == selected_status]

#     # Render template
#     context = {
#         "pemesanan_list": pemesanan_list,
#         "selected_subkategori": selected_subkategori,
#         "selected_status": selected_status,
#     }
#     return render(request, 'subkategori_jasa/view_pemesanan_jasa.html', context)

# def view_pemesanan_jasa(request):
#     user = get_user_by_id(request.user.id)
#     if not user:
#         return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
#     # Filter inputs
#     selected_subkategori = request.GET.get('subkategori', '')
#     selected_status = request.GET.get('status', '')

#     # Fetch relevant pemesanan
#     pemesanan_list = [
#         {
#             "id": p["id"],
#             "subkategori": get_subkategori_jasa_by_id(p["id_kategori_jasa"]),
#             "sesi": p["sesi"],
#             "total_biaya": p["total_biaya"],
#             "pekerja": get_pekerja_by_id(p["id_pekerja"]),
#             "status": get_status_pesanan_by_id_tr_pemesanan(p["id"]),
#             "testimoni_dibuat": p["id"] in [t["id_tr_pemesanan"] for t in DUMMY_TESTIMONI],
#         }
#         for p in get_pemesanan_jasa_by_pelanggan(user["id"])
#     ]

#     # Apply filters
#     if selected_subkategori:
#         pemesanan_list = [p for p in pemesanan_list if str(p["subkategori"]["id"]) == selected_subkategori]
#     if selected_status:
#         pemesanan_list = [p for p in pemesanan_list if str(p["status"]["id"]) == selected_status]

#     # Render template
#     context = {
#         "pemesanan_list": pemesanan_list,
#         "selected_subkategori": selected_subkategori,
#         "selected_status": selected_status,
#     }
#     return render(request, 'subkategori_jasa/view_pemesanan_jasa.html', context)

def view_pemesanan_jasa(request):
    return render(request, 'subkategori_jasa/view_pemesanan_jasa.html')



def batalkan_pemesanan_jasa(request, pemesanan_id):
    user = get_user_by_id(request.user.id)
    if not user:
        return HttpResponseForbidden("Pengguna tidak ditemukan.")

    user_role = get_user_role(request.user.id)
    if user_role != "pelanggan":
        return HttpResponseForbidden(
            "Anda tidak memiliki izin untuk melakukan aksi ini."
        )

    pemesanan = get_tr_pemesanan_jasa_by_id(pemesanan_id)
    if not pemesanan:
        return render(
            request,
            "subkategori_jasa/error.html",
            {"message": "Pemesanan tidak ditemukan."},
        )

    if pemesanan["id_pelanggan"] != user["id"]:
        return HttpResponseForbidden(
            "Anda tidak memiliki izin untuk membatalkan pemesanan ini."
        )

    # Mendapatkan status pemesanan
    tr_pemesanan_status = get_tr_pemesanan_status_by_id_tr_pemesanan(pemesanan_id)
    if not tr_pemesanan_status:
        return render(
            request,
            "subkategori_jasa/error.html",
            {"message": "Status pemesanan tidak ditemukan."},
        )

    current_status = None
    for status in DUMMY_STATUS_PESANAN:
        if status["id"] == tr_pemesanan_status["id_status"]:
            current_status = status["keterangan"]
            break

    if current_status not in ["Menunggu Pembayaran", "Mencari Pekerja Terdekat"]:
        return render(
            request,
            "subkategori_jasa/error.html",
            {"message": "Tidak dapat membatalkan pemesanan ini."},
        )

    # Update status pemesanan menjadi "Dibatalkan"
    status_dibatalkan = get_status_pesanan_by_keterangan("Dibatalkan")
    if not status_dibatalkan:
        return render(
            request,
            "subkategori_jasa/error.html",
            {"message": 'Status "Dibatalkan" tidak ditemukan.'},
        )

    tr_pemesanan_status["id_status"] = status_dibatalkan["id"]
    tr_pemesanan_status["tgl_waktu"] = datetime.now()

    # Mengembalikan saldo MyPay pengguna
    for mypay in DUMMY_MYPAY:
        if mypay["id"] == user["id"]:
            mypay["saldo"] += pemesanan["total_biaya"]
            break
    
    return redirect('view_pemesanan_jasa')

def show_form_testimoni(request):
    return render(request, "form_testimoni.html")

# def show_form_testimoni(request, pemesanan_id):
#     user = get_user_by_id(request.user.id)
#     if not user:
#         return HttpResponseForbidden("Pengguna tidak ditemukan.")
    
#     user_role = get_user_role(request.user.id)
#     if user_role != 'pelanggan':
#         return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")
    
#     pemesanan = get_tr_pemesanan_jasa_by_id(pemesanan_id)
#     if not pemesanan:
#         return render(request, 'subkategori_jasa/not_found.html', {'message': 'Pemesanan tidak ditemukan.'})
    
#     if pemesanan["id_pelanggan"] != user["id"]:
#         return HttpResponseForbidden("Anda tidak memiliki izin untuk melihat testimoni ini.")
    
#     testimoni = get_testimoni_by_id_tr_pemesanan(pemesanan_id)
#     if not testimoni:
#         return render(request, 'subkategori_jasa/not_found.html', {'message': 'Testimoni tidak ditemukan.'})
    
#     context = {
#         'testimoni': testimoni,
#     }
    
#     return render(request, 'subkategori_jasa/testimoni.html', context)
    
# '''
# Fungsi untuk mengembalikan saldo MyPay saat pemesanan dibatalkan

# CREATE OR REPLACE FUNCTION handle_order_cancellation() RETURNS TRIGGER 
# AS $$
# DECLARE
#     pelanggan_id UUID;
#     total_biaya NUMERIC;
#     id_status_dibatalkan INTEGER;
#     id_status_mencari_pekerja INTEGER;
# BEGIN
#     SELECT Id INTO id_status_dibatalkan FROM STATUS_PESANAN WHERE Keterangan = 'Dibatalkan';
#     SELECT Id INTO id_status_mencari_pekerja FROM STATUS_PESANAN WHERE Keterangan = 'Mencari Pekerja Terdekat';
    
#     IF NEW.IdStatus = id_status_dibatalkan THEN
#         IF OLD.IdStatus = id_status_mencari_pekerja THEN
#             SELECT IdPelanggan, TotalBiaya INTO pelanggan_id, total_biaya
#             FROM TR_PEMESANAN_JASA
#             WHERE Id = NEW.IdTrPemesanan;
            
#             UPDATE MYPAY
#             SET Saldo = Saldo + total_biaya
#             WHERE Id = pelanggan_id;
#         END IF;
#     END IF;
    
#     RETURN NEW;
# END;
# $$ LANGUAGE plpgsql;

# CREATE TRIGGER trg_handle_order_cancellation
# AFTER UPDATE ON TR_PEMESANAN_STATUS
# FOR EACH ROW
# EXECUTE FUNCTION handle_order_cancellation();
# """
