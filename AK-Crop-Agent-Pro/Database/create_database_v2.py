from pathlib import Path
import sqlite3

# -----------------------------------------
# Pfade
# -----------------------------------------

database_dir = Path(__file__).parent

schema_file = (
    database_dir /
    "schema_v2.sql"
)

database_file = (
    database_dir /
    "collection_v2.db"
)

# -----------------------------------------
# Datenbank erzeugen
# -----------------------------------------

conn = sqlite3.connect(
    database_file
)

cursor = conn.cursor()

with open(
    schema_file,
    "r",
    encoding="utf-8"
) as f:

    schema = f.read()

cursor.executescript(schema)

conn.commit()

print()
print("=" * 60)
print("DATABASE V2 ERSTELLT")
print(database_file)
print("=" * 60)

conn.close()