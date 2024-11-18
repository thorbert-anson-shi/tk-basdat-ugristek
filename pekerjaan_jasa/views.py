from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

# Dummy data
categories_to_subcategories = {
    "perbaikan_rumah": ["Perbaikan Genteng", "Perbaikan Dinding"],
    "mencuci": ["Cuci Baju", "Cuci Sepatu"],
}

tickets_per_subcategory = {
    "cuci_baju": [
        {
            "id": "756f4f52-9ef3-4667-a45a-8c7f5fbf7172",
            "subkategori": "cuci_baju",
            "nama_pelanggan": "danniel",
            "tanggal_pemesanan": "2024-12-10",
            "tanggal_pekerjaan": "2024-12-25",
            "biaya": 20000,
            "status": "tiba",
        },
        {
            "id": "cb55e6f6-1928-4b4f-b964-8798bdae8f4d",
            "subkategori": "cuci_baju",
            "nama_pelanggan": "sarah",
            "tanggal_pemesanan": "2024-12-11",
            "tanggal_pekerjaan": "2024-12-26",
            "biaya": 25000,
            "status": "in_progress",
        },
    ],
    "cuci_sepatu": [
        {
            "id": "3a79befa-f462-4bc5-be59-de9fd2dec848",
            "subkategori": "cuci_sepatu",
            "nama_pelanggan": "john",
            "tanggal_pemesanan": "2024-12-12",
            "tanggal_pekerjaan": "2024-12-27",
            "biaya": 30000,
            "status": "selesai",
        }
    ],
    "perbaikan_genteng": [
        {
            "id": "904c2ad9-1bd8-44ab-ba1a-6b5cf99ff33b",
            "subkategori": "perbaikan_genteng",
            "nama_pelanggan": "mike",
            "tanggal_pemesanan": "2024-12-13",
            "tanggal_pekerjaan": "2024-12-28",
            "biaya": 50000,
            "status": "tiba",
        }
    ],
    "perbaikan_dinding": [
        {
            "id": "4cad1bdf-f9c0-416a-b113-4f8227a13e49",
            "subkategori": "perbaikan_dinding",
            "nama_pelanggan": "anna",
            "tanggal_pemesanan": "2024-12-14",
            "tanggal_pekerjaan": "2024-12-29",
            "biaya": 45000,
            "status": "in_progress",
        }
    ],
}


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
    subcategory = request.GET.get("subkategori")

    # Fetch tickets from chosen subcategory
    tickets = tickets_per_subcategory[subcategory]

    jsonData = {"data": tickets}
    return JsonResponse(jsonData)
