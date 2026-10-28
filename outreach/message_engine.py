#!/usr/bin/env python3
"""
MD DIGITAL — Personalized Outreach Message Engine
Generates tailored, high-converting WhatsApp, Email, and SMS pitches for Vienna businesses.
"""

import urllib.parse
import re

MY_PHONE = "+436765878022"
MY_DISPLAY_PHONE = "+43 676 5878022"
BASE_URL = "https://d10ud.github.io/md-digital-websites"

TEMPLATES = {
    "barber": {
        "subject": "Kurze Frage zu {name} in {district} (Live-Vorschau)",
        "demo_url": f"{BASE_URL}/demo-barber.html",
        "email_body": """Hallo {name}-Team!

Mein Kollege Marcel und ich sind zwei Wiener Studenten (Software-Entwicklung & Medienproduktion) und unterstützen inhabergeführte Betriebe in Wien.

Wir haben gesehen, dass euer Barbershop in {district} bisher entweder keine moderne Website hat oder veraltete Fotos nutzt. 

Damit ihr direkt seht, was möglich ist, haben wir euch unverbindlich eine Live-Vorschau für Friseure & Barbershops gebaut:
👉 {demo_link}

Unser Paket für Wiener Betriebe:
• 399 € Festpreis für eine moderne Website (0.4s Ladezeit, perfekt auf jedem Smartphone)
• +100 € Vor-Ort Foto-Shooting: Marcel kommt mit unserer Sony 4K-Kamera direkt zu euch in den Salon (authentische Team- und Fade-Detailfotos)
• Keine Knebelverträge, 100% eure Rechte

Hättet ihr diese Woche Zeit für ein kurzes 5-Minuten-Gespräch oder einen Kaffee bei euch im Laden?

Beste Grüße aus Wien,
Daoud Sahel & Marcel Pasik
MD DIGITAL Wien
📞 Telefon / WhatsApp: {my_phone}
🌐 https://d10ud.github.io/md-digital-websites/""",
        "whatsapp_body": """Grüß euch {name}! 👋 
Mein Kollege Marcel und ich sind zwei Wiener Studenten (Web & 4K-Foto). Wir haben gesehen, dass ihr in {district} noch keine moderne Smartphone-Website habt.

Wir haben euch unverbindlich eine Live-Demo gebaut, wie euer Barbershop auf dem Handy aussehen könnte:
👉 {demo_link}

Wir bieten das für faire 399 € Festpreis an (+100 € wenn Marcel mit der Sony 4K Kamera direkt zu euch kommt). 

Sollen wir euch kurz unverbindlich anrufen oder hier kurz schreiben?
Viele Grüße, Daoud & Marcel"""
    },

    "tech": {
        "subject": "Mehr Reparatur-Kunden für {name} ({district})",
        "demo_url": f"{BASE_URL}/demo-tech.html",
        "email_body": """Hallo {name}-Team!

Wir sind Daoud & Marcel von MD DIGITAL aus Wien (zwei Studenten für Web-Architektur & Medienproduktion).

Bei vielen Smartphone-Werkstätten in Wien suchen Kunden vor allem zwei Dinge: Den genauen Reparaturpreis und einen schnellen WhatsApp-Kontakt.

Wir haben speziell dafür ein interaktives Konzept mit Live-Reparaturkostenrechner gebaut:
👉 {demo_link}

Unser Angebot für euch in {district}:
• 399 € Festpreis für die komplette Website (blitzschnell, Google Maps optimiert)
• +79 € Google Unternehmensprofil & Maps Eintrag für Top-Platzierung in eurem Bezirk
• +100 € Vor-Ort Werkbank-Fotografie mit Marcel

Passt euch die Tage ein kurzes Telefonat, ob das für euch interessant ist?

Beste Grüße,
Daoud Sahel & Marcel Pasik
MD DIGITAL Wien
📞 {my_phone}
🌐 https://d10ud.github.io/md-digital-websites/""",
        "whatsapp_body": """Servus {name}! 👋
Wir sind Daoud & Marcel (zwei Wiener Studenten für Web & Foto). Wir haben gesehen, dass ihr in {district} Handyreparaturen anbietet.

Wir haben eine fertige Live-Demo mit interaktivem Reparaturrechner gebaut:
👉 {demo_link}

Das ganze gibt es bei uns zum fairen Studenten-Festpreis ab 399 € (inkl. Google Maps Eintrag). Passt euch ein kurzes Telefonat?
Lg Daoud & Marcel ({my_phone})"""
    },

    "gastro": {
        "subject": "Digitale Speisekarte & 4K Fotos für {name} ({district})",
        "demo_url": f"{BASE_URL}/",
        "email_body": """Guten Tag {name}-Team!

Wir sind Daoud & Marcel – zwei ambitionierte Wiener Studenten für Web-Entwicklung und Food-Fotografie.

Wir haben gesehen, dass viele Gäste euer Lokal in {district} online suchen, aber oft nur alte Speisekarten oder schlechte Smartphone-Bilder finden. 

Wir bauen moderne Websites für Wiener Gastronomie mit echtem Sony 4K Foto-Shooting vor Ort:
👉 Live-Einblick: {demo_link}

Was wir für euch tun können:
• 399 € Express Website mit digitaler Speisekarte & QR-Code für Tischaufsteller
• +100 € 4K Foto-Shooting mit Marcel (Gerichte, Atmosphäre, Team)
• Keine monatlichen Kosten – ihr behaltet 100% aller Rechte

Dürfen wir unverbindlich auf einen Sprung bei euch vorbeikommen und euch die Vorschau auf dem Smartphone zeigen?

Herzliche Grüße,
Daoud Sahel & Marcel Pasik
MD DIGITAL Wien
📞 {my_phone}""",
        "whatsapp_body": """Hallo {name}! 👋
Wir sind Daoud & Marcel aus Wien (zwei Studenten für Web & Food-Fotografie). 

Wir bauen moderne Gastronomie-Websites mit 4K-Fotos und QR-Code Speisekarte zum fairen Festpreis von 399 € (+100 € Vor-Ort Shooting).

Schaut euch gerne unsere Live-Arbeit an:
👉 {demo_link}

Wann passt euch ein kurzes Kennenlernen bei euch im Lokal?
Liebe Grüße, Daoud & Marcel"""
    },

    "craft": {
        "subject": "Website & Google Maps Auftritt für {name}",
        "demo_url": f"{BASE_URL}/",
        "email_body": """Sehr geehrte Damen und Herren bei {name},

mein Kollege Marcel und ich sind zwei Wiener Studenten und unterstützen lokale Handwerks- und Meisterbetriebe bei modernen Webauftritten.

Viele Betriebe verlieren wertvolle Neukunden im Bezirk {district}, weil die Website auf Smartphones veraltet wirkt oder bei Google Maps schwer zu finden ist.

Wir bieten einen ehrlichen, studentischen Festpreis:
• 399 € One-Pager Website (0.4s Ladezeit, 24h Notruf/Anfrage-Button, DSGVO & Impressum)
• +99 € Google Maps Local SEO Ranking für euren Bezirk
• +100 € Vor-Ort Team- & Werkstatt-Shooting mit Marcel

Hier können Sie unsere Arbeitsweise und Referenzen testen:
👉 {demo_link}

Wäre ein kurzes 5-Minuten Telefonat für Sie passend?

Mit freundlichen Grüßen,
Daoud Sahel & Marcel Pasik
MD DIGITAL Wien
📞 {my_phone}""",
        "whatsapp_body": """Guten Tag {name}! 👋
Wir sind Daoud & Marcel von MD DIGITAL aus Wien. Wir unterstützen Handwerksbetriebe mit schnellen, modernen Websites & Google Maps Einträgen ab 399 € Festpreis.

Hier ist unsere Live-Website:
👉 {demo_link}

Hätten Sie die Tage kurz Zeit für ein unverbindliches Gespräch?
Beste Grüße, Daoud & Marcel ({my_phone})"""
    },

    "general": {
        "subject": "Moderne Website für {name} in {district} (ab 399 €)",
        "demo_url": f"{BASE_URL}/",
        "email_body": """Hallo {name}-Team!

Wir sind Daoud & Marcel &mdash; zwei Studenten aus Wien für Web-Architektur und 4K-Medienproduktion.

Statt teurer Agentur-Angebote über mehrere tausend Euro bauen wir inhabergeführten Wiener Betrieben kompromisslos schnelle Websites zu fairen Studenten-Konditionen:
• 399 € Festpreis für eine moderne Website (Apple-Standard, mobiloptimiert)
• +100 € Vor-Ort Foto-Shooting mit Marcel (Sony 4K-Setup)
• 100% Eigentum an Code & Fotos, keine Monatsverträge

Hier können Sie unsere Live-Showcases und Hardware testen:
👉 {demo_link}

Wann passt Ihnen ein kurzes, unverbindliches Kennenlernen?

Beste Grüße,
Daoud Sahel & Marcel Pasik
MD DIGITAL Wien
📞 {my_phone}""",
        "whatsapp_body": """Servus {name}! 👋
Wir sind Daoud & Marcel von MD DIGITAL aus Wien (zwei Studenten für Web & 4K-Foto). Wir bauen moderne Websites für Wiener Betriebe ab fairen 399 € Festpreis.

Schau dir gerne unsere Live-Seite auf dem Smartphone an:
👉 {demo_link}

Dürfen wir uns kurz telefonisch melden?
Lg Daoud & Marcel ({my_phone})"""
    }
}

def clean_phone_number(raw_phone):
    """Clean phone number into international format for WhatsApp and tel:"""
    if not raw_phone:
        return ""
    clean = re.sub(r"[^\d+]", "", raw_phone)
    if clean.startswith("0"):
        clean = "+43" + clean[1:]
    elif clean.startswith("43"):
        clean = "+" + clean
    return clean

def generate_pitch(lead):
    """Generates email, whatsapp, and sms texts along with clickable action links."""
    branch = lead.get("branch", "general").lower()
    tmpl = TEMPLATES.get(branch, TEMPLATES["general"])
    
    lead_id = lead.get("id", "0")
    name = lead.get("name", "Geschäft")
    district = lead.get("district", "Wien")
    raw_phone = lead.get("phone", "")
    email = lead.get("email", "")
    
    clean_phone = clean_phone_number(raw_phone)
    whatsapp_clean = clean_phone.replace("+", "") if clean_phone else ""

    demo_link = f"{tmpl['demo_url']}?ref=lead-{lead_id}"
    
    # Fill templates
    subject = tmpl["subject"].format(name=name, district=district)
    email_body = tmpl["email_body"].format(
        name=name,
        district=district,
        demo_link=demo_link,
        my_phone=MY_DISPLAY_PHONE
    )
    whatsapp_body = tmpl["whatsapp_body"].format(
        name=name,
        district=district,
        demo_link=demo_link,
        my_phone=MY_DISPLAY_PHONE
    )

    # Clickable URLs
    mailto_url = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(email_body)}" if email else ""
    whatsapp_url = f"https://wa.me/{whatsapp_clean}?text={urllib.parse.quote(whatsapp_body)}" if whatsapp_clean else ""
    sms_url = f"sms:{clean_phone}&body={urllib.parse.quote(whatsapp_body)}" if clean_phone else ""
    call_url = f"tel:{clean_phone}" if clean_phone else ""

    return {
        "lead_id": lead_id,
        "name": name,
        "branch": branch,
        "district": district,
        "subject": subject,
        "email": email,
        "phone": clean_phone,
        "email_body": email_body,
        "whatsapp_body": whatsapp_body,
        "demo_link": demo_link,
        "mailto_url": mailto_url,
        "whatsapp_url": whatsapp_url,
        "sms_url": sms_url,
        "call_url": call_url
    }

if __name__ == "__main__":
    sample_lead = {
        "id": 1,
        "name": "Barbier am Graben",
        "branch": "barber",
        "district": "1010 Wien",
        "phone": "+43 676 123 45 67",
        "email": "kontakt@barbier-graben.at"
    }
    pitch = generate_pitch(sample_lead)
    print("Subject:", pitch["subject"])
    print("\nWhatsApp Preview:\n", pitch["whatsapp_body"])
    print("\nWhatsApp Link:", pitch["whatsapp_url"])
