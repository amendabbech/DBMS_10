CREATE TABLE spender (
    spender_id SERIAL PRIMARY KEY,
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    geburtsdatum DATE NOT NULL,
    blutgruppe VARCHAR(3) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE spendezentrum (
    zentrum_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    adresse VARCHAR(255) NOT NULL,
    stadt VARCHAR(100) NOT NULL
);

CREATE TABLE spende (
    spende_id SERIAL PRIMARY KEY,
    spender_id INTEGER NOT NULL REFERENCES spender(spender_id),
    zentrum_id INTEGER NOT NULL REFERENCES spendezentrum(zentrum_id),
    spende_datum DATE NOT NULL,
    menge_ml INTEGER NOT NULL CHECK (menge_ml > 0)
);

CREATE OR REPLACE FUNCTION pruefe_spendeabstand()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM spende
        WHERE spender_id = NEW.spender_id
        AND spende_datum > NEW.spende_datum - INTERVAL '56 days'
        AND spende_datum < NEW.spende_datum + INTERVAL '56 days'
    ) THEN
        RAISE EXCEPTION 'Mindestabstand von 56 Tagen zwischen Spenden nicht eingehalten';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_spendeabstand
BEFORE INSERT ON spende
FOR EACH ROW
EXECUTE FUNCTION pruefe_spendeabstand();
