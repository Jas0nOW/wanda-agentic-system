# Voice-System – Clean Spec / Problem- & Feature-Definition

## 1. Fehlerbeschreibung: Gemini Timeout

### Status
- Andere Komponenten funktionieren korrekt
- Nur Gemini (Flash) antwortet nicht

### Beobachtung
- Anfrage wird gesendet
- Keine Antwort innerhalb des Timeouts
- System faellt korrekt auf Timeout-Handling zurueck

### Log-Auszug
[Wanda] 🤖 Asking Gemini...
[Gemini] Sending to flash...
[Gemini] Timeout waiting for response

🤖 GEMINI RESPONSE:
⏱️ Timeout - Gemini took too long to respond

### Erwartetes Verhalten
- Timeout sauber erkennen (bereits gegeben)
- Optional:
  - Retry-Mechanismus (konfigurierbar)
  - Fallback auf anderes Modell
  - Klarer Status: „Gemini nicht verfuegbar“

---

## 2. Voice-Aufnahme mit Stille-Erkennung (Auto-Stop)

### Ziel
- Keine manuelle Taste zum Beenden der Aufnahme noetig
- Aufnahme endet automatisch bei erkannter Stille

### Anforderungen
- Stille-Erkennung mit konfigurierbarer Dauer (z. B. 1.0–1.5 Sek.)
- Nach Aufnahme **immer** Bestaetigungs-Dialog
- Bestaetigung **per Stimme**, nicht per Taste

### Flow (Pflicht)
1. Aufnahme startet
2. Nutzer spricht
3. Stille wird erkannt → Aufnahme endet automatisch
4. System erzeugt **verbesserte Version** der Aufnahme
5. System liest diese Version vor:
„Hier ist die verbesserte Version der Aufnahme: <Text>“
6. System fragt anschliessend:
„Soll ich die Aufnahme abschicken oder veraendern?“

### Gueltige Sprach-Befehle
- **„Abschicken“** → Text wird gesendet
- **„Veraendern“** → Text bearbeiten (erneute Aufnahme / Edit-Flow)
- **„Nochmal“** → Aufnahme komplett neu
- **„Abbrechen“** → Vorgang wird verworfen

---

## 3. Globales Voice-Feature (Systemweit)

### Ziel
- Voice-Funktion ueberall im Betriebssystem nutzbar
- Unabhaengig von App / Fenster / Kontext

---

### Global Hotkey – neues Verhalten

#### Hotkey-Zuordnung
- **Rechte Strg** → Globales Voice-Feature
- **Alt Gr** → CLI-Agent-Interaktion
+ **Hotkeys werden getauscht**

---

### Global-Voice Flow – Variante A (Hold-to-Talk)
1. Rechte **Strg gedrueckt halten**
2. Nutzer spricht
3. Hotkey loslassen **oder** Stille-Erkennung greift
4. System:
- Transkribiert
- Verbessert Text
- Liest verbesserte Version vor

---

### Global-Voice Flow – Variante B (Toggle)
1. Rechte **Strg druecken** → Aufnahme startet
2. Nutzer spricht
3. Rechte **Strg erneut druecken** → Aufnahme endet
4. System:
- Transkribiert
- Verbessert Text
- Liest verbesserte Version vor
- Fuegt Text automatisch ins **aktive Fenster** ein

---

### Pflichtfunktionen
- Erkennung des aktiven Fensters
- Simuliertes Texteingeben (Paste / Typing)
- Vorlesen **immer vor** dem Einfuegen
- Kein automatisches Senden ohne Nutzer-Bestaetigung (ausser explizit konfiguriert)

---

## Zusammenfassung (Kurz)
- ✅ Gemini-Timeout ist sauber erkannt → Stabilitaet ok
- 🔧 Aufnahme braucht Stille-Erkennung + Voice-Bestaetigung
- 🌍 Globales Voice-Feature mit rechtem Strg
- 🔁 Hotkeys: Rechte Strg ↔ Alt Gr tauschen
- 🔊 System liest **immer** verbesserte Version vor
- ⌨️ Text landet im aktiven Fenster
