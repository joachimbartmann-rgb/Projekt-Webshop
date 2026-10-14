import sqlite3

conn = sqlite3.connect("Database/collection_v2.db")

cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM images
LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

conn.close()