import copy
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from enum import Enum
import json


class Status(Enum):
    tiba = "Tiba Di Lokasi"
    in_progress = "Melakukan Pelayanan Jasa"
    selesai = "Selesai Melakukan Pelayanan"


# Dummy data
categories_to_subcategories = {
    "perbaikan_rumah": ["Perbaikan Genteng", "Perbaikan Dinding"],
    "mencuci": ["Cuci Baju", "Cuci Sepatu"],
}

tickets = [
    {
        "id": "756f4f52-9ef3-4667-a45a-8c7f5fbf7172",
        "subkategori": "cuci_baju",
        "nama_pelanggan": "danniel",
        "tanggal_pemesanan": "2024-12-10",
        "tanggal_pekerjaan": "2024-12-25",
        "biaya": 20000,
        "status": Status.tiba.value,
    },
    {
        "id": "cb55e6f6-1928-4b4f-b964-8798bdae8f4d",
        "subkategori": "cuci_baju",
        "nama_pelanggan": "sarah",
        "tanggal_pemesanan": "2024-12-11",
        "tanggal_pekerjaan": "2024-12-26",
        "biaya": 25000,
        "status": Status.in_progress.value,
    },
    {
        "id": "3a79befa-f462-4bc5-be59-de9fd2dec848",
        "subkategori": "cuci_sepatu",
        "nama_pelanggan": "john",
        "tanggal_pemesanan": "2024-12-12",
        "tanggal_pekerjaan": "2024-12-27",
        "biaya": 30000,
        "status": Status.selesai.value,
    },
    {
        "id": "904c2ad9-1bd8-44ab-ba1a-6b5cf99ff33b",
        "subkategori": "perbaikan_genteng",
        "nama_pelanggan": "mike",
        "tanggal_pemesanan": "2024-12-13",
        "tanggal_pekerjaan": "2024-12-28",
        "biaya": 50000,
        "status": Status.tiba.value,
    },
    {
        "id": "4cad1bdf-f9c0-416a-b113-4f8227a13e49",
        "subkategori": "perbaikan_dinding",
        "nama_pelanggan": "anna",
        "tanggal_pemesanan": "2024-12-14",
        "tanggal_pekerjaan": "2024-12-29",
        "biaya": 45000,
        "status": Status.in_progress.value,
    },
    {
        "id": "ee669b1e-fff2-42b7-9f90-27cc2b430248",
        "subkategori": "cuci_baju",
        "nama_pelanggan": "alice",
        "tanggal_pemesanan": "2024-12-15",
        "tanggal_pekerjaan": "2024-12-30",
        "biaya": 22000,
        "status": Status.tiba.value,
    },
    {
        "id": "950133e2-ed67-4581-950f-44890c6f39cf",
        "subkategori": "cuci_sepatu",
        "nama_pelanggan": "bob",
        "tanggal_pemesanan": "2024-12-16",
        "tanggal_pekerjaan": "2024-12-31",
        "biaya": 32000,
        "status": Status.in_progress.value,
    },
    {
        "id": "9497e961-d290-46cd-b29d-5c41d33f48c3",
        "subkategori": "perbaikan_genteng",
        "nama_pelanggan": "charlie",
        "tanggal_pemesanan": "2024-12-17",
        "tanggal_pekerjaan": "2025-01-01",
        "biaya": 55000,
        "status": Status.selesai.value,
    },
    {
        "id": "1cddcf9e-527a-46a6-823b-0d77a3c76f4d",
        "subkategori": "perbaikan_dinding",
        "nama_pelanggan": "david",
        "tanggal_pemesanan": "2024-12-18",
        "tanggal_pekerjaan": "2025-01-02",
        "biaya": 47000,
        "status": Status.tiba.value,
    },
    {
        "id": "450d0ddd-9fbe-4693-b24a-239a235ad5fd",
        "subkategori": "cuci_baju",
        "nama_pelanggan": "eve",
        "tanggal_pemesanan": "2024-12-19",
        "tanggal_pekerjaan": "2025-01-03",
        "biaya": 23000,
        "status": Status.in_progress.value,
    },
]


def home(request: HttpRequest):
    return render(request, "pekerjaan_jasa/home.html")


def pekerjaan_list(request: HttpRequest):
    return render(request, "pekerjaan_jasa/pekerjaan_list.html")


def get_categories(request: HttpRequest):
    # Fetching categories from user
    # ...

    # Dummy data
    categories = ["Perbaikan Rumah", "Mencuci"]
    jsonData = {"data": categories}
    return JsonResponse(jsonData)


def get_subcategories(request: HttpRequest):
    category = request.GET.get("kategori")

    # Fetch subcategories from chosen category
    subcategories = categories_to_subcategories[category]

    jsonData = {"data": subcategories}
    return JsonResponse(jsonData)


def get_tickets(request: HttpRequest):
    subcategory = request.GET.get("subkategori", default=None)
    status = request.GET.get("status", default=None)

    filtered_tickets = copy.deepcopy(tickets)

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
