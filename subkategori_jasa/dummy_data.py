from datetime import datetime, timedelta
import uuid

# Dummy Data untuk Pengguna (User)
DUMMY_PENGGUNA = [
    {
        "id": "11111111-1111-1111-1111-111111111111",
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
        "id": "22222222-2222-2222-2222-222222222222",
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
        "id": "11111111-1111-1111-1111-111111111111",
        "level": "Gold"
    }
]

# Dummy Data untuk Pekerja
DUMMY_PEKERJA = [
    {
        "id": "22222222-2222-2222-2222-222222222222",
        "nama_bank": "Bank Mandiri",
        "nomor_rekening": "1234567890",
        "npwp": "01.234.567.8-901.000",
        "link_foto": "https://example.com/foto/2222.jpg",
        "rating": 4.5,
        "jml_pesanan_selesai": 150
    }
]

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

# Dummy Data untuk Pekerja_Kategori_Jasa
DUMMY_PEKERJA_KATEGORI_JASA = [
    {
        "pekerja_id": "22222222-2222-2222-2222-222222222222",
        "kategori_jasa_id": "55555555-5555-5555-5555-555555555555"
    },
    {
        "pekerja_id": "22222222-2222-2222-2222-222222222222",
        "kategori_jasa_id": "66666666-6666-6666-6666-666666666666"
    }
]

# Dummy Data untuk Sesi Layanan
DUMMY_SESI_LAYANAN = [
    {
        "id": "99999999-9999-9999-9999-999999999999",
        "sesi": "Basic",
        "harga": 500000.00,
        "subkategori_id": "77777777-7777-7777-7777-777777777777"
    },
    {
        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "sesi": "Standard",
        "harga": 1000000.00,
        "subkategori_id": "77777777-7777-7777-7777-777777777777"
    },
    {
        "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        "sesi": "Premium",
        "harga": 1500000.00,
        "subkategori_id": "77777777-7777-7777-7777-777777777777"
    },
    {
        "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
        "sesi": "Basic",
        "harga": 2000000.00,
        "subkategori_id": "88888888-8888-8888-8888-888888888888"
    },
    {
        "id": "dddddddd-dddd-dddd-dddd-dddddddddddd",
        "sesi": "Advanced",
        "harga": 3000000.00,
        "subkategori_id": "88888888-8888-8888-8888-888888888888"
    }
]

# Dummy Data untuk Metode Bayar
DUMMY_METODE_BAYAR = [
    {
        "id": "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee",
        "nama": "Transfer Bank"
    },
    {
        "id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
        "nama": "Kartu Kredit"
    },
    {
        "id": "gggggggg-gggg-gggg-gggg-gggggggggggg",
        "nama": "MyPay"
    },
    {
        "id": "hhhhhhhh-hhhh-hhhh-hhhh-hhhhhhhhhhhh",
        "nama": "GoPay"
    }
]

# Dummy Data untuk Diskon
DUMMY_DISKON = [
    {
        "id": "iiiiiiii-iiii-iiii-iiii-iiiiiiiiiiii",
        "kode": "DISKON10",
        "potongan": 10.00,  # Representasi persentase
        "min_tr_pemesanan": 5
    },
    {
        "id": "jjjjjjjj-jjjj-jjjj-jjjj-jjjjjjjjjjjj",
        "kode": "DISKON20",
        "potongan": 20.00,
        "min_tr_pemesanan": 10
    }
]

# Dummy Data untuk Voucher
DUMMY_VOUCHER = [
    {
        "kode": "DISKON10",
        "jml_hari_berlaku": 30,
        "kuota_penggunaan": 100
    },
    {
        "kode": "DISKON20",
        "jml_hari_berlaku": 60,
        "kuota_penggunaan": 50
    }
]

# Dummy Data untuk Promo
DUMMY_PROMO = [
    {
        "kode": "PROMO5"
    },
    {
        "kode": "PROMO10"
    }
]

# Dummy Data untuk Pemesanan Jasa
DUMMY_TR_PEMESANAN_JASA = [
    {
        "id": "kkkkkkkk-kkkk-kkkk-kkkk-kkkkkkkkkkkk",
        "tgl_pemesanan": datetime(2024, 4, 1),
        "tgl_pekerjaan": datetime(2024, 4, 5),
        "waktu_pekerjaan": datetime(2024, 4, 5, 10, 0, 0),
        "total_biaya": 900000.00,
        "id_pelanggan": "11111111-1111-1111-1111-111111111111",
        "id_pekerja": "22222222-2222-2222-2222-222222222222",
        "id_kategori_jasa": "55555555-5555-5555-5555-555555555555",
        "sesi": "Basic",
        "id_diskon": "DISKON10",
        "id_metode_bayar": "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"
    },
    {
        "id": "llllllll-llll-llll-llll-llllllllllll",
        "tgl_pemesanan": datetime(2024, 4, 2),
        "tgl_pekerjaan": datetime(2024, 4, 6),
        "waktu_pekerjaan": datetime(2024, 4, 6, 14, 0, 0),
        "total_biaya": 2000000.00,
        "id_pelanggan": "11111111-1111-1111-1111-111111111111",
        "id_pekerja": "22222222-2222-2222-2222-222222222222",
        "id_kategori_jasa": "66666666-6666-6666-6666-666666666666",
        "sesi": "Advanced",
        "id_diskon": None,
        "id_metode_bayar": "gggggggg-gggg-gggg-gggg-gggggggggggg"
    }
]

# Dummy Data untuk Testimoni
DUMMY_TESTIMONI = [
    {
        "id": "mmmmmmmm-mmmm-mmmm-mmmm-mmmmmmmmmmmm",
        "tgl": datetime(2024, 4, 7),
        "teks": "Pelayanan cepat dan hasil memuaskan!",
        "rating": 5,
        "id_tr_pemesanan": "kkkkkkkk-kkkk-kkkk-kkkk-kkkkkkkkkkkk"
    },
    {
        "id": "nnnnnnnn-nnnn-nnnn-nnnn-nnnnnnnnnnnn",
        "tgl": datetime(2024, 4, 8),
        "teks": "Desain website sangat responsif.",
        "rating": 4.5,
        "id_tr_pemesanan": "llllllll-llll-llll-llll-llllllllllll"
    }
]

# Dummy Data untuk Status Pesanan
DUMMY_STATUS_PESANAN = [
    {
        "id": 1,
        "keterangan": "Menunggu Pembayaran"
    },
    {
        "id": 2,
        "keterangan": "Mencari Pekerja Terdekat"
    },
    {
        "id": 3,
        "keterangan": "Dibatalkan"
    },
    {
        "id": 4,
        "keterangan": "Selesai"
    }
]

# Dummy Data untuk TR_PEMESANAN_STATUS
DUMMY_TR_PEMESANAN_STATUS = [
    {
        "id_tr_pemesanan": "kkkkkkkk-kkkk-kkkk-kkkk-kkkkkkkkkkkk",
        "id_status": 1,  # Menunggu Pembayaran
        "tgl_waktu": datetime(2024, 4, 1, 9, 0, 0)
    },
    {
        "id_tr_pemesanan": "llllllll-llll-llll-llll-llllllllllll",
        "id_status": 4,  # Selesai
        "tgl_waktu": datetime(2024, 4, 6, 15, 0, 0)
    }
]

# Dummy Data untuk MyPay
DUMMY_MYPAY = [
    {
        "id": "11111111-1111-1111-1111-111111111111",
        "saldo": 1000000.00
    },
    {
        "id": "22222222-2222-2222-2222-222222222222",
        "saldo": 1500000.00
    }
]