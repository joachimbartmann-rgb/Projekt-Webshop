from pathlib import Path
import sqlite3

# -------------------------------------
# Datenbank
# -------------------------------------

db_file = (
    Path(__file__).parent /
    "collection_v2.db"
)

conn = sqlite3.connect(db_file)

cursor = conn.cursor()

cursor.execute("""
SELECT artikelnummer
FROM products
""")

products = {
    row[0]
    for row in cursor.fetchall()
}

conn.close()

# -------------------------------------
# Bilder
# -------------------------------------

image_dir = Path(
    r"C:\_docs\Ansichtskarten\Import"
)

front = set()
back = set()

for file in image_dir.rglob("*"):

    if not file.is_file():
        continue

    name = file.stem

    if "_" not in name:
        continue

    artikelnummer = name.split("_")[0]

    if name.endswith("_v"):
        front.add(artikelnummer)

    elif name.endswith("_r"):
        back.add(artikelnummer)

# -------------------------------------
# Statistik
# -------------------------------------

complete = front & back

print()
print("=" * 60)
print("BILDABGLEICH")
print("=" * 60)

print()

print("Produkte:", len(products))
print("Vorderseiten:", len(front))
print("Rückseiten:", len(back))
print("Vollständig:", len(complete))

print()

missing_front = sorted(products - front)
missing_back = sorted(products - back)

print("Fehlende Vorderseiten:", len(missing_front))
print("Fehlende Rückseiten:", len(missing_back))

print()

print("Beispiele fehlende Vorderseite:")
for x in missing_front[:10]:
    print(x)

print()

print("Beispiele fehlende Rückseite:")
for x in missing_back[:10]:
    print(x)