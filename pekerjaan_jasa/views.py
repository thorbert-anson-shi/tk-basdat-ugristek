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
        "cuci_baju": [],
        "cuci_sepatu": [],
        "perbaikan_genteng": [],
        "perbaikan_dinding": [],
    }

    tickets = tickets_per_subcategory[subcategory]

    jsonData = {"data": tickets}
    return JsonResponse(tickets)
