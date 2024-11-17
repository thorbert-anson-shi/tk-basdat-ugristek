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
        RAISE EXCEPTION 'Voucher "%" sudah kedaluwarsa.', NEW.Kode;

    ELSE
        RAISE EXCEPTION 'Kuota penggunaan voucher "%" sudah habis.', NEW.Kode;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_pembatasan_penggunaan
BEFORE UPDATE ON voucher
FOR EACH ROW
EXECUTE FUNCTION pembatasan_penggunaan();