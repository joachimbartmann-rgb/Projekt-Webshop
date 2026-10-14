from flask import Flask, render_template, send_file
import sqlite3
from pathlib import Path

app = Flask(__name__)

DB_FILE = (
    Path(__file__).parent.parent /
    "Database" /
    "collection_v2.db"
)


@app.route("/")
def index():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT artikelnummer,
               titel
        FROM products
        LIMIT 4
    """)

    products = cursor.fetchall()

    conn.close()

    return render_template(
        "index_neu.html",
        products=products
    )


@app.route("/test")
def test():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT artikelnummer,
               titel
        FROM products
        LIMIT 20
    """)

    products = cursor.fetchall()

    conn.close()

    return render_template(
        "test.html",
        products=products
    )


@app.route("/katalog")
def katalog():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT artikelnummer,
               titel
        FROM products
        ORDER BY artikelnummer
    """)

    products = cursor.fetchall()

    conn.close()

    return render_template(
        "katalog.html",
        products=products
    )

@app.route("/warenkorb")
def warenkorb():
    return render_template("warenkorb.html")
@app.route("/bild/<artikelnummer>")

def bild(artikelnummer):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT dateipfad
        FROM images
        WHERE artikelnummer = ?
        AND bildtyp = 'front'
        LIMIT 1
    """, (artikelnummer,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return send_file(row[0])

    return "Bild nicht gefunden", 404


@app.route("/bild_rueckseite/<artikelnummer>")
def bild_rueckseite(artikelnummer):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT dateipfad
        FROM images
        WHERE artikelnummer = ?
        AND bildtyp = 'back'
        LIMIT 1
    """, (artikelnummer,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return send_file(row[0])

    return "Rückseite nicht gefunden", 404


@app.route("/produkt/<artikelnummer>")
def produkt(artikelnummer):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM products
        WHERE artikelnummer = ?
    """, (artikelnummer,))

    product = cursor.fetchone()

    cursor.execute("""
        SELECT *
        FROM postcards
        WHERE artikelnummer = ?
    """, (artikelnummer,))

    postcard = cursor.fetchone()

    conn.close()

    if not product:
        return "Produkt nicht gefunden", 404

    return render_template(
        "produkt.html",
        product=product,
        postcard=postcard
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )