from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
import uuid

# Updated Dummy Data untuk Kategori Jasa
DUMMY_KATEGORI_JASA = [
    {"id": "55555555-5555-5555-5555-555555555555", "nama_kategori": "Kategori Jasa 1"},
    {"id": "66666666-6666-6666-6666-666666666666", "nama_kategori": "Kategori Jasa 2"},
    {"id": "77777777-7777-7777-7777-777777777777", "nama_kategori": "Kategori Jasa 3"},
    # {"id": "4", "nama_kategori": "Kategori Jasa 4"},
    # {"id": "5", "nama_kategori": "Kategori Jasa 5"}
]

# Updated Dummy Data untuk Subkategori Jasa
DUMMY_SUBKATEGORI_JASA = [
    {"id": "1", "nama_subkategori": "Subkategori Jasa 1", "kategori_jasa_id": "55555555-5555-5555-5555-555555555555"},
    {"id": "2", "nama_subkategori": "Subkategori Jasa 2", "kategori_jasa_id": "55555555-5555-5555-5555-555555555555"},
    {"id": "3", "nama_subkategori": "Subkategori Jasa 3", "kategori_jasa_id": "55555555-5555-5555-5555-555555555555"},
    {"id": "4", "nama_subkategori": "Subkategori Jasa 1", "kategori_jasa_id": "66666666-6666-6666-6666-666666666666"},
    {"id": "5", "nama_subkategori": "Subkategori Jasa 2", "kategori_jasa_id": "66666666-6666-6666-6666-666666666666"},
    {"id": "6", "nama_subkategori": "Subkategori Jasa 3", "kategori_jasa_id": "66666666-6666-6666-6666-666666666666"},
    {"id": "7", "nama_subkategori": "Subkategori Jasa 1", "kategori_jasa_id": "77777777-7777-7777-7777-777777777777"},
    {"id": "8", "nama_subkategori": "Subkategori Jasa 2", "kategori_jasa_id": "77777777-7777-7777-7777-777777777777"},
    {"id": "9", "nama_subkategori": "Subkategori Jasa 3", "kategori_jasa_id": "77777777-7777-7777-7777-777777777777"},

]

def homepage(request):
    kategori_id_filter = request.GET.get("kategori", "")
    search_query = request.GET.get("search", "").lower()

    kategori_jasa = DUMMY_KATEGORI_JASA
    subkategori_jasa = DUMMY_SUBKATEGORI_JASA

    if kategori_id_filter:
        subkategori_jasa = [sub for sub in subkategori_jasa if sub["kategori_jasa_id"] == kategori_id_filter]
    if search_query:
        subkategori_jasa = [sub for sub in subkategori_jasa if search_query in sub["nama_subkategori"].lower()]

    context = {
        "kategori_jasa": kategori_jasa,
        "subkategori_jasa": subkategori_jasa,
    }
    return render(request, "main/homepage.html", context)


def navbar(request):
    return render(request, "navbar.html")
