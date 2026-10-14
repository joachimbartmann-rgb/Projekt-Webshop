from pathlib import Path
import sqlite3

db = Path(__file__).parent / "collection_v2.db"

conn = sqlite3.connect(db)

cursor = conn.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM products
""")

count = cursor.fetchone()[0]

print()
print("Produkte:", count)

conn.close()