import copy
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from enum import Enum
import json

# To make raw SQL queries
from django.db import connection


class Status(Enum):
    tiba = "Tiba Di Lokasi"
    in_progress = "Melakukan Pelayanan Jasa"
    selesai = "Selesai Melakukan Pelayanan"


def home(request: HttpRequest):
    return render(request, "pekerjaan_jasa/home.html")


def pekerjaan_list(request: HttpRequest):
    return render(request, "pekerjaan_jasa/pekerjaan_list.html")


def get_categories(request: HttpRequest):
    # TODO: Confirm correctness with auth service
    user = request.session.get("user")
    user_id = user["id"]

    # Fetching categories from user
    with connection.cursor() as cursor:
        cursor.execute(
            "set search_path to sijarta;"
            "select k.namakategori from kategori_jasa k "
            "join pekerja_kategori_jasa p on k.id = p.kategorijasaid "
            "where p.pekerjaid = %s",
            [user_id],
        )
        categories = cursor.fetchall()
        print(categories)

    jsonData = {"data": categories}
    return JsonResponse(jsonData)


def get_subcategories(request: HttpRequest):
    # TODO: Fetch category ID instead in order to keep things consistent
    category = request.GET.get("kategori")
    category_id = category["id"]

    # Fetch subcategories from chosen category
    with connection.cursor() as cursor:
        cursor.execute(
            "select sj.namasubkategori from subkategori_jasa sj "
            "join kategori_jasa k on k.id = sj.kategorijasaid "
            "where sj.kategorijasaid = %s",
            [category_id],
        )
        subcategories = cursor.fetchall()

    jsonData = {"data": subcategories}
    return JsonResponse(jsonData)


def get_tickets(request: HttpRequest):
    subcategory = request.GET.get("subkategori", default=None)
    status = request.GET.get("status", default=None)

    with connection.cursor() as cursor:
        cursor.execute(
            "select sj.namasubkategori as subkategori, p.nama, tpj.tglpemesanan, "
            "tpj.tglpekerjaan, tpj.totalbiaya, st.statuspesanan as status "
            "from tr_pemesanan_jasa tpj "
            "join subkategori_jasa sj on sj.id = tpj.idkategorijasa "
            "join users p on tpj.idpelanggan = p.id "
            "join tr_pemesanan_status tps on tpj.id = tps.idtrpemesanan "
            "join status_pesanan st on st.id = tps.idstatus"
        )
        filtered_tickets = dictfetchall(cursor)

    # Fetch tickets from chosen subcategory
    if subcategory != "" and subcategory is not None:
        filtered_tickets = list(
            filter(
                lambda ticket: ticket["subkategori"] == subcategory, filtered_tickets
            )
        )

    if status != "" and status is not None:
        filtered_tickets = list(
            filter(
                lambda ticket: Status(ticket["status"]).name == status, filtered_tickets
            )
        )

    jsonData = {"data": filtered_tickets}
    return JsonResponse(jsonData)


@csrf_exempt
def update_ticket_status(request: HttpRequest):
    body_data = json.loads(request.body)
    ticket_id = body_data.get("id")

    ticket = list(filter(lambda ticket: ticket["id"] == ticket_id, tickets))

    assert len(ticket) == 1

    ticket = ticket[0]

    if ticket["status"] == Status.tiba.value:
        ticket["status"] = Status.in_progress.value
    elif ticket["status"] == Status.in_progress.value:
        ticket["status"] = Status.selesai.value
    else:
        response = HttpResponse({"message": "Status pekerjaan sudah selesai!"})
        response.status_code = 304
        return response

    response = HttpResponse({"message": "Update pesanan berhasil diupdate!"})
    response.status_code = 200
    return response


def get_status_choices(request: HttpRequest):
    return JsonResponse(
        {"choices": [(status.name, status.value) for status in (Status)]}
    )


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
