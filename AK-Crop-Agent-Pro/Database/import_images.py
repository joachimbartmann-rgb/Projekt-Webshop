from pathlib import Path
import sqlite3

# ----------------------------------------
# Datenbank
# ----------------------------------------

db_file = (
    Path(__file__).parent /
    "collection_v2.db"
)

# ----------------------------------------
# Bildordner
# ----------------------------------------

image_dir = Path(
    r"C:\_docs\Ansichtskarten\Import"
)

# ----------------------------------------
# Verbindung
# ----------------------------------------

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

count = 0

# ----------------------------------------
# Bilder suchen
# ----------------------------------------

for file in image_dir.rglob("*"):

    if not file.is_file():
        continue

    if file.suffix.lower() not in [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]:
        continue

    filename = file.name
    stem = file.stem

    if "_" not in stem:
        continue

    artikelnummer = stem.split("_")[0]

    bildtyp = "unknown"

    if stem.endswith("_v"):
        bildtyp = "front"

    elif stem.endswith("_r"):
        bildtyp = "back"

    cursor.execute("""
    INSERT INTO images
    (
        artikelnummer,
        bildtyp,
        dateiname,
        dateipfad
    )
    VALUES (?, ?, ?, ?)
    """, (
        artikelnummer,
        bildtyp,
        filename,
        str(file)
    ))

    count += 1

conn.commit()

print()
print("=" * 60)
print("BILDER IMPORTIERT")
print("=" * 60)

print()

print("Importierte Bilder:", count)

print()

conn.close()