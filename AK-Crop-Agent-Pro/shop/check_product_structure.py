import sqlite3

conn = sqlite3.connect("Database/collection_v2.db")
cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM products
LIMIT 1
""")

print(cursor.fetchone())

conn.close()