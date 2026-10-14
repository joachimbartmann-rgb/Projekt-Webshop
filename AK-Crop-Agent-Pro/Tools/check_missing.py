from pathlib import Path
import sqlite3
import pandas as pd

# -------------------------------------
# Dateien
# -------------------------------------

project_root = Path(__file__).parent.parent

excel_file = (
    project_root /
    "Postkarten_Datenbank_Inventar.xlsx"
)

db_file = (
    Path(__file__).parent /
    "collection_v2.db"
)

# -------------------------------------
# Excel
# -------------------------------------

df = pd.read_excel(
    excel_file,
    sheet_name="Postkarten"
)

df = df.dropna(
    axis=1,
    how="all"
)

excel_ids = set()

for value in df["Artikelnummer"]:

    if pd.isna(value):
        continue

    artikelnummer = str(value).strip()

    if artikelnummer:
        excel_ids.add(artikelnummer)

# -------------------------------------
# Datenbank
# -------------------------------------

conn = sqlite3.connect(db_file)

cursor = conn.cursor()

cursor.execute("""
SELECT artikelnummer
FROM products
""")

db_ids = set()

for row in cursor.fetchall():
    db_ids.add(row[0])

conn.close()

# -------------------------------------
# Vergleich
# -------------------------------------

missing = sorted(
    excel_ids - db_ids
)

print()
print("=" * 60)
print("FEHLENDE ARTIKEL")
print("=" * 60)

print()

print(
    f"Excel:    {len(excel_ids)}"
)

print(
    f"Datenbank:{len(db_ids)}"
)

print(
    f"Fehlend:  {len(missing)}"
)

print()

for item in missing:
    print(item)