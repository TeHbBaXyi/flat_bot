import sqlite3
def search(price_user=None, rooms_user=None, pets_allowed_user=None, metro_user=None,  area_user=None, district_user=None):
    conn = sqlite3.connect('../flats.db')

    res = conn.execute("SELECT price, district, metro, rooms, area, pets_allowed FROM appart WHERE price <= ?",
                       (price_user,)).fetchall()
    conn.close()
    return res
if __name__ == '__main__':
    res = search(int(input("Укажите максимальную цену квартиры: ")))
    for row in res:
        print(f"Цена {row[0]} руб, район {row[1]}, метро {row[2]}, комнат {row[3]}, квартира {row[4]} кв метра, c животными {("можно" if row[5] == 1 else "нельзя")}")