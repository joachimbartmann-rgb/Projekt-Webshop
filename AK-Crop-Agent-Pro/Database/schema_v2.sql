-- =====================================================
-- COLLECTION SHOP DATABASE V2.1
-- =====================================================

-- =====================================================
-- PRODUKTE
-- =====================================================

CREATE TABLE products (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    artikelnummer TEXT UNIQUE NOT NULL,

    produkttyp TEXT NOT NULL,

    titel TEXT NOT NULL,

    beschreibung TEXT,

    land TEXT,
    region TEXT,
    ort TEXT,

    jahr INTEGER,

    preis REAL,

    status TEXT DEFAULT 'Im Bestand',

    erstellt_am DATETIME,
    aktualisiert_am DATETIME

);

-- =====================================================
-- KATEGORIEN
-- =====================================================

CREATE TABLE categories (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    parent_id INTEGER

);

-- =====================================================
-- PRODUKT-KATEGORIEN
-- =====================================================

CREATE TABLE product_categories (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    artikelnummer TEXT NOT NULL,

    category_id INTEGER NOT NULL

);

-- =====================================================
-- ORTE
-- =====================================================

CREATE TABLE locations (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    land TEXT,

    region TEXT,

    ort TEXT

);

-- =====================================================
-- BILDER
-- =====================================================

CREATE TABLE images (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    artikelnummer TEXT NOT NULL,

    bildtyp TEXT NOT NULL,

    dateiname TEXT NOT NULL,

    dateipfad TEXT,

    breite INTEGER,

    hoehe INTEGER,

    sortierung INTEGER DEFAULT 0,

    erstellt_am DATETIME

);

-- =====================================================
-- POSTKARTEN
-- =====================================================

CREATE TABLE postcards (

    artikelnummer TEXT PRIMARY KEY,

    verlag TEXT,

    kategorie_motiv TEXT,

    erhaltungszustand TEXT,

    zustand_details TEXT,

    gelaufen TEXT,

    baujahr_postamt TEXT,

    stempel_info TEXT,

    empfaenger_absender TEXT,

    wert_min REAL,

    wert_max REAL,

    besondere_merkmale TEXT,

    bekannte_maengel TEXT

);

-- =====================================================
-- BÜCHER
-- =====================================================

CREATE TABLE books (

    artikelnummer TEXT PRIMARY KEY,

    autor TEXT,

    verlag TEXT,

    isbn TEXT,

    zustand TEXT,

    besondere_merkmale TEXT,

    bekannte_maengel TEXT

);

-- =====================================================
-- MÜNZEN
-- =====================================================

CREATE TABLE coins (

    artikelnummer TEXT PRIMARY KEY,

    material TEXT,

    praegung TEXT,

    jahr TEXT,

    erhaltung TEXT,

    wert_min REAL,

    wert_max REAL

);

-- =====================================================
-- GENERISCHE ATTRIBUTE
-- =====================================================

CREATE TABLE product_attributes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    artikelnummer TEXT NOT NULL,

    attribut_name TEXT NOT NULL,

    attribut_wert TEXT

);

-- =====================================================
-- KUNDEN
-- =====================================================

CREATE TABLE customers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT UNIQUE NOT NULL,

    passwort_hash TEXT,

    vorname TEXT,

    nachname TEXT,

    telefon TEXT,

    erstellt_am DATETIME,

    letzter_login DATETIME

);

-- =====================================================
-- MERKLISTE
-- =====================================================

CREATE TABLE wishlist (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER NOT NULL,

    artikelnummer TEXT NOT NULL,

    erstellt_am DATETIME

);

-- =====================================================
-- =====================================================
-- WARENKORB
-- =====================================================

CREATE TABLE carts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER,

    erstellt_am DATETIME

);

CREATE TABLE cart_items (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cart_id INTEGER NOT NULL,

    artikelnummer TEXT NOT NULL,

    menge INTEGER DEFAULT 1

);

-- =====================================================
-- BESTELLUNGEN
-- =====================================================

CREATE TABLE orders (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER NOT NULL,

    bestellnummer TEXT UNIQUE,

    status TEXT,

    gesamtbetrag REAL,

    bezahlt INTEGER DEFAULT 0,

    bestellt_am DATETIME

);

CREATE TABLE order_items (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    order_id INTEGER NOT NULL,

    artikelnummer TEXT NOT NULL,

    einzelpreis REAL,

    menge INTEGER

);

-- =====================================================
-- SÜTTERLIN
-- =====================================================

CREATE TABLE transcriptions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    artikelnummer TEXT NOT NULL,

    transkript TEXT,

    erstellt_am DATETIME

);

-- =====================================================
-- MEHRSPRACHIGKEIT
-- =====================================================

CREATE TABLE product_translations (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    artikelnummer TEXT NOT NULL,

    sprache TEXT NOT NULL,

    titel TEXT,

    beschreibung TEXT

);
