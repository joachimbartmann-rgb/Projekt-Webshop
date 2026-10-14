from pathlib import Path
import sqlite3

database_file = (
    Path(__file__).parent /
    "collection_v2.db"
)

conn = sqlite3.connect(database_file)

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name;
""")

tables = cursor.fetchall()

print()
print("=" * 60)
print("TABELLEN")
print("=" * 60)

for table in tables:
    print(table[0])

print()
print(f"Gesamt: {len(tables)} Tabellen")

conn.close()