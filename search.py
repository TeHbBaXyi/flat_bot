import csv, sqlite3
def max_peice():
    conn = sqlite3.connect('flats.db')

#res = conn.execute("SELECT district FROM appart WHERE id = 2").fetchone()
    conn.close()