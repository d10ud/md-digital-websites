#!/usr/bin/env python3
"""
MD DIGITAL — Terminal Outreach CLI
Quick command-line tool for managing Vienna leads and triggering 1-click pitches.
"""

import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_manager import init_db, get_all_leads, get_lead_by_id, add_lead, update_lead_status
from message_engine import generate_pitch

def print_help():
    print("""
🏛️ MD DIGITAL — Vienna Outreach CLI
-----------------------------------
python3 cli.py list                : Alle Wiener Leads anzeigen
python3 cli.py pitch <ID>          : Pitch für einen Betrieb anzeigen
python3 cli.py wa <ID>             : WhatsApp mit vorgefertigtem Pitch öffnen
python3 cli.py mail <ID>           : Mailprogramm mit vorgefertigtem Text öffnen
python3 cli.py start               : Web-Dashboard auf http://localhost:5050 starten
""")

def cmd_list():
    leads = get_all_leads()
    print(f"\n📍 Aktuelle Leads in Wien ({len(leads)} Betriebe):\n")
    print(f"{'ID':<4} | {'Name':<30} | {'Bezirk':<12} | {'Branche':<10} | {'Status':<12} | {'Telefon'}")
    print("-" * 90)
    for l in leads:
        print(f"{l['id']:<4} | {l['name'][:28]:<30} | {l['district'][:10]:<12} | {l['branch']:<10} | {l['status']:<12} | {l['phone'] or 'Keine'}")
    print("\nTipp: Führe 'python3 cli.py pitch <ID>' aus, um die Nachricht zu sehen.\n")

def cmd_pitch(lead_id):
    lead = get_lead_by_id(int(lead_id))
    if not lead:
        print(f"❌ Lead mit ID {lead_id} nicht gefunden.")
        return
    p = generate_pitch(lead)
    print("\n" + "=" * 60)
    print(f"🎯 PITCH FÜR: {p['name']} ({p['branch'].upper()} · {p['district']})")
    print("=" * 60)
    print("\n📱 WHATSAPP PITCH:")
    print("-" * 60)
    print(p["whatsapp_body"])
    print("\n✉️ E-MAIL PITCH:")
    print("-" * 60)
    print("Betreff:", p["subject"])
    print("\n" + p["email_body"])
    print("\n🔗 Demo-Link:", p["demo_link"])
    print("=" * 60 + "\n")

def cmd_wa(lead_id):
    lead = get_lead_by_id(int(lead_id))
    if not lead:
        print("❌ Lead nicht gefunden.")
        return
    p = generate_pitch(lead)
    if not p["whatsapp_url"]:
        print("❌ Keine Telefonnummer für diesen Lead hinterlegt.")
        return
    update_lead_status(lead["id"], "kontaktiert")
    print(f"🚀 Öffne WhatsApp für {lead['name']}...")
    subprocess.run(["open", p["whatsapp_url"]])

def cmd_mail(lead_id):
    lead = get_lead_by_id(int(lead_id))
    if not lead:
        print("❌ Lead nicht gefunden.")
        return
    p = generate_pitch(lead)
    if not p["mailto_url"]:
        print("❌ Keine E-Mail für diesen Lead hinterlegt.")
        return
    update_lead_status(lead["id"], "kontaktiert")
    print(f"✉️ Öffne Mailprogramm für {lead['name']}...")
    subprocess.run(["open", p["mailto_url"]])

if __name__ == "__main__":
    init_db()
    args = sys.argv[1:]
    if not args or args[0] == "help":
        print_help()
    elif args[0] == "list":
        cmd_list()
    elif args[0] == "pitch" and len(args) > 1:
        cmd_pitch(args[1])
    elif args[0] == "wa" and len(args) > 1:
        cmd_wa(args[1])
    elif args[0] == "mail" and len(args) > 1:
        cmd_mail(args[1])
    elif args[0] == "start":
        os.system("python3 " + os.path.join(os.path.dirname(__file__), "server.py"))
    else:
        print_help()
