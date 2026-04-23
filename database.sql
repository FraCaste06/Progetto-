CREATE TABLE categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL
);

CREATE TABLE spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    importo REAL CHECK(importo > 0),
    categoria_id INTEGER,
    descrizione TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

CREATE TABLE budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL,
    categoria_id INTEGER,
    importo REAL CHECK(importo > 0),
    FOREIGN KEY (categoria_id) REFERENCES categorie(id),
    UNIQUE (mese, categoria_id)
);

CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT,
    categoria_id INTEGER,
    importo REAL,
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);