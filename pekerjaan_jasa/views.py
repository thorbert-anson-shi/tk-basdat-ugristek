from django.http import HttpRequest, JsonResponse
from django.shortcuts import render


def home(request: HttpRequest):
    return render(request, "pekerjaan_jasa/home.html")


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

    # Dummy data
    if category == "perbaikan_rumah":
        subcategories = ["Perbaikan Genteng", "Perbaikan Dinding"]
    else:
        subcategories = ["Cuci Baju", "Cuci Sepatu"]

    jsonData = {"data": subcategories}
    return JsonResponse(jsonData)


def get_tickets(request: HttpRequest):
    subcategory = request.GET.get("subkategori")

    # Fetch tickets from chosen subcategory

    # Dummy data
    tickets_per_subcategory = {
        "cuci_baju": [
            {
                "subkategori": "cuci_baju",
                "nama_pelanggan": "danniel",
                "tanggal_pemesanan": "2024-12-10",
                "tanggal_pekerjaan": "2024-12-25",
                "biaya": 20000,
            },
            {
                "subkategori": "cuci_baju",
                "nama_pelanggan": "sarah",
                "tanggal_pemesanan": "2024-12-11",
                "tanggal_pekerjaan": "2024-12-26",
                "biaya": 25000,
            },
        ],
        "cuci_sepatu": [
            {
                "subkategori": "cuci_sepatu",
                "nama_pelanggan": "john",
                "tanggal_pemesanan": "2024-12-12",
                "tanggal_pekerjaan": "2024-12-27",
                "biaya": 30000,
            }
        ],
        "perbaikan_genteng": [
            {
                "subkategori": "perbaikan_genteng",
                "nama_pelanggan": "mike",
                "tanggal_pemesanan": "2024-12-13",
                "tanggal_pekerjaan": "2024-12-28",
                "biaya": 50000,
            }
        ],
        "perbaikan_dinding": [
            {
                "subkategori": "perbaikan_dinding",
                "nama_pelanggan": "anna",
                "tanggal_pemesanan": "2024-12-14",
                "tanggal_pekerjaan": "2024-12-29",
                "biaya": 45000,
            }
        ],
    }

    tickets = tickets_per_subcategory[subcategory]

    jsonData = {"data": tickets}
    return JsonResponse(jsonData)
