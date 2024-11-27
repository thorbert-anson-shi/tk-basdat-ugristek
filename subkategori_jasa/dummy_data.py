from datetime import datetime

# Dummy Data untuk Pengguna (User)
DUMMY_PENGGUNA = [
    {
        "id": "1",
        "nama": "Andi Wijaya",
        "password": "password123",
        "jenis_kelamin": "L",
        "no_hp": "08123456789",
        "tanggal_lahir": "1995-06-15",
        "alamat": "Jl. Contoh No. 1",
        "role": "pelanggan",
        "saldo_mypay": 1000000.00
    },
    {
        "id": "2",
        "nama": "Budi Santoso",
        "password": "password456",
        "jenis_kelamin": "L",
        "no_hp": "08198765432",
        "tanggal_lahir": "1990-03-22",
        "alamat": "Jl. Contoh No. 2",
        "role": "pekerja",
        "saldo_mypay": 1500000.00
    }
]



# Dummy Data untuk Pelanggan
DUMMY_PELANGGAN = [
    {
        "id": "1",
        "level": "Gold"
    }
]

# Dummy Data untuk Pekerja
DUMMY_PEKERJA = [
    {
        "id": "1",
        "nama": "Pekerja 1",  # Pastikan kunci 'nama' ada
        "nama_bank": "Bank Mandiri",
        "nomor_rekening": "1234567890",
        "npwp": "01.234.567.8-901.000",
        "link_foto": "https://example.com/foto/1.jpg",
        "rating": 4.5,
        "jml_pesanan_selesai": 150
    },
    {
        "id": "2",
        "nama": "Pekerja 2",  # Pastikan kunci 'nama' ada
        "nama_bank": "Bank BCA",
        "nomor_rekening": "0987654321",
        "npwp": "02.345.678.9-012.000",
        "link_foto": "https://example.com/foto/2.jpg",
        "rating": 4.0,
        "jml_pesanan_selesai": 120
    }
]


# Dummy Data untuk Kategori Jasa
DUMMY_KATEGORI_JASA = [
    {"id": "1", "nama_kategori": "Kategori Jasa 1"},
    {"id": "2", "nama_kategori": "Kategori Jasa 2"},
    {"id": "3", "nama_kategori": "Kategori Jasa 3"}
]

# Dummy Data untuk Subkategori Jasa
DUMMY_SUBKATEGORI_JASA = [
    {"id": "1", "nama_subkategori": "Subkategori Jasa 1", "kategori_jasa_id": "1", "deskripsi": "Deskripsi Subkategori 1"},
    {"id": "2", "nama_subkategori": "Subkategori Jasa 2", "kategori_jasa_id": "1", "deskripsi": "Deskripsi Subkategori 2"},
    {"id": "3", "nama_subkategori": "Subkategori Jasa 3", "kategori_jasa_id": "1", "deskripsi": "Deskripsi Subkategori 3"},
    {"id": "4", "nama_subkategori": "Subkategori Jasa 1", "kategori_jasa_id": "2", "deskripsi": "Deskripsi Subkategori 4"},
    {"id": "5", "nama_subkategori": "Subkategori Jasa 2", "kategori_jasa_id": "2", "deskripsi": "Deskripsi Subkategori 5"},
    {"id": "6", "nama_subkategori": "Subkategori Jasa 3", "kategori_jasa_id": "2", "deskripsi": "Deskripsi Subkategori 6"},
    {"id": "7", "nama_subkategori": "Subkategori Jasa 1", "kategori_jasa_id": "3", "deskripsi": "Deskripsi Subkategori 7"},
    {"id": "8", "nama_subkategori": "Subkategori Jasa 2", "kategori_jasa_id": "3", "deskripsi": "Deskripsi Subkategori 8"},
    {"id": "9", "nama_subkategori": "Subkategori Jasa 3", "kategori_jasa_id": "3", "deskripsi": "Deskripsi Subkategori 9"}
]

# Dummy Data untuk Pekerja_Kategori_Jasa
DUMMY_PEKERJA_KATEGORI_JASA = [
    {"pekerja_id": "2", "kategori_jasa_id": "1"},
    {"pekerja_id": "2", "kategori_jasa_id": "2"},
    {"pekerja_id": "2", "kategori_jasa_id": "3"}
]

DUMMY_VOUCHER = [
    {"kode": "DISKON10", "jml_hari_berlaku": 30, "kuota_penggunaan": 100},
    {"kode": "DISKON20", "jml_hari_berlaku": 60, "kuota_penggunaan": 50}
]

DUMMY_PROMO = [
    {"kode": "PROMO5", "deskripsi": "Promo potongan 5% untuk semua kategori."},
    {"kode": "PROMO10", "deskripsi": "Promo potongan 10% untuk pelanggan baru."}
]

DUMMY_TR_PEMESANAN_JASA = [
    {
        "id": "1",
        "tgl_pemesanan": datetime(2024, 4, 1),
        "tgl_pekerjaan": datetime(2024, 4, 5),
        "waktu_pekerjaan": datetime(2024, 4, 5, 10, 0, 0),
        "total_biaya": 900000.00,
        "id_pelanggan": "1",
        "id_pekerja": "2",
        "id_kategori_jasa": "1",
        "sesi": "Basic",
        "id_diskon": "DISKON10",
        "id_metode_bayar": "1"
    },
    {
        "id": "2",
        "tgl_pemesanan": datetime(2024, 4, 2),
        "tgl_pekerjaan": datetime(2024, 4, 6),
        "waktu_pekerjaan": datetime(2024, 4, 6, 14, 0, 0),
        "total_biaya": 2000000.00,
        "id_pelanggan": "1",
        "id_pekerja": "2",
        "id_kategori_jasa": "2",
        "sesi": "Advanced",
        "id_diskon": None,
        "id_metode_bayar": "2"
    }
]


# Dummy Data untuk Sesi Layanan
DUMMY_SESI_LAYANAN = [
    {"id": "1", "sesi": "Basic", "harga": 500000.00, "subkategori_id": "1"},
    {"id": "2", "sesi": "Standard", "harga": 1000000.00, "subkategori_id": "1"},
    {"id": "3", "sesi": "Premium", "harga": 1500000.00, "subkategori_id": "1"},
    {"id": "4", "sesi": "Basic", "harga": 2000000.00, "subkategori_id": "2"},
    {"id": "5", "sesi": "Advanced", "harga": 3000000.00, "subkategori_id": "2"}
]

# Dummy Data untuk Metode Bayar
DUMMY_METODE_BAYAR = [
    {"id": "1", "nama": "Transfer Bank"},
    {"id": "2", "nama": "Kartu Kredit"},
    {"id": "3", "nama": "MyPay"},
    {"id": "4", "nama": "GoPay"}
]

# Dummy Data untuk Diskon
DUMMY_DISKON = [
    {"id": "1", "kode": "DISKON10", "potongan": 10.00, "min_tr_pemesanan": 5},
    {"id": "2", "kode": "DISKON20", "potongan": 20.00, "min_tr_pemesanan": 10}
]

# Dummy Data untuk Testimoni
DUMMY_TESTIMONI = [
    {"id": "1", "tgl": datetime(2024, 4, 7), "teks": "Pelayanan cepat!", "rating": 5, "id_tr_pemesanan": "1"},
    {"id": "2", "tgl": datetime(2024, 4, 8), "teks": "Desain sangat bagus.", "rating": 4.5, "id_tr_pemesanan": "2"}
]

# Dummy Data untuk Status Pesanan
DUMMY_STATUS_PESANAN = [
    {"id": "1", "keterangan": "Menunggu Pembayaran"},
    {"id": "2", "keterangan": "Mencari Pekerja Terdekat"},
    {"id": "3", "keterangan": "Dibatalkan"},
    {"id": "4", "keterangan": "Selesai"}
]

# Dummy Data untuk TR_PEMESANAN_STATUS
DUMMY_TR_PEMESANAN_STATUS = [
    {"id_tr_pemesanan": "1", "id_status": 1, "tgl_waktu": datetime(2024, 4, 1, 9, 0, 0)},
    {"id_tr_pemesanan": "2", "id_status": 4, "tgl_waktu": datetime(2024, 4, 6, 15, 0, 0)}
]

# Dummy Data untuk MyPay
DUMMY_MYPAY = [
    {"id": "1", "saldo": 1000000.00},
    {"id": "2", "saldo": 1500000.00}
]
