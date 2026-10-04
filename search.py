import sqlite3
def max_price():
    price_user = int(input("Укажите максимальную цену квартиры: "))
    conn = sqlite3.connect('flats.db')
    res = conn.execute("SELECT price, district, metro, rooms, area, pets_allowed FROM appart WHERE price <= ?",
                       (price_user,)).fetchall()
    for row in res:
        print(f"Цена {row[0]} руб, район {row[1]}, метро {row[2]}, комнат {row[3]}, квартира {row[4]} кв метра, c животными {("можно" if row[5] == 1 else "нельзя")}")
    conn.close()
max_price()