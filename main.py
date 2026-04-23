import sqlite3

conn = sqlite3.connect("progetto.db")
cursor = conn.cursor()

with open("database.sql", "r") as f:
    cursor.executescript(f.read())

conn.commit()

print("Database creato!")

while True:
    print("\n1. Aggiungi categoria")
    print("2. Inserisci spesa")
    print("3. Imposta budget")
    print("4. Report totale per categoria")
    print("5. Report budget mensile")
    print("6. Report Elenco completo spese")
    print("7. Esci")

    scelta = input("Scelta: ")

    # -------------------------
    # CATEGORIA
    # -------------------------
    if scelta == "1":
        nome = input("Nome categoria: ")

        if nome == "":
            print("Errore: nome categoria vuoto")
            continue

        cursor.execute("SELECT * FROM categorie WHERE nome = ?", (nome,))
        risultato = cursor.fetchone()

        if risultato:
            print("La categoria esiste già")
        else:
            cursor.execute("INSERT INTO categorie(nome) VALUES(?)", (nome,))
            conn.commit()
            print("Categoria inserita correttamente")

    # -------------------------
    # SPESA
    # -------------------------
    elif scelta == "2":
        data = input("Data (YYYY-MM-DD): ")
        importo = float(input("Importo: "))
        categoria = input("Categoria: ")
        descrizione = input("Descrizione: ")

        if importo <= 0:
            print("Errore: importo non valido")
            continue

        cursor.execute("SELECT id FROM categorie WHERE nome = ?", (categoria,))
        risultato = cursor.fetchone()

        if not risultato:
            print("Errore: categoria non esiste")
            continue

        categoria_id = risultato[0]

        cursor.execute("""
            INSERT INTO spese(data, importo, categoria_id, descrizione)
            VALUES (?, ?, ?, ?)
        """, (data, importo, categoria_id, descrizione))

        conn.commit()
        print("Spesa inserita!")

    # -------------------------
    # BUDGET
    # -------------------------
    elif scelta == "3":
        mese = input("Mese (YYYY-MM): ")
        categoria = input("Categoria: ")

        try:
            importo = float(input("Budget: "))
        except:
            print("Errore: inserisci un numero valido")
            continue

        if importo <= 0:
            print("Errore: budget non valido")
            continue

        cursor.execute("SELECT id FROM categorie WHERE nome = ?", (categoria,))
        risultato = cursor.fetchone()

        if not risultato:
            print("Errore: categoria non esiste")
            continue

        categoria_id = risultato[0]

        cursor.execute("""
            SELECT * FROM budget 
            WHERE mese = ? AND categoria_id = ?
        """, (mese, categoria_id))

        esiste = cursor.fetchone()

        if esiste:
            cursor.execute("""
                UPDATE budget
                SET importo = ?
                WHERE mese = ? AND categoria_id = ?
            """, (importo, mese, categoria_id))
        else:
            cursor.execute("""
                INSERT INTO budget(mese, categoria_id, importo)
                VALUES (?, ?, ?)
            """, (mese, categoria_id, importo))

        conn.commit()
        print("Budget mensile salvato correttamente")

    # -------------------------
    # REPORT 1
    # -------------------------
    elif scelta == "4":
        cursor.execute("""
            SELECT categorie.nome, IFNULL(SUM(spese.importo), 0)
            FROM categorie
            LEFT JOIN spese ON categorie.id = spese.categoria_id
            GROUP BY categorie.nome
        """)

        risultati = cursor.fetchall()

        print("\n--- TOTALE SPESE PER CATEGORIA ---")

        for nome, totale in risultati:
            print(f"{nome}: {totale}€")

    # -------------------------
    # REPORT 2
    # -------------------------
    elif scelta == "5":
        mese = input("Mese (YYYY-MM): ")

        cursor.execute("""
            SELECT 
                categorie.nome,
                IFNULL(SUM(spese.importo), 0),
                IFNULL(budget.importo, 0)
            FROM categorie
            LEFT JOIN spese 
                ON categorie.id = spese.categoria_id 
                AND substr(spese.data, 1, 7) = ?
            LEFT JOIN budget 
                ON categorie.id = budget.categoria_id 
                AND budget.mese = ?
            GROUP BY categorie.nome
        """, (mese, mese))

        risultati = cursor.fetchall()

        print("\n--- REPORT BUDGET ---")

        for nome, totale_speso, budget in risultati:
            print(f"\nCategoria: {nome}")
            print(f"Speso: {totale_speso}€")
            print(f"Budget: {budget}€")

            if budget > 0:
                diff = budget - totale_speso
                if diff >= 0:
                    print(f"Puoi spendere ancora {diff}€ 🥳")
                else:
                    print(f"Hai superato il budget di {-diff}€ 😱")

    # -------------------------
    # REPORT 3
    # -------------------------
    elif scelta == "6":
        cursor.execute("""
            SELECT spese.data, categorie.nome, spese.importo, spese.descrizione
            FROM spese
            JOIN categorie ON spese.categoria_id = categorie.id
            ORDER BY spese.data DESC
        """)

        risultati = cursor.fetchall()

        print("\n--- ELENCO SPESE ---")

        if not risultati:
            print("Nessuna spesa trovata")
        else:
            for data, categoria, importo, descrizione in risultati:
                print(f"{data} | {categoria} | {importo}€ | {descrizione}")

    # -------------------------
    # ESCI
    # -------------------------
    elif scelta == "7":
        break

    else:
        print("Scelta non valida")