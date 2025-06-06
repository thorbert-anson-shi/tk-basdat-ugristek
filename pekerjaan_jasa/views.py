import copy
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from enum import Enum
import json

# To make raw SQL queries
from django.db import connection


class Status:
    status_to_id = dict()

    @classmethod
    def get_available_statuses(self):
        with connection.cursor() as cursor:
            cursor.execute("set search_path to sijarta;")
            cursor.execute("select * from status_pesanan;")
            status_list = dictfetchall(cursor)

        for status in status_list:
            self.status_to_id[status["statuspesanan"]] = status["id"]


def home(request: HttpRequest):
    return render(request, "pekerjaan_jasa/home.html")


def pekerjaan_list(request: HttpRequest):
    return render(request, "pekerjaan_jasa/pekerjaan_list.html")


def get_categories(request: HttpRequest):
    user_id = request.session["user"]["id"]

    # Fetching categories from user
    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "select k.namakategori, k.id from kategori_jasa k "
            "join pekerja_kategori_jasa p on k.id = p.kategorijasaid "
            "where p.pekerjaid = %s;",
            [user_id],
        )
        categories = cursor.fetchall()
        print(categories)

    jsonData = {"data": categories}
    return JsonResponse(jsonData)


def take_ticket(request: HttpRequest):
    Status.get_available_statuses()

    user_id = request.session["user"]["id"]
    ticket_id = request.GET.get("ticket_id")

    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "update tr_pemesanan_jasa set idpekerja = %s where idtrpemesanan = %s;"
            "update tr_pemesanan_status set idstatus = %s where idtrpemesanan = %s;",
            [
                user_id,
                ticket_id,
                Status.status_to_id["Menunggu Pekerja Berangkat"],
                ticket_id,
            ],
        )

    return HttpResponse("Pesanan berhasil diambil", status=200)


def get_subcategories(request: HttpRequest):
    category_id = request.GET.get("kategori")

    # Fetch subcategories from chosen category
    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "select sj.namasubkategori, sj.id from subkategori_jasa sj "
            "join kategori_jasa k on k.id = sj.kategorijasaid "
            "where sj.kategorijasaid = %s",
            [category_id],
        )
        subcategories = cursor.fetchall()

    jsonData = {"data": subcategories}
    return JsonResponse(jsonData)


def get_tickets(request: HttpRequest):
    subcategory_id = request.GET.get("subkategori", default=None)
    status = request.GET.get("status", default=None)

    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "select tpj.id, sj.id as subkategoriid, sj.namasubkategori as subkategori, p.nama as nama_pelanggan, tpj.tglpemesanan as tanggal_pemesanan, "
            "tpj.tglpekerjaan as tanggal_pekerjaan, tpj.totalbiaya as biaya, st.statuspesanan as status "
            "from tr_pemesanan_jasa tpj "
            "join subkategori_jasa sj on sj.id = tpj.idkategorijasa "
            "join users p on tpj.idpelanggan = p.id "
            "join tr_pemesanan_status tps on tpj.id = tps.idtrpemesanan "
            "join status_pesanan st on st.id = tps.idstatus"
        )
        filtered_tickets = dictfetchall(cursor)

    # Fetch tickets from chosen subcategory
    if subcategory_id != "" and subcategory_id is not None:
        filtered_tickets = list(
            filter(
                lambda ticket: str(ticket["subkategoriid"]) == subcategory_id
                and ticket["status"] == "Mencari Pekerja Terdekat",
                filtered_tickets,
            )
        )

    if status != "" and status is not None:
        filtered_tickets = list(
            filter(
                lambda ticket: ticket["status"] == status,
                filtered_tickets,
            )
        )

    jsonData = {"data": filtered_tickets}
    return JsonResponse(jsonData)


@csrf_exempt
def update_ticket_status(request: HttpRequest):
    ticket_id = request.POST.get("id")

    with connection.cursor() as cursor:
        cursor.execute("set search_path to sijarta;")
        cursor.execute(
            "select s.statuspesanan from tr_pemesanan_status as tps "
            "join status_pesanan s on tps.idstatus = s.id "
            "where tps.idtrpemesanan = %s;",
            [ticket_id],
        )
        ticket_status = cursor.fetchone()
        print(ticket_status)

        if ticket_status == "Pekerja Tiba Di Lokasi":
            cursor.execute(
                "update tr_pemesanan_status set idstatus = %s where idtrpemesanan = %s;",
                [Status.status_to_id["Pelayanan Jasa Sedang Dilakukan"], ticket_id],
            )
        elif ticket_status == "Pelayanan Jasa Sedang Dilakukan":
            cursor.execute(
                "update tr_pemesanan_status set idstatus = %s where idtrpemesanan = %s;",
                [Status.status_to_id["Selesai"], ticket_id],
            )
        else:
            response = HttpResponse({"message": "Status pekerjaan sudah selesai!"})
            response.status_code = 304
            return response

    response = HttpResponse({"message": "Update pesanan berhasil diupdate!"})
    response.status_code = 200
    return response


def get_status_choices(request: HttpRequest):
    Status.get_available_statuses()
    return JsonResponse(
        {
            "choices": list(
                filter(
                    lambda status: status
                    in [
                        "Menunggu Pekerja Berangkat",
                        "Pekerja Tiba Di Lokasi",
                        "Pelayanan Jasa Sedang Dilakukan",
                        "Pesanan Selesai",
                    ],
                    list(Status.status_to_id.keys()),
                )
            )
        }
    )


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
