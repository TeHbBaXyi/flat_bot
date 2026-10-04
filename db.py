import csv, sqlite3
def init_db():
    conn = sqlite3.connect('flats.db')
    conn.execute("""
                CREATE TABLE IF NOT EXISTS appart
                (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    district TEXT,
                    metro TEXT,
                    rooms INTEGER,
                    price INTEGER,
                    area REAL,
                    pets_allowed INTEGER,
                    description TEXT
                )
                """)
    with open("list_appart.csv", encoding="utf-8-sig") as database:
        for row in csv.DictReader(database):
            conn.execute(
                "INSERT OR REPLACE INTO appart values(?,?,?,?,?,?,?,?,?)",
                (row["id"], row["title"], row["district"], row["metro"],
                 row["rooms"], row["price"], row["area"],
                 row["pets_allowed"], row["description"])
            )
    conn.commit()
    conn.close()
init_db()
