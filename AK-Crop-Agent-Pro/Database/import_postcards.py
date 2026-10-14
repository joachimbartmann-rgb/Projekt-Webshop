from pathlib import Path
import sqlite3
import pandas as pd

# --------------------------------------------------
# Pfade
# --------------------------------------------------

project_root = Path(__file__).parent.parent

excel_file = (
    project_root /
    "Postkarten_Datenbank_Inventar.xlsx"
)

database_file = (
    Path(__file__).parent /
    "collection_v2.db"
)

# --------------------------------------------------
# Excel laden
# --------------------------------------------------

df = pd.read_excel(
    excel_file,
    sheet_name="Postkarten"
)

df = df.dropna(
    axis=1,
    how="all"
)

# --------------------------------------------------
# Datenbank
# --------------------------------------------------

conn = sqlite3.connect(database_file)

cursor = conn.cursor()

count = 0

for _, row in df.iterrows():

    artikelnummer = str(
        row.get("Artikelnummer", "")
    ).strip()

    if not artikelnummer:
        continue

    titel = str(
        row.get("Titel", "")
    )

    preis = row.get(
        "Verkaufspreis (€)",
        None
    )

    status = str(
        row.get("Status", "Im Bestand")
    )

    # --------------------------------------------------
    # products
    # --------------------------------------------------

    cursor.execute("""
        INSERT OR REPLACE INTO products
        (
            artikelnummer,
            produkttyp,
            titel,
            preis,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        artikelnummer,
        "Postkarte",
        titel,
        preis,
        status
    ))

    # --------------------------------------------------
    # postcards
    # --------------------------------------------------

    cursor.execute("""
        INSERT OR REPLACE INTO postcards
        (
            artikelnummer,
            verlag,
            kategorie_motiv,
            erhaltungszustand,
            zustand_details,
            gelaufen,
            baujahr_postamt,
            stempel_info,
            empfaenger_absender,
            wert_min,
            wert_max,
            besondere_merkmale,
            bekannte_maengel
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        artikelnummer,
        row.get("Verlag"),
        row.get("Kategorie / Motiv"),
        row.get("Erhaltungszustand"),
        row.get("Zustand Details"),
        row.get("Gelaufen (J/N)"),
        row.get("Baujahr / Postamt"),
        row.get("Stempel Info"),
        row.get("Empfänger / Absender"),
        row.get("Wert Min (€)"),
        row.get("Wert Max (€)"),
        row.get("Besondere Merkmale"),
        row.get("Bekannte Mängel")
    ))

    count += 1

conn.commit()

print()
print("=" * 60)
print(f"{count} Postkarten importiert")
print("=" * 60)

conn.close()