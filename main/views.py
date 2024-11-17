from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required


DUMMY_KATEGORI_JASA = [
    {
        "id": "55555555-5555-5555-5555-555555555555",
        "nama_kategori": "Desain Grafis"
    },
    {
        "id": "66666666-6666-6666-6666-666666666666",
        "nama_kategori": "Pemrograman"
    }
]

# Dummy Data untuk Subkategori Jasa
DUMMY_SUBKATEGORI_JASA = [
    {
        "id": "77777777-7777-7777-7777-777777777777",
        "nama_subkategori": "Logo Design",
        "deskripsi": "Pembuatan desain logo profesional.",
        "kategori_jasa_id": "55555555-5555-5555-5555-555555555555"
    },
    {
        "id": "88888888-8888-8888-8888-888888888888",
        "nama_subkategori": "Website Development",
        "deskripsi": "Pengembangan website responsif dan dinamis.",
        "kategori_jasa_id": "66666666-6666-6666-6666-666666666666"
    }
]

def homepage(request):
    # Ambil nilai filter dari query parameters, jika ada
    selected_kategori = request.GET.get('kategori', '')
    search_subkategori = request.GET.get('search', '')

    # Terapkan filter berdasarkan kategori dan pencarian subkategori
    filtered_subkategori = DUMMY_SUBKATEGORI_JASA

    if selected_kategori:
        filtered_subkategori = [
            sub for sub in filtered_subkategori if sub['kategori_jasa_id'] == selected_kategori
        ]

    if search_subkategori:
        filtered_subkategori = [
            sub for sub in filtered_subkategori if search_subkategori.lower() in sub['nama_subkategori'].lower()
        ]

    context = {
        'kategori_jasa': DUMMY_KATEGORI_JASA,
        'subkategori_jasa': filtered_subkategori,
        'selected_kategori': selected_kategori,
        'search_subkategori': search_subkategori,
    }
    return render(request, 'main/homepage.html', context)

def navbar(request):
    return render(request, "navbar.html")
