from pathlib import Path
import sqlite3

db = Path(__file__).parent / "collection_v2.db"

conn = sqlite3.connect(db)
cursor = conn.cursor()

cursor.execute("""
DELETE FROM products
WHERE artikelnummer = 'nan'
""")

conn.commit()

print("Gelöscht:", cursor.rowcount)

conn.close()