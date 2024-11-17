from django.shortcuts import render
from django.db import connection

# Fungsi untuk tampilkan halaman diskon beserta data voucher dan promo.
def show_hal_diskon(request):

    # Bagian ini nanti ditambahkan pada TK3.
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM diskon d JOIN voucher v ON d.Kode = v.Kode")
    #     voucher = cursor.fetchall()
    #     cursor.execute("SELECT * FROM promo")
    #     promo = cursor.fetchall()

    # context = {
    #     'data_voucher': voucher,
    #     'data_promo': promo,
    # }

    return render(request, "hal_diskon.html")

'''
Tempat tampung trigger dan stored procedure sementara

Pembatasan penggunaan voucher:
Ketika pengguna ingin menggunakan voucher lakukan pengecekan 
bahwa voucher yang digunakan tidak melewati batas jumlah penggunaan atau batasan hari berlaku. 
Jika voucher telah melewati batas jumlah penggunaan atau batasan hari berlaku maka keluarkan pesan error.

CREATE OR REPLACE FUNCTION pembatasan_penggunaan() RETURNS TRIGGER
AS $$
DECLARE
    jumlah_hari_berlaku INT;
    kuota_penggunaan INT;
BEGIN
    SELECT v.JmlHariBerlaku, v.KuotaPenggunaan
    INTO jumlah_hari_berlaku, kuota_penggunaan
    FROM voucher v
    WHERE v.Kode = NEW.Kode;

    IF jumlah_hari_berlaku > 0 AND kuota_penggunaan > 0 THEN
        UPDATE voucher
        SET kuota_penggunaan = kuota_penggunaan - 1
        WHERE Kode = NEW.Kode;

    ELSIF jumlah_hari_berlaku <= 0 THEN
        RAISE EXCEPTION 'Voucher % sudah kedaluwarsa', NEW.Kode;
    
    ELSE
        RAISE EXCEPTION 'Kuota penggunaan voucher % sudah habis', NEW.Kode;
    ENDIF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_pembatasan_penggunaan
BEFORE UPDATE ON voucher
FOR EACH ROW EXECUTE FUNCTION pembatasan_penggunaan();
'''