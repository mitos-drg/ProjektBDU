-- Clean-up existing database tables
DROP TABLE IF EXISTS Wybory CASCADE;
DROP TABLE IF EXISTS Wyborcy CASCADE;
DROP TABLE IF EXISTS Glosy CASCADE;
DROP TABLE IF EXISTS Kandydaci CASCADE;

-- Create necessary tables
CREATE TABLE Wybory
(
    id         SERIAL PRIMARY KEY,
    nazwa      VARCHAR(40) NOT NULL,
    posady     INTEGER CHECK (posady > 0),
    zgloszenia TIMESTAMP,
    poczatek   TIMESTAMP,
    koniec     TIMESTAMP,
    publiczne  BOOLEAN,
    CHECK (poczatek < koniec),
    CHECK (zgloszenia < poczatek)
);

CREATE TABLE Wyborcy
(
    indeks   CHAR(6) PRIMARY KEY,
    imie     VARCHAR(32) NOT NULL,
    nazwisko VARCHAR(64) NOT NULL,
    haslo    VARCHAR(32) NOT NULL
);

CREATE TABLE Kandydaci
(
    wybory INTEGER NOT NULL REFERENCES Wybory,
    indeks CHAR(6) NOT NULL REFERENCES Wyborcy,
    glosy  INTEGER,
    PRIMARY KEY (wybory, indeks)
);

CREATE TABLE Glosy
(
    wybory   INTEGER NOT NULL REFERENCES Wybory,
    wyborca  CHAR(6) NOT NULL REFERENCES Wyborcy,
    kandydat CHAR(6) NOT NULL,
    PRIMARY KEY (wybory, wyborca, kandydat)
);

-- Add Election Committee special user
INSERT INTO Wyborcy VALUES ('000000', 'Komisja', 'Wyborcza', 'Admin1');

-- Define API perspectives for use by applications
CREATE VIEW ElectionsAPI(id, name, seats, submit, start, ends, is_public) AS
    SELECT id, nazwa, posady, zgloszenia, poczatek, koniec, publiczne FROM Wybory;

CREATE VIEW VotersAPI(index, name, surname, password) AS
    SELECT indeks, imie, nazwisko, haslo FROM Wyborcy;

CREATE VIEW NomineesAPI(election, nominee, votes) AS
    SELECT wybory, indeks, glosy FROM Kandydaci;

CREATE VIEW VotesAPI(election, voter, nominee) AS
    SELECT wybory, wyborca, kandydat FROM Glosy;
