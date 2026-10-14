from pathlib import Path
from core.detector import detect_cards
import cv2
import yaml
import re
import sys
import shutil
import csv

# --------------------------------------------------
# Konfiguration
# --------------------------------------------------

with open(
    "config.yaml",
    encoding="utf-8"
) as f:
    conf = yaml.safe_load(f)

imp = Path(conf["import_dir"])
out = Path(conf["output_dir"])
archive = Path(conf["archive_dir"])

out.mkdir(exist_ok=True)
archive.mkdir(exist_ok=True)

report_file = out / "crop_report.csv"
report_rows = []

# --------------------------------------------------
# Nummer aus Dateinamen holen
# --------------------------------------------------

def extract_number(filename):

    numbers = re.findall(
        r"\d+",
        filename
    )

    if numbers:
        return int(numbers[-1])

    return -1


# --------------------------------------------------
# Dateien laden
# --------------------------------------------------

files = (
    list(imp.glob("*.jpg"))
    + list(imp.glob("*.png"))
)

files.sort(
    key=lambda f: extract_number(f.name)
)

print()
print("=" * 70)
print("AK Crop Agent gestartet")
print("=" * 70)
print(f"Gefundene Dateien: {len(files)}")

# --------------------------------------------------
# Grundprüfung
# --------------------------------------------------

if len(files) == 0:
    raise RuntimeError(
        "Keine Dateien im Importordner gefunden."
    )

if len(files) % 2 != 0:
    raise RuntimeError(
        "Ungerade Anzahl Dateien gefunden."
    )

# --------------------------------------------------
# Kartenzähler
# --------------------------------------------------

card_counter = 1

# --------------------------------------------------
# Verarbeitung
# --------------------------------------------------

for i in range(0, len(files), 2):

    front_file = files[i]
    back_file = files[i + 1]

    print()
    print("-" * 70)
    print(f"Vorderseite : {front_file.name}")
    print(f"Rückseite   : {back_file.name}")

    front_img = cv2.imread(
        str(front_file)
    )

    back_img = cv2.imread(
        str(back_file)
    )

    if front_img is None:
        raise RuntimeError(
            f"Datei konnte nicht geladen werden: {front_file.name}"
        )

    if back_img is None:
        raise RuntimeError(
            f"Datei konnte nicht geladen werden: {back_file.name}"
        )

    front_cards = detect_cards(
        front_img,
        conf["min_area"]
    )

    back_cards = detect_cards(
        back_img,
        conf["min_area"]
    )

    front_count = len(front_cards)
    back_count = len(back_cards)

    print(
        f"Erkannte Vorderseiten : {front_count}"
    )

    print(
        f"Erkannte Rückseiten   : {back_count}"
    )

    # --------------------------------------------------
    # Sicherheitsprüfung
    # --------------------------------------------------

    if front_count != back_count:

        print()
        print("=" * 70)
        print("FEHLER")
        print(
            "Vorderseiten und Rückseiten stimmen nicht überein."
        )

        print(
            f"{front_file.name} -> {front_count}"
        )

        print(
            f"{back_file.name} -> {back_count}"
        )

        report_rows.append([
            front_file.name,
            back_file.name,
            front_count,
            back_count,
            "FEHLER"
        ])

        with open(
            report_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(
                csvfile,
                delimiter=";"
            )

            writer.writerow([
                "Frontdatei",
                "Rueckdatei",
                "Vorderseiten",
                "Rueckseiten",
                "Status"
            ])

            writer.writerows(
                report_rows
            )

        print()
        print(
            f"Crop-Report gespeichert: {report_file}"
        )

        print("=" * 70)

        sys.exit(1)

    # --------------------------------------------------
    # Speichern
    # --------------------------------------------------

    for card_index in range(front_count):

        front_card = front_cards[card_index]
        back_card = back_cards[card_index]

        if front_card is None:
            raise RuntimeError(
                f"Leere Vorderseite bei Karte {card_index + 1}"
            )

        if back_card is None:
            raise RuntimeError(
                f"Leere Rückseite bei Karte {card_index + 1}"
            )

        number = f"{card_counter:04d}"

        front_name = (
            f"temp_{number}_v.jpg"
        )

        back_name = (
            f"temp_{number}_r.jpg"
        )

        cv2.imwrite(
            str(out / front_name),
            front_card
        )

        cv2.imwrite(
            str(out / back_name),
            back_card
        )

        print(
            f"Gespeichert: temp_{number}"
        )

        card_counter += 1

    # --------------------------------------------------
    # Report aktualisieren
    # --------------------------------------------------

    report_rows.append([
        front_file.name,
        back_file.name,
        front_count,
        back_count,
        "OK"
    ])

    # --------------------------------------------------
    # Archivierung
    # --------------------------------------------------

    shutil.move(
        str(front_file),
        str(
            archive / front_file.name
        )
    )

    shutil.move(
        str(back_file),
        str(
            archive / back_file.name
        )
    )

    print(
        f"Archiviert: {front_file.name}"
    )

    print(
        f"Archiviert: {back_file.name}"
    )

# --------------------------------------------------
# Crop-Report speichern
# --------------------------------------------------

with open(
    report_file,
    "w",
    newline="",
    encoding="utf-8"
) as csvfile:

    writer = csv.writer(
        csvfile,
        delimiter=";"
    )

    writer.writerow([
        "Frontdatei",
        "Rueckdatei",
        "Vorderseiten",
        "Rueckseiten",
        "Status"
    ])

    writer.writerows(
        report_rows
    )

# --------------------------------------------------
# Abschluss
# --------------------------------------------------

print()
print("=" * 70)
print("Crop-Agent erfolgreich beendet")
print(
    f"Gesamtzahl Karten: {card_counter - 1}"
)
print(
    f"Crop-Report: {report_file}"
)
print("=" * 70)