from db import connect_db

def search(price=None, rooms=None, pets_allowed=None, metro=None,  area=None, district=None):
    with connect_db() as conn:
        sql = "SELECT price, district, metro, rooms, area, pets_allowed FROM appart WHERE 1 = 1"

        params = []
        if price is not None:
            sql += " AND price <= %s"
            params.append(price)
        if district is not None:
            quantity = ", ".join("%s" * len(district))
            sql += f" AND district IN ({quantity})"
            params.extend(district)
        if rooms is not None:
            sql += " AND rooms = %s"
            params.append(rooms)
        if metro is not None:
            quantity = ", ".join("%s" * len(metro))
            sql += f" AND metro IN ({quantity})"
            params.extend(metro)
        if area is not None:
            sql += " AND area >= %s"
            params.append(area)
        if pets_allowed == 1:
            sql += " AND pets_allowed = 1"
        res = conn.execute(sql, params).fetchall()
        return res