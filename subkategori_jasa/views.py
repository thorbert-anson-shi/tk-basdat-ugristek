from django.shortcuts import render, get_object_or_404
from .models import SubkategoriJasa, SesiLayanan

def subkategori_list(request):
    subkategori = SubkategoriJasa.objects.all()
    return render(request, 'subkategori_jasa/subkategori_list.html', {'subkategori': subkategori})

def subkategori_detail(request, id):
    subkategori = get_object_or_404(SubkategoriJasa, id=id)
    sesi_layanan = SesiLayanan.objects.filter(subkategori=subkategori)
    return render(request, 'subkategori_jasa/subkategori_detail.html', {'subkategori': subkategori, 'sesi_layanan': sesi_layanan})