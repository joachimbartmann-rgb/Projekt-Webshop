from pathlib import Path
import sqlite3

db = Path(__file__).parent / "collection_v2.db"

conn = sqlite3.connect(db)
cursor = conn.cursor()

cursor.execute("""
SELECT artikelnummer, titel
FROM products
WHERE artikelnummer='AK-2026-0342'
""")

print(cursor.fetchall())

conn.close()