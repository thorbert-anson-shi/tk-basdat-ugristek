-- Trigger dan Stored Procedure Danniel Kuning

CREATE OR REPLACE FUNCTION check_phone_number() RETURNS TRIGGER AS $$
BEGIN
    IF (EXISTS (SELECT * FROM users WHERE NoHP = NEW.NoHP)) THEN
        RAISE EXCEPTION 'Nomor telepon sudah terdaftar!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_phone_number BEFORE INSERT OR UPDATE OF nohp ON users 
FOR EACH ROW EXECUTE FUNCTION check_phone_number();

CREATE OR REPLACE FUNCTION check_bank_account() RETURNS TRIGGER AS $$
BEGIN
    IF (EXISTS (SELECT * FROM pekerja WHERE NomorRekening = NEW.NomorRekening AND NamaBank = NEW.NamaBank)) THEN
        RAISE EXCEPTION 'Nomor rekening dan Nama bank sudah terdaftar!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_bank_account BEFORE INSERT OR UPDATE OF NomorRekening, NamaBank ON pekerja 
FOR EACH ROW EXECUTE FUNCTION check_bank_account();