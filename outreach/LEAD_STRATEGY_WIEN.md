# 🚀 MD DIGITAL — Wiener B2B Lead-Akquise & Outreach System

Dieses System ermöglicht es **Daoud Sahel & Marcel Pasik**, gezielt und mit maximaler Abschlussquote Wiener Klein- und Meisterbetriebe (Barbershops, Tech-Reparaturen, Cafés, Gastronomie, Handwerker) zu kontaktieren und zu zahlenden Kunden für das **399 € Website-Paket (+100 € 4K-Foto-Shooting)** zu machen.

---

## 🖥️ Schnellstart: Lokales Outreach-Dashboard starten

Öffnet einfach das Terminal auf eurem MacBook Air M4 und führt aus:

```bash
cd /Users/daoud/Desktop/MD-Digital-Websites/outreach
python3 server.py
```

Öffnet anschließend im Browser: **[http://localhost:5050](http://localhost:5050)**

### Was das Dashboard kann:
* **Übersicht aller Wiener Leads:** Filtert nach Bezirk (1010, 1070, 1020...) und Branche.
* **1-Click WhatsApp:** Öffnet WhatsApp Web / Desktop mit einer maßgeschneiderten Nachricht, dem passenden Demo-Link und eurer Nummer.
* **1-Click E-Mail:** Öffnet euer Mailprogramm mit fertigem Betreff und individuellem Pitch-Text.
* **Neuen Betrieb hinzufügen:** Wenn ihr auf Google Maps oder beim Spazierengehen einen Laden ohne Website seht, tragt ihn in 10 Sekunden ein.
* **CSV Export:** Alle Kontakte für Excel oder euer Handy sichern.

---

## ⚡ Schnelle Bedienung über das Terminal (CLI)

Wenn ihr schnell über das Terminal arbeiten wollt:

```bash
# 1. Alle Leads auflisten
python3 cli.py list

# 2. Den vorgefertigten Pitch für Lead ID 1 ansehen
python3 cli.py pitch 1

# 3. WhatsApp direkt mit dem Pitch für Lead ID 1 öffnen
python3 cli.py wa 1

# 4. Mailprogramm mit dem Pitch für Lead ID 1 öffnen
python3 cli.py mail 1
```

---

## 🎯 Die 3 stärksten Akquise-Kanäle in Wien (Praxis-Leitfaden)

### Kanal 1: WhatsApp 1-Click Outreach (Höchste Antwortrate: 35–45%)
* **Warum es funktioniert:** Inhaber von Barbershops, Handyläden und Gastronomie stehen tagsüber im Laden und lesen keine E-Mails. WhatsApp-Nachrichten werden im Schnitt innerhalb von 3 Minuten gelesen.
* **Der Ablauf:**
  1. Klickt im Dashboard bei einem Betrieb auf **WhatsApp**.
  2. Die Nachricht ist bereits auf die Branche abgestimmt (z. B. Hinweis auf die *Fade & Blade Barbershop Demo*).
  3. Klickt auf Senden.
  4. Der Inhaber klickt auf seinem Handy den Link, sieht die blitzschnelle Seite und kann euch mit einem Klick zurückrufen oder schreiben.

### Kanal 2: Der "Walk-In" in eurem Bezirk (1010 Innere Stadt & 1070 Neubau)
* **Die unschlagbare Taktik für Studenten:**
  1. Geht mit eurem Smartphone oder MacBook in einen Barbershop oder Handyladen in 1010 oder 1070.
  2. Sagt einfach sympathisch und direkt:
     > *"Servus! Wir sind Daoud und Marcel, zwei Studenten hier aus Wien (Software-Entwicklung & Medienproduktion). Wir haben gesehen, dass ihr noch keine eigene Smartphone-Website habt. Wir haben euch gestern unverbindlich eine Live-Vorschau gebaut – schaut mal kurz auf euer Handy!"*
  3. Zeigt ihnen die Live-Demo ([demo-barber.html](https://d10ud.github.io/md-digital-websites/demo-barber.html) oder [demo-tech.html](https://d10ud.github.io/md-digital-websites/demo-tech.html)).
  4. Wenn der Inhaber begeistert ist: *"Wir machen euch das komplett fertig für 399 € Festpreis, und Marcel kommt mit unserer Sony 4K-Kamera für +100 € direkt zu euch in den Laden für Team-Fotos."*
  5. 8 von 10 Ladenbesitzern sagen bei 399 € sofort Ja, weil Agenturen ihnen sonst 3.000 € bis 5.000 € abknöpfen wollen.

### Kanal 3: Personalisierte E-Mail (für Meisterbetriebe & Handwerker)
* **Ideal für:** Installateure, Elektriker, Tischler und traditionsreiche Restaurants.
* Diese Betriebe prüfen abends ihr Postfach. Nutzt den E-Mail-Button im Dashboard, um die E-Mail mit einem Klick zu öffnen und abzusenden.

---

## 🔍 Wie ihr in 10 Minuten 100 neue Wiener Leads findet

### Methode 1: Google Maps Suche (Kostenlos & extrem treffsicher)
1. Geht auf Google Maps und zoomt auf Wien (z. B. 1. Bezirk, 6./7. Bezirk).
2. Sucht nach:
   * `Barbershop Wien` / `Friseur Wien`
   * `Handy Reparatur Wien` / `Smartphone Reparatur`
   * `Café Wien` / `Bäckerei Wien`
   * `Installateur 1070 Wien` / `Elektriker Wien`
3. Klickt die Einträge durch. Wenn bei einem Eintrag **keine Website** hinterlegt ist oder nur eine Facebook-Seite/Instagram verlinkt ist:
   -> **Sofort ins Dashboard eintragen!** Das ist ein heißer Lead.

### Methode 2: Herold.at & WKO Firmen A-Z
* Auf [herold.at](https://www.herold.at) oder [firmen.wko.at](https://firmen.wko.at) nach Branchen in Wien filtern.
* Viele Einträge haben Telefonnummern und Adressen, aber keine Homepage.

---

## ⚖️ Rechtliche Sicherheit in Österreich (§ 174 TKG & DSGVO)

* **Kein unüberlegter Massen-Spam:** Schickt niemals unpersönliche automatisierte Massenmails an tausende anonyme Adressen. Das verstößt gegen § 174 TKG 2021 und landet im Spamfilter.
* **Der sichere & erfolgreiche Weg:** Kontaktiert Betriebe gezielt 1-zu-1 als studentische Dienstleister mit echtem Mehrwert (ihr habt ihnen bereits eine echte, unverbindliche Live-Vorschau gebaut). Das wird von lokalen Unternehmern geschätzt und führt zu echten Aufträgen.
