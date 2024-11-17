from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required

# @login_required
def homepage(request):
    kategori_filter = request.GET.get('kategori')
    search_subkategori = request.GET.get('search')

    with connection.cursor() as cursor:
        # Query untuk mengambil semua kategori jasa
        cursor.execute("""
            SELECT Id, Nama
            FROM KATEGORI_JASA
            ORDER BY Nama;
        """)
        kategori_jasa = cursor.fetchall()

        # Query untuk mengambil subkategori jasa dengan filter jika ada
        query = """
            SELECT sj.Id, sj.NamaSubkategori, sj.Deskripsi, kj.Nama AS NamaKategori
            FROM SUBKATEGORI_JASA sj
            JOIN KATEGORI_JASA kj ON sj.KategoriJasaId = kj.Id
        """
        params = []
        conditions = []
        if kategori_filter:
            conditions.append("kj.Id = %s")
            params.append(str(kategori_filter))
        if search_subkategori:
            conditions.append("sj.NamaSubkategori ILIKE %s")
            params.append(f"%{search_subkategori}%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY kj.Nama, sj.NamaSubkategori;"

        cursor.execute(query, params)
        subkategori_jasa = cursor.fetchall()

    context = {
        'kategori_jasa': kategori_jasa,
        'subkategori_jasa': subkategori_jasa,
        'selected_kategori': kategori_filter,
        'search_subkategori': search_subkategori,
    }

    return render(request, 'main/homepage.html', context)