# Voice-System – Clean Spec / Problem- & Feature-Definition

## 1. Fehlerbeschreibung: Gemini Timeout

### Status
- Andere Komponenten funktionieren korrekt
- Nur Gemini (Flash) antwortet nicht

### Beobachtung
- Anfrage wird gesendet
- Keine Antwort innerhalb des Timeouts
- System fällt korrekt auf Timeout-Handling zurück

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
  - Klarer Status: „Gemini nicht verfügbar“

---

## 2. Voice-Aufnahme mit Stille-Erkennung (Auto-Stop)

### Ziel
- Keine manuelle Taste zum Beenden der Aufnahme nötig
- Aufnahme endet automatisch bei erkannter Stille

### Anforderungen
- Stille-Erkennung mit konfigurierbarer Dauer (z. B. 1.0–1.5 Sek.)
- Nach Aufnahme **immer** Bestätigungs-Dialog
- Bestätigung **per Stimme**, nicht per Taste

### Flow (Pflicht)
1. Aufnahme startet
2. Nutzer spricht
3. Stille wird erkannt → Aufnahme endet automatisch
4. System erzeugt **verbesserte Version** der Aufnahme
5. System liest diese Version vor:
„Hier ist die verbesserte Version der Aufnahme: <Text>“
6. System fragt anschließend:
„Soll ich die Aufnahme abschicken oder verändern?“

### Gültige Sprach-Befehle
- **„Abschicken“** → Text wird gesendet
- **„Verändern“** → Text bearbeiten (erneute Aufnahme / Edit-Flow)
- **„Nochmal“** → Aufnahme komplett neu
- **„Abbrechen“** → Vorgang wird verworfen

---

## 3. Globales Voice-Feature (Systemweit)

### Ziel
- Voice-Funktion überall im Betriebssystem nutzbar
- Unabhängig von App / Fenster / Kontext

---

### Global Hotkey – neues Verhalten

#### Hotkey-Zuordnung
- **Rechte Strg** → Globales Voice-Feature  
- **Alt Gr** → CLI-Agent-Interaktion  
→ **Hotkeys werden getauscht**

---

### Global-Voice Flow – Variante A (Hold-to-Talk)
1. Rechte **Strg gedrückt halten**
2. Nutzer spricht
3. Hotkey loslassen **oder** Stille-Erkennung greift
4. System:
- Transkribiert
- Verbessert Text
- Liest verbesserte Version vor

---

### Global-Voice Flow – Variante B (Toggle)
1. Rechte **Strg drücken** → Aufnahme startet
2. Nutzer spricht
3. Rechte **Strg erneut drücken** → Aufnahme endet
4. System:
- Transkribiert
- Verbessert Text
- Liest verbesserte Version vor
- Fügt Text automatisch ins **aktive Fenster** ein

---

### Pflichtfunktionen
- Erkennung des aktiven Fensters
- Simuliertes Texteingeben (Paste / Typing)
- Vorlesen **immer vor** dem Einfügen
- Kein automatisches Senden ohne Nutzer-Bestätigung (außer explizit konfiguriert)

---

## Zusammenfassung (Kurz)
- ✅ Gemini-Timeout ist sauber erkannt → Stabilität ok
- 🔧 Aufnahme braucht Stille-Erkennung + Voice-Bestätigung
- 🌍 Globales Voice-Feature mit rechtem Strg
- 🔁 Hotkeys: Rechte Strg ↔ Alt Gr tauschen
- 🔊 System liest **immer** verbesserte Version vor
- ⌨️ Text landet im aktiven Fenster

