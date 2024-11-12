from django.db import models
import uuid

# Create your models here.
class KategoriJasa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_kategori = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_kategori

class SubkategoriJasa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_subkategori = models.CharField(max_length=255)
    deskripsi = models.TextField()
    kategori_jasa = models.ForeignKey(KategoriJasa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama_subkategori

class SesiLayanan(models.Model):
    subkategori = models.ForeignKey(SubkategoriJasa, on_delete=models.CASCADE)
    sesi = models.IntegerField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('subkategori', 'sesi')

    def __str__(self):
        return f"Sesi {self.sesi} - {self.subkategori.nama_subkategori}"