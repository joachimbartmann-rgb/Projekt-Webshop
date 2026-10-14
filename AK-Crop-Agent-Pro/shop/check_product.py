import sqlite3
from pathlib import Path

db_file = (
    Path(__file__).parent.parent /
    "Database" /
    "collection_v2.db"
)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM products
WHERE artikelnummer = 'AK-2026-0233'
""")

print(cursor.fetchone())

conn.close()