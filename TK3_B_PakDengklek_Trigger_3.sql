-- Trigger dan Stored Procedure Valentino Biru

-- -----------------------------------------------------
-- Fungsi: pembatasan_penggunaan
-- Deskripsi:
--            - Memastikan voucher tidak kedaluwarsa.
--            - Memastikan voucher masih memiliki kuota penggunaan.
--            - Mengurangi kuota penggunaan jika voucher valid.
-- -----------------------------------------------------

CREATE OR REPLACE FUNCTION pembatasan_penggunaan()
RETURNS TRIGGER AS $$
DECLARE
    tanggal_akhir DATE;
    telah_digunakan INT;
    batas_penggunaan INT;
    id_pembelian INT;
BEGIN

    -- Ambil tanggal akhir, telah digunakan, kuota penggunaan, dan id_pembelian dari 
    -- tr_pembelian_voucher dengan Id tertentu.
    SELECT tpv.TglAkhir, tpv.TelahDigunakan, v.KuotaPenggunaan, tpv.Id
    INTO tanggal_akhir, telah_digunakan, batas_penggunaan, id_pembelian
    FROM tr_pembelian_voucher tpv
    JOIN voucher v ON v.kode = tpv.IdVoucher
    WHERE tpv.Id = NEW.Id;

    -- Kalau voucher sudah kedaluwarsa, hapuslah voucher tersebut dari relasi tr_pembelian_voucher.
    IF CURRENT_DATE > tanggal_akhir THEN
        RAISE EXCEPTION 'Voucher "%" sudah kedaluwarsa.', NEW.Kode;
        DELETE FROM tr_pembelian_voucher
        WHERE Id = id_pembelian;

    -- Kalau penggunaan voucher sudah sama dengan atau melewati batas penggunaan, 
    -- hapuslah voucher tersebut dari relasi tr_pembelian_voucher.
    ELSIF telah_digunakan >= batas_penggunaan THEN
        RAISE EXCEPTION 'Kuota penggunaan voucher "%" sudah habis.', NEW.Kode;
        DELETE FROM tr_pembelian_voucher
        WHERE Id = id_pembelian;

    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_pembatasan_penggunaan
BEFORE UPDATE ON tr_pembelian_voucher
FOR EACH ROW
EXECUTE FUNCTION pembatasan_penggunaan();