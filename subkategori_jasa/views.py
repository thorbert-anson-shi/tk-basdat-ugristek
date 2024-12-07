from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

# yang bisa akses subkategori jasa cuman yg udah login


@login_required
def subkategori_jasa_pelanggan(request, id_subkategori):
    set_syntax = """
        SET search_path TO sijarta;
    """

    subkategori_syntax = f"""
        SELECT *
        FROM subkategori_jasa
        WHERE id = {id_subkategori};
    """

    kategori_syntax = f"""
        SELECT *
        FROM kategori_jasa
        WHERE id = 
        (SELECT kategorijasaid
        FROM subkategori_jasa
        WHERE id = {id_subkategori};
        );
    """

    sesi_layanan_syntax = f"""
        SELECT *
        FROM sesi_layanan
        WHERE subkategoriid = {id_subkategori};
    """

    pekerja_list_syntax = f"""
        SELECT *
        FROM pekerja_kategori_jasa
        WHERE kategorijasaid = 
        (SELECT kategorijasaid
        FROM subkategori_jasa
        WHERE id = {id_subkategori};
        );
    """


    testimoni_list_syntax = f"""
        SELECT *
        FROM testimoni
        WHERE idtrpemesanan = 
        (SELECT id
        FROM tr_pemesanan_jasa
        WHERE idkategorijasa = 
        (SELECT kategorijasaid
        FROM subkategori_jasa
        WHERE id = {id_subkategori}
        )
        );
    """

    diskon_list_syntax = f"""
        SELECT *
        FROM tr_pembelian_voucher
        WHERE idpelanggan = {request.session.get("user", None).get("id")};
    """

    metode_bayar_list_syntax = """
        SELECT *
        FROM metode_bayar;
    """

    with connection.cursor() as cursor:
        cursor.execute(set_syntax)

        cursor.execute(subkategori_syntax)
        subkategori = cursor.fetchall()

        cursor.execute(kategori_syntax)
        kategori = cursor.fetchall()

        cursor.execute(sesi_layanan_syntax)
        sesi_layanan = cursor.fetchall()

        cursor.execute(pekerja_list_syntax)
        pekerja_list = cursor.fetchall()
        
        cursor.execute(testimoni_list_syntax)
        testimoni_list = cursor.fetchall()

        cursor.execute(metode_bayar_list_syntax)
        metode_bayar_list = cursor.fetchall()

        cursor.execute(diskon_list_syntax)
        diskon_list = cursor.fetchall()
        

    context = {
        'subkategori': subkategori, #ez tinggal dari id
        'kategori': kategori, #ez tinggal dari id 
        'sesi_layanan': sesi_layanan, #fetch dari database juga
        'pekerja_list': pekerja_list, #ini fetch dari current pekerja_list yg ada di database, kalo dari pekerja ada yg bergabung, maka trigger penambahannya
        'testimoni_list': testimoni_list, #ini fetch dari testimoni tino

        'metode_bayar_list': metode_bayar_list, #ini dari metode-metode bayar yg ada di database aja
        'diskon_list': diskon_list, #ini dari diskon2 (voucher, promo) yg dimiliki pelanggan ybs

        #keknya nanti bakal ada satu trigger khusus untuk kurangin saldo user sesuai metode_bayar, diskon, dan sesi layanan yg dipilih
        #sama distribute duitnya ke pekerjanya pikirin jg
    }
    return render(request, "pelanggan.html", context)

@login_required
def subkategori_jasa_pekerja(request, id_subkategori):
    set_syntax = """
        SET search_path TO sijarta;
    """

    subkategori_syntax = f"""
        SELECT *
        FROM subkategori_jasa
        WHERE id = {id_subkategori};
    """

    kategori_syntax = f"""
        SELECT *
        FROM kategori_jasa
        WHERE id = 
        (SELECT kategorijasaid
        FROM subkategori_jasa
        WHERE id = {id_subkategori};
        );
    """

    sesi_layanan_syntax = f"""
        SELECT *
        FROM sesi_layanan
        WHERE subkategoriid = {id_subkategori};
    """

    pekerja_list_syntax = f"""
        SELECT *
        FROM pekerja_kategori_jasa
        WHERE kategorijasaid = 
        (SELECT kategorijasaid
        FROM subkategori_jasa
        WHERE id = {id_subkategori};
        );
    """

    testimoni_list_syntax = f"""
        SELECT *
        FROM testimoni
        WHERE idtrpemesanan = 
        (SELECT id
        FROM tr_pemesanan_jasa
        WHERE idkategorijasa = 
        (SELECT kategorijasaid
        FROM subkategori_jasa
        WHERE id = {id_subkategori}
        )
        );
    """

    with connection.cursor() as cursor:
        cursor.execute(set_syntax)

        cursor.execute(subkategori_syntax)
        subkategori = cursor.fetchall()

        cursor.execute(kategori_syntax)
        kategori = cursor.fetchall()

        cursor.execute(sesi_layanan_syntax)
        sesi_layanan = cursor.fetchall()

        cursor.execute(pekerja_list_syntax)
        pekerja_list = cursor.fetchall()
        
        cursor.execute(testimoni_list_syntax)
        testimoni_list = cursor.fetchall()

    context = {
        "subkategori": subkategori,
        "kategori": kategori,
        "sesi_layanan": sesi_layanan,
        "pekerja_list": pekerja_list,
        "testimoni_list": testimoni_list,
    }
    return render(request, "pekerja.html", context)

def show_form_testimoni(request):
    return render(request, "form_testimoni.html")