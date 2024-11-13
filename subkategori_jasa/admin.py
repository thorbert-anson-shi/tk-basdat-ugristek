from django.contrib import admin
from .models import KategoriJasa, SubkategoriJasa, SesiLayanan

# Register your models here.
admin.site.register(KategoriJasa)
admin.site.register(SubkategoriJasa)
admin.site.register(SesiLayanan)