-- Trigger dan Stored Procedure Darren Hijau

CREATE OR REPLACE FUNCTION handle_order_cancellation()
RETURNS TRIGGER AS $$
DECLARE
    pelanggan_id UUID;
    total_biaya NUMERIC;
    id_status_dibatalkan INTEGER;
    id_status_mencari_pekerja INTEGER;
BEGIN
    -- Mendapatkan IdStatus untuk 'Dibatalkan' dan 'Mencari Pekerja Terdekat'
    SELECT Id INTO id_status_dibatalkan FROM STATUS_PESANAN WHERE Keterangan = 'Dibatalkan';
    SELECT Id INTO id_status_mencari_pekerja FROM STATUS_PESANAN WHERE Keterangan = 'Mencari Pekerja Terdekat';
    
    -- Memeriksa apakah status diubah menjadi 'Dibatalkan'
    IF NEW.IdStatus = id_status_dibatalkan THEN
        -- Memeriksa apakah status sebelumnya adalah 'Mencari Pekerja Terdekat'
        IF OLD.IdStatus = id_status_mencari_pekerja THEN
            -- Mengambil IdPelanggan dan TotalBiaya dari pemesanan
            SELECT IdPelanggan, TotalBiaya INTO pelanggan_id, total_biaya
            FROM TR_PEMESANAN_JASA
            WHERE Id = NEW.IdTrPemesanan;
            
            -- Mengembalikan saldo ke MyPay pelanggan
            UPDATE MYPAY
            SET Saldo = Saldo + total_biaya
            WHERE Id = pelanggan_id;
            
            -- Logging (opsional)
            RAISE NOTICE 'Saldo MyPay untuk pelanggan % dikembalikan sebesar %', pelanggan_id, total_biaya;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Membuat trigger untuk memanggil fungsi handle_order_cancellation setelah update pada TR_PEMESANAN_STATUS
CREATE TRIGGER trg_handle_order_cancellation
AFTER UPDATE ON TR_PEMESANAN_STATUS
FOR EACH ROW
EXECUTE FUNCTION handle_order_cancellation();

