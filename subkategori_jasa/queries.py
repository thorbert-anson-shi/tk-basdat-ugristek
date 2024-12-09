def set_syntax():
    return f"""
        SET search_path TO sijarta, public;
    """

def subkategori_syntax(subkategori_id):
    return f"""
        SELECT *
        FROM subkategori_jasa
        WHERE id = '{subkategori_id}';
    """

def kategori_syntax(subkategori_id):
    return f"""
        SELECT *
        FROM kategori_jasa
        WHERE id = 
        (SELECT kategorijasaid
        FROM subkategori_jasa
        WHERE id = '{subkategori_id}'
        );
    """

def sesi_layanan_syntax(subkategori_id):
    return f"""
        SELECT *
        FROM sesi_layanan
        WHERE subkategoriid = '{subkategori_id}';
    """

def pekerja_list_syntax(subkategori_id):
    return f"""
        SELECT DISTINCT U.id::text, U.nama, U.jeniskelamin, U.nohp, U.pwd, U.tgllahir, U.alamat, U.saldomypay
        FROM users U
        JOIN pekerja P on U.id = P.id
        JOIN pekerja_kategori_jasa PKJ on PKJ.pekerjaid = P.id
        WHERE PKJ.kategorijasaid = 
        (SELECT kategorijasaid
        FROM subkategori_jasa
        WHERE id = '{subkategori_id}'
        );
    """

def testimoni_list_syntax(subkategori_id):
    return f"""
        SELECT *
        FROM testimoni
        WHERE idtrpemesanan = 
        (SELECT id
        FROM tr_pemesanan_jasa
        WHERE idkategorijasa = 
        (SELECT kategorijasaid
        FROM subkategori_jasa
        WHERE id = '{subkategori_id}'
        )
        );
    """

def select_diskon_val_syntax(kode):
    return f"""
        SELECT DISTINCT diskon.kode, diskon.potongan, diskon.mintrpemesanan
        FROM diskon
        JOIN promo ON diskon.kode = promo.kode
        JOIN tr_pembelian_voucher ON diskon.kode = tr_pembelian_voucher.idvoucher
        WHERE promo.tglakhirberlaku >= CURR_DATE
        AND tr_pembelian_voucher.tglawal <= CURR_DATE
        AND tr_pembelian_voucher.tglakhir >= CURR_DATE
        AND diskon.kode = '{kode}';
    """

def metode_bayar_list_syntax():
    return f"""
        SELECT *
        FROM metode_bayar;
    """

def terdaftar_syntax(pekerja_id, kategori_id):
    return f"""
        SELECT EXISTS(
        SELECT 1
        FROM pekerja_kategori_jasa
        WHERE pekerjaid = '{pekerja_id}'
        AND kategorijasaid = '{kategori_id}'
        ) AS status_terdaftar;
    """

def tambah_pekerja():
    return """
        INSERT INTO pekerja_kategori_jasa (pekerjaid, kategorijasaid)
        VALUES (%s, %s);
    """

def cek_pekerja():
    return """
        SELECT COUNT(*)
        FROM pekerja_kategori_jasa
        WHERE pekerjaid = %s
        AND kategorijasaid = %s;
    """

def delete_status_syntax():
    return """
        DELETE 
        FROM tr_pemesanan_status
        WHERE idtrPpemesanan = %s;
    """

def delete_pesanan_syntax():
    return """
        DELETE
        FROM tr_pemesanan_jasa
        WHERE id = %s;
    """

def tambah_tr_pemesanan_jasa_berdiskon():
    return """
        INSERT INTO
        tr_pemesanan_jasa (
            id, idpelanggan, idkategorijasa, sesi, tglpemesanan, totalbiaya, tglpekerjaan, waktupekerjaan, idpekerja, idmetodebayar, iddiskon
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, %s, %s);
    """

def tambah_tr_pemesanan_jasa_tanpadiskon():
    return """
        INSERT INTO
        tr_pemesanan_jasa (
            id, idpelanggan, idkategorijasa, sesi, tglpemesanan, totalbiaya, tglpekerjaan, waktupekerjaan, idpekerja, idmetodebayar, iddiskon
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, %s, NULL);
    """

def tr_tambah_pemesanan_status():
    return """
        INSERT INTO tr_pemesanan_status (
            idtrpemesanan, idstatus, tglwaktu
        ) VALUES (%s, %s, %s);
    """