-- Trigger dan Stored Procedure Thorbert Merah

CREATE OR REPLACE FUNCTION IncrementWorkerBalance()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_IdPekerja UUID;
    v_TotalBiaya DECIMAL;
    v_KategoriId UUID;
    v_Tgl DATE := CURRENT_DATE;
BEGIN
    SELECT IdPekerja, TotalBiaya
    INTO v_IdPekerja, v_TotalBiaya
    FROM tr_pemesanan_jasa
    WHERE Id = TG_ARGV[0];

    -- Increment the worker's balance
    UPDATE users
    SET SaldoMyPay = COALESCE(SaldoMyPay, 0) + v_TotalBiaya
    WHERE Id = v_IdPekerja;

    INSERT INTO tr_mypay (Id, usersId, Tgl, Nominal, KategoriId)
    VALUES (
        uuid_generate_v4(),
        v_IdPekerja,
        v_Tgl,
        v_TotalBiaya,
        (SELECT id FROM kategori_tr_mypay WHERE LOWER(nama) = 'menerima honor transaksi jasa')
    );

    RAISE NOTICE 'Transaction recorded for worker %, amount: %', v_IdPekerja, v_TotalBiaya;
END;
$$;

CREATE OR REPLACE FUNCTION GetSelesaiStatusId()
RETURNS UUID
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT id FROM status_pesanan WHERE statuspesanan = 'Selesai';
END;
$$;

CREATE OR REPLACE TRIGGER check_order_completion
AFTER INSERT ON tr_pemesanan_status
FOR EACH ROW
WHEN (NEW.idstatus = GetSelesaiStatusId())
EXECUTE FUNCTION IncrementWorkerBalance(IdTrPemesanan);
