from pathlib import Path
import sqlite3

# --------------------------------------------------
# Pfade
# --------------------------------------------------

project_root = Path(__file__).parent.parent

database_dir = Path(__file__).parent

database_file = (
    database_dir /
    "postcards.db"
)

# --------------------------------------------------
# Verbindung
# --------------------------------------------------

conn = sqlite3.connect(
    database_file
)

cursor = conn.cursor()

# --------------------------------------------------
# Tabelle erstellen
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS postcards (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    artikelnummer TEXT UNIQUE,

    titel TEXT,
    ort TEXT,
    region TEXT,
    land TEXT,

    verlag TEXT,
    kategorie TEXT,

    zustand TEXT,
    gelaufen TEXT,

    jahr TEXT,

    beschreibung TEXT,

    preis REAL,

    status TEXT,

    bild_v TEXT,
    bild_r TEXT
)
""")

conn.commit()

print()
print("=" * 60)
print("Datenbank erfolgreich erstellt")
print(database_file)
print("=" * 60)

conn.close()