-- Trigger dan Stored Procedure Thorbert Hijau

CREATE OR REPLACE FUNCTION IncrementWorkerBalance(p_IdPemesanan UUID)
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    v_IdPekerja UUID;
    v_TotalBiaya DECIMAL;
BEGIN
    SELECT IdPekerja, TotalBiaya
    INTO v_IdPekerja, v_TotalBiaya
    FROM tr_pemesanan_jasa
    WHERE Id = p_IdPemesanan;

    UPDATE users
    SET SaldoMyPay = COALESCE(SaldoMyPay, 0) + v_TotalBiaya
    WHERE Id = v_IdPekerja;

    RAISE NOTICE 'Balance updated for worker %, new balance: %', v_IdPekerja, v_TotalBiaya;
END;
$$;

CREATE OR REPLACE TRIGGER check_order_completion
AFTER UPDATE OF idstatus ON tr_pemesanan_status
FOR EACH ROW
WHEN (OLD.idstatus IS DISTINCT FROM NEW.idstatus 
    AND NEW.idstatus = (SELECT id FROM status_pesanan WHERE statuspesanan = "Selesai"))
EXECUTE FUNCTION IncrementWorkerBalance(NEW.IdTrPemesanan);
