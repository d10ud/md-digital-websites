#!/usr/bin/env python3
"""
MD DIGITAL — Vienna Lead Manager Engine
SQLite-backed pipeline for local business outreach in Vienna.
"""

import sqlite3
import os
import csv
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        branch TEXT NOT NULL,
        district TEXT,
        address TEXT,
        phone TEXT,
        email TEXT,
        website TEXT,
        has_website INTEGER DEFAULT 0,
        status TEXT DEFAULT 'neu',
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

    # Check if empty, then populate with starter curated Vienna leads
    cursor.execute("SELECT COUNT(*) as cnt FROM leads")
    row = cursor.fetchone()
    if row["cnt"] == 0:
        seed_starter_leads(conn)
    conn.close()

def seed_starter_leads(conn):
    starter = [
        # 1010 Innere Stadt - Barbers & Salons
        ("Barbier am Graben", "barber", "1010 Wien", "Graben 14, 1010 Wien", "+43 1 512 34 56", "info@barbier-graben.at", "", 0, "Top Lage, hat bisher nur veralteten Instagram Link, keine eigene Seite. Perfekt für Fade & Blade Demo!"),
        ("Gentlemen Cut Stephansplatz", "barber", "1010 Wien", "Rotenturmstraße 8, 1010 Wien", "+43 676 111 22 33", "kontakt@gentlemen-cut.at", "", 0, "Hohe Frequenz, Marcel kann Vor-Ort 4K Fotos schießen. 399 € One-Pager ideal."),
        ("Kaiser Barbershop 1010", "barber", "1010 Wien", "Wollzeile 22, 1010 Wien", "+43 1 513 88 99", "kaiserbarber.wien@gmail.com", "http://alt.kaiserbarber.at", 1, "Bestehende Website ist nicht mobilfähig, lädt über 4 Sekunden. Re-Design anbieten!"),
        
        # 1070 Neubau - Smartphone Repair & Tech Stores
        ("iFix Neubau Phone Repair", "tech", "1070 Wien", "Neubaugasse 31, 1070 Wien", "+43 664 222 33 44", "office@ifix-neubau.at", "", 0, "Starke Konkurrenz auf der Mariahilfer Straße, braucht Google Maps SEO (+99 €) & Rechner."),
        ("HandyLab 1070 Wien", "tech", "1070 Wien", "Zieglergasse 15, 1070 Wien", "+43 1 526 99 00", "support@handylab-wien.at", "", 0, "Sehr gute Reparaturwerkbank, perfekt für die PhoneLab Express Demo!"),
        ("SmartFix Westbahnhof", "tech", "1070 Wien", "Mariahilfer Straße 124, 1070 Wien", "+43 676 333 44 55", "info@smartfix-wien.at", "", 0, "Hohe Passantenfrequenz, braucht WhatsApp Sofort-Angebot Button."),

        # 1020 & 1030 Wien - Cafés & Gastronomie
        ("Café Leopold Specialty Coffee", "gastro", "1020 Wien", "Taborstraße 19, 1020 Wien", "+43 1 214 55 66", "hallo@cafe-leopold.at", "", 0, "Hipster Café, Marcel 4K Kaffee-Makroaufnahmen + QR-Code Speisekarte anbieten."),
        ("Rösterei Donaukanal", "gastro", "1020 Wien", "Praterstraße 42, 1020 Wien", "+43 699 444 55 66", "coffee@roesterei-donaukanal.at", "", 0, "Braucht Google Unternehmensprofil & zweisprachige Website (DE/EN)."),
        ("Trattoria Bella Vienna", "gastro", "1030 Wien", "Landstraßer Hauptstraße 55, 1030 Wien", "+43 1 713 22 11", "bella.vienna.1030@gmail.com", "", 0, "Traditions-Lokal, keine Website. Potenzial für 399 € One-Pager + 100 € Fotos."),

        # Handwerk & Meisterbetriebe Wien
        ("Schlüsseldienst & Sicherheit 1010", "craft", "1010 Wien", "Tuchlauben 11, 1010 Wien", "+43 676 555 66 77", "notdienst@aufsperr-wien.at", "", 0, "Dringend 24h Notruf-Button auf Smartphone & Google Maps Local SEO nötig!"),
        ("Installateur Meisterbetrieb Pasch", "craft", "1070 Wien", "Burggasse 45, 1070 Wien", "+43 1 523 44 55", "office@pasch-installationen.at", "", 0, "Solider Betrieb, alte Flash-Website von 2012. 399 € Express Relaunch."),
        ("Elektro Express Wien", "craft", "1080 Wien", "Josefstädter Straße 34, 1080 Wien", "+43 676 777 88 99", "service@elektro-express-wien.at", "", 0, "Braucht Trust-Badges & schnelles Kontaktformular.")
    ]
    cursor = conn.cursor()
    for item in starter:
        cursor.execute("""
        INSERT INTO leads (name, branch, district, address, phone, email, website, has_website, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, item)
    conn.commit()

def get_all_leads(branch=None, district=None, status=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM leads WHERE 1=1"
    params = []
    if branch:
        query += " AND branch = ?"
        params.append(branch)
    if district:
        query += " AND district LIKE ?"
        params.append(f"%{district}%")
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return leads

def get_lead_by_id(lead_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_lead(name, branch, district="", address="", phone="", email="", website="", has_website=0, notes=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO leads (name, branch, district, address, phone, email, website, has_website, notes, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    """, (name, branch, district, address, phone, email, website, has_website, notes))
    lead_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return lead_id

def update_lead_status(lead_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE leads SET status = ?, updated_at = datetime('now') WHERE id = ?
    """, (new_status, lead_id))
    conn.commit()
    conn.close()

def import_from_csv(file_path):
    conn = get_connection()
    cursor = conn.cursor()
    count = 0
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name") or row.get("Name") or row.get("title")
            if not name:
                continue
            branch = row.get("branch") or row.get("Kategorie") or "general"
            district = row.get("district") or row.get("Bezirk") or "Wien"
            address = row.get("address") or row.get("Adresse") or ""
            phone = row.get("phone") or row.get("Telefon") or ""
            email = row.get("email") or row.get("Email") or ""
            website = row.get("website") or row.get("Web") or ""
            has_website = 1 if website and len(website) > 4 else 0
            notes = row.get("notes") or row.get("Notiz") or ""
            
            cursor.execute("""
            INSERT INTO leads (name, branch, district, address, phone, email, website, has_website, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (name, branch.lower(), district, address, phone, email, website, has_website, notes))
            count += 1
    conn.commit()
    conn.close()
    return count

def export_to_csv(output_path):
    leads = get_all_leads()
    if not leads:
        return 0
    keys = list(leads[0].keys())
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(leads)
    return len(leads)

if __name__ == "__main__":
    init_db()
    leads = get_all_leads()
    print(f"Lead Manager initialisiert. Aktuell {len(leads)} Leads in der Datenbank.")
