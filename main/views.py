from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
import uuid
from uuid import UUID

def display_homepage(request):
    set_syntax = """
    SET search_path TO public, sijarta;
    """

    kategori_jasa_fetch_syntax = """
        SELECT * FROM kategori_jasa;
    """

    subkategori_jasa_fetch_syntax = """
        SELECT * FROM subkategori_jasa;
    """

    with connection.cursor() as cursor:
        cursor.execute(set_syntax)

        cursor.execute(kategori_jasa_fetch_syntax)
        kategori_jasa_columns = [col[0] for col in cursor.description]
        kategori_jasa = [
            dict(
                zip(
                    kategori_jasa_columns, 
                    [str(col) if isinstance(col, UUID) else col for col in row]
                )
            )
            for row in cursor.fetchall()
        ]

        cursor.execute(subkategori_jasa_fetch_syntax)
        subkategori_jasa_columns = [col[0] for col in cursor.description]
        subkategori_jasa = [
            dict(
                zip(
                    subkategori_jasa_columns, 
                    [str(col) if isinstance(col, UUID) else col for col in row]
                )
            )
            for row in cursor.fetchall()
        ]

    kategori_filter = request.GET.get("kategori", "")
    search_query = request.GET.get("search", "").lower()

    if kategori_filter:
        subkategori_jasa = [
            sub 
            for sub in subkategori_jasa 
            if sub["kategorijasaid"] == kategori_filter
        ]
    if search_query:
        subkategori_jasa = [
            sub
            for sub in subkategori_jasa
            if search_query in sub["namasubkategori"].lower()
        ]

    context = {
        "kategori_jasa": kategori_jasa,
        "subkategori_jasa": subkategori_jasa,
        "user": request.session.get("user", None),
    }


    # print("\n\n")

    print(context['subkategori_jasa'])

    # print(context['subkategori'][0])


    return render(request, "main/homepage.html", context)


def navbar(request):
    return render(request, "navbar.html")
