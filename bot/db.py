import csv, os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

CSV_PATH = Path(__file__).parent / "list_appart.csv"


def init_db():
    load_dotenv()
    with psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USER"),
    ) as conn:
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

        with open(CSV_PATH, encoding="utf-8-sig") as database:
            for row in csv.DictReader(database):
                conn.execute("""
                    INSERT INTO appart VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        district = EXCLUDED.district,
                        metro = EXCLUDED.metro,
                        rooms = EXCLUDED.rooms,
                        price = EXCLUDED.price,
                        area = EXCLUDED.area,
                        pets_allowed = EXCLUDED.pets_allowed,
                        description = EXCLUDED.description
                """, (row["id"], row["title"], row["district"], row["metro"],
                      row["rooms"], row["price"], row["area"],
                      row["pets_allowed"], row["description"]))
if __name__ == "__main__":
    init_db()
