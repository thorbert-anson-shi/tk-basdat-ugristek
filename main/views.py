from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required


# Dummy Data untuk Kategori Jasa
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

def homepage(request):
    kategori = DUMMY_KATEGORI_JASA
    return render(request, 'main/homepage.html', {'kategori': kategori})



def navbar(request):
    return render(request, "navbar.html")
