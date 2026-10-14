from pathlib import Path
import sqlite3

db = Path(__file__).parent / "collection_v2.db"

conn = sqlite3.connect(db)

cursor = conn.cursor()

cursor.execute("""
SELECT artikelnummer, titel
FROM products
ORDER BY id DESC
LIMIT 20
""")

for row in cursor.fetchall():
    print(row)

conn.close()