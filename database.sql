CREATE TABLE IF NOT EXISTS categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    importo REAL CHECK(importo > 0),
    categoria_id INTEGER,
    descrizione TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL,
    categoria_id INTEGER,
    importo REAL CHECK(importo > 0),
    FOREIGN KEY (categoria_id) REFERENCES categorie(id),
    UNIQUE (mese, categoria_id)
);

INSERT INTO categorie (nome) VALUES ('Cibo');
INSERT INTO categorie (nome) VALUES ('Trasporti');
INSERT INTO categorie (nome) VALUES ('Svago');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2026-04-01', 12.5, 1, 'Pranzo');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2026-04-02', 2.5, 2, 'Metro');

INSERT INTO spese (data, importo, categoria_id, descrizione)
VALUES ('2026-04-03', 20.0, 3, 'Cinema');

INSERT INTO budget (mese, categoria_id, importo)
VALUES ('2026-04', 1, 200);

INSERT INTO budget (mese, categoria_id, importo)
VALUES ('2026-04', 2, 100);

INSERT INTO budget (mese, categoria_id, importo)
VALUES ('2026-04', 3, 150);
