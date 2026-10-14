from pathlib import Path
import csv
import re
import yaml

# --------------------------------------------------
# Konfiguration laden
# --------------------------------------------------

project_root = Path(__file__).parent.parent

with open(
    project_root / "config.yaml",
    encoding="utf-8"
) as f:
    conf = yaml.safe_load(f)

output_dir = Path(
    conf["output_dir"]
)

inventory_file = (
    Path(__file__).parent
    / "cards_inventory.csv"
)

# --------------------------------------------------
# Dateien sammeln
# --------------------------------------------------

files = list(
    output_dir.glob("*.jpg")
)

# --------------------------------------------------
# Kartenstruktur
# --------------------------------------------------

cards = {}

for file in files:

    match = re.match(
        r"temp_(\d+)_([vr])\.jpg",
        file.name,
        re.IGNORECASE
    )

    if not match:
        continue

    number = match.group(1)
    side = match.group(2).lower()

    if number not in cards:

        cards[number] = {
            "v": False,
            "r": False
        }

    cards[number][side] = True

# --------------------------------------------------
# CSV schreiben
# --------------------------------------------------

with open(
    inventory_file,
    "w",
    newline="",
    encoding="utf-8"
) as csvfile:

    writer = csv.writer(
        csvfile,
        delimiter=";"
    )

    writer.writerow([
        "Artikelnummer",
        "Bild_V",
        "Bild_R",
        "Status",
        "Titel",
        "Ort",
        "Region",
        "Land",
        "Verlag",
        "Kategorie",
        "Zustand",
        "Beschreibung",
        "Preis",
        "Shop_Status"
    ])

    for number in sorted(cards.keys()):

        front = cards[number]["v"]
        back = cards[number]["r"]

        if front and back:

            status = "OK"

        elif front:

            status = "FEHLT_RUECKSEITE"

        elif back:

            status = "FEHLT_VORDERSEITE"

        else:

            status = "FEHLT_BEIDES"

        writer.writerow([
            number,
            f"temp_{number}_v.jpg",
            f"temp_{number}_r.jpg",
            status,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "Entwurf"
        ])

# --------------------------------------------------
# Ausgabe
# --------------------------------------------------

print()
print("=" * 60)
print("Inventar-Agent 0.2")
print("=" * 60)

print(
    f"Karten gefunden: {len(cards)}"
)

print(
    f"CSV erzeugt: {inventory_file}"
)

print("=" * 60)