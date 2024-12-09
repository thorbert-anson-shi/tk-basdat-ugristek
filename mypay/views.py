from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from main.utils import dictfetchall

from django.db import connection


def home(request: HttpRequest):
    nomor_hp = request.session["user"]["no_hp"]
    nama = request.session["user"]["nama"]
    # TODO: Make sure to fetch from db
    saldo = request.session["user"]["saldo"]
    role = request.session["user"]["role"]

    return render(
        request,
        "mypay/home.html",
        context={"nomor_hp": nomor_hp, "saldo": saldo, "nama": nama, "role": role},
    )


def fetch_bills(request: HttpRequest):
    user_id = request.session["user"]["id"]

    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "select tpj.id, tpj.tglpekerjaan, tpj.totalbiaya, sj.namasubkategori as subkategori, tpj.sesi "
            "from tr_pemesanan_jasa tpj join subkategori_jasa sj on tpj.idkategorijasa = sj.id "
            "join tr_pemesanan_status tps on tpj.id = tps.idtrpemesanan "
            "join status_pesanan s on s.id = tps.idstatus "
            "where tpj.idpelanggan = %s and not s.statuspesanan = 'Menunggu Pembayaran';",
            [user_id],
        )
        bills = dictfetchall(cursor)

    return JsonResponse({"data": bills}, status=200)


def fetch_banks(request: HttpRequest):
    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute("select * from metode_bayar")
        banks = dictfetchall(cursor)

    return JsonResponse({"data": banks}, status=200)


def fetch_transactions(request: HttpRequest):
    user_id = request.session["user"]["id"]

    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "select tr.tgl as tanggal, tr.nominal, k.nama as kategori "
            "from tr_mypay tr join kategori_tr_mypay k on tr.kategoriid = k.id "
            "where tr.usersid = %s;",
            [user_id],
        )
        data = dictfetchall(cursor)

    return JsonResponse({"data": data}, status=200)


def handle_topup(request: HttpRequest):
    amount = request.POST["nominal"]
    user_id = request.session["user"]["id"]

    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "update users set saldomypay = saldomypay + %s where id = %s;",
            [amount, user_id],
        )

    return JsonResponse({"data": None}, status=200)


def handle_withdrawal(request: HttpRequest):
    user_account = request.POST["account-no"]
    amount = request.POST["nominal"]

    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "update users set saldomypay = saldomypay - %s where id = %s;",
            [amount, user_account],
        )

    return JsonResponse({"data": None}, status=200)


def handle_transfer(request: HttpRequest):
    amount = request.POST["nominal"]
    user_id = request.session["user"]["id"]
    recipient_pno = request.POST["nomor-hp"]

    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "update users set saldomypay = saldomypay - %s where id = %s;"
            "update users set saldomypay = saldomypay + %s where nohp = %s;",
            [amount, user_id, amount, recipient_pno],
        )

    return JsonResponse({"data": None}, status=200)


def handle_payment(request: HttpRequest):
    user_id = request.session["user"]["id"]
    bill_id = request.POST["jasa"]

    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "select totalbiaya from tr_pemesanan_jasa where id = %s;", [bill_id]
        )

        amount = cursor.fetchone()[0]

        cursor.execute(
            "update tr_pemesanan_status set idstatus = "
            "(select id from status_pesanan where statuspesanan = 'Selesai') "
            "where idtrpemesanan = %s;"
            "update users set saldomypay = saldomypay - %s where id = %s;",
            [bill_id, amount, user_id],
        )

    return JsonResponse({"data": None}, status=200)
