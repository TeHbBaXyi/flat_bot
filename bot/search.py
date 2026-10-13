from pathlib import Path
from dotenv import load_dotenv
from db import connect_db
#import sqlite3
import csv, os, psycopg
CSV_PATH = Path(__file__).parent / "list_appart.csv"
def search(price=None, rooms=None, pets_allowed=None, metro=None,  area=None, district=None):
    conn = connect_db()
    with open(CSV_PATH, encoding="utf-8-sig") as database:
        sql = "SELECT price, district, metro, rooms, area, pets_allowed FROM appart WHERE 1 = 1"

        params = []
        if price is not None:
            sql += " AND price <= ?"
            params.append(price)
        if district is not None:
            quantity = ", ".join("?" * len(district))
            sql += f" AND district IN ({quantity})"
            params.extend(district)
        if rooms is not None:
            sql += " AND rooms = ?"
            params.append(rooms)
        if metro is not None:
            quantity = ", ".join("?" * len(metro))
            sql += f" AND metro IN ({quantity})"
            params.extend(metro)
        if area is not None:
            sql += " AND area >= ?"
            params.append(area)
        if pets_allowed == 1:
            sql += " AND pets_allowed = 1"
        res = conn.execute(sql, params).fetchall()


    return res