# OpenCode + OhMyOpenCode Diagnose - Vollständige Dokumentation

**Datum**: 2026-01-31
**Status**: 🔍 Diagnose in Progress
**Problem**: OpenCode hängt beim Start mit oh-my-opencode Plugin

---

## Problemhistorie

### Ursprüngliches Problem
- OpenCode startet **nicht**, wenn das OhMyOpenCode Plugin aktiv ist
- Sobald das Plugin aus der opencode.json entfernt wird, startet OpenCode normal
- Problem besteht seit Installation auf neuem PC/OS (funktionierte früher auf anderem System)

### Erste Diagnose (FEHLERHAFT)
**Annahme**: Falsche Modellnamen in oh-my-opencode.json
**Durchgeführte Änderungen**:
- Modellnamen korrigiert (z.B. `google/gemini-3-flash` → `google/antigravity-gemini-3-flash`)
- `"google_auth": false` hinzugefügt
- Multi-Provider-Strategie implementiert

**Ergebnis**: ❌ Problem nicht gelöst - OpenCode hängt weiterhin

### Zweite Diagnose (KORREKT)
**Log-Analyse** (`/home/jannis/.local/share/opencode/log/2026-01-31T182920.log`):
```
INFO  2026-01-31T18:29:20 +55ms service=plugin path=file:///home/jannis/.config/opencode/node_modules/oh-my-opencode/dist/index.js loading plugin
INFO  2026-01-31T18:29:20 +475ms service=plugin path=opencode-anthropic-auth@0.0.13 loading plugin
INFO  2026-01-31T18:29:20 +2ms service=plugin path=@gitlab/opencode-gitlab-auth@1.3.2 loading plugin
INFO  2026-01-31T18:29:20 +43ms service=server method=GET path=/provider request
INFO  2026-01-31T18:29:20 +0ms service=server status=started method=GET path=/provider request
[LOG ENDET HIER - OpenCode hängt]
```

**Erkenntnisse**:
- oh-my-opencode Plugin wird erfolgreich geladen
- Weitere Auth-Plugins werden geladen (anthropic-auth, gitlab-auth)
- OpenCode hängt bei `/provider` Anfrage
- Problem ist **NICHT** die oh-my-opencode.json Konfiguration
- Problem ist das oh-my-opencode Plugin selbst oder ein Plugin-Konflikt

---

## Systemkonfiguration

### Versionen
- **OpenCode**: 1.1.47
- **oh-my-opencode**: 3.1.9
- **opencode-antigravity-auth**: 1.4.3
- **OS**: Linux 6.17.9-76061709-generic
- **Package Manager**: Bun 1.3.8

### Installierte Plugins (aus opencode.json)
```json
"plugin": [
  "opencode-antigravity-auth@latest",
  "oh-my-opencode@3.1.9"
]
```

### Weitere geladene Plugins (aus Log)
- opencode-anthropic-auth@0.0.13
- @gitlab/opencode-gitlab-auth@1.3.2
- @cgasgarth/opencode-for-rust@1.1.18
- opencode-gemini-auth@1.3.8
- opencode-knowledge@0.6.0
- opencode-scheduler@1.1.0
- opencode-supermemory@0.1.8
- micode@0.9.1
- opencode-antigravity-quota@0.1.6

### Verfügbare Provider (OAuth konfiguriert)
1. **Anthropic** (Claude API)
2. **OpenAI** (GPT-5.2, Codex)
3. **GitHub Copilot**
4. **Google CLI/Gemini**
5. **Antigravity** (Google IDE)

---

## Hypothesen

### 1. Plugin-Initialisierungs-Deadlock ⚠️
- oh-my-opencode oder Auth-Plugin wartet auf Netzwerkantwort
- Plugin-Hook hängt in Endlosschleife
- Race Condition zwischen Plugins

### 2. Provider-Validierungs-Problem 🔍
- OpenCode versucht alle Provider zu validieren
- Einer antwortet nicht → Timeout
- Authentifizierungs-Probleme

### 3. Modell-Verfügbarkeits-Check 🔍
- oh-my-opencode validiert konfigurierte Modelle beim Start
- Hängt bei nicht verfügbarem Modell
- Netzwerk-Timeout

### 4. Auth-Plugin Konflikt 🔥 (WAHRSCHEINLICHSTE URSACHE)
- Mehrere Auth-Plugins gleichzeitig geladen
- Konflikte zwischen:
  - opencode-antigravity-auth
  - opencode-anthropic-auth
  - opencode-gemini-auth
  - @gitlab/opencode-gitlab-auth
- Race Condition oder Deadlock

---

## Geplante Diagnoseschritte

### Schritt 1: Minimale Plugin-Konfiguration ⏳
**Ziel**: Isoliere das problematische Plugin

**Test A - Nur oh-my-opencode**:
```json
{
  "plugin": ["oh-my-opencode@3.1.9"]
}
```
+ Minimale oh-my-opencode.json (kein google_auth, keine Agents)

**Test B - Nur antigravity-auth**:
```json
{
  "plugin": ["opencode-antigravity-auth@latest"]
}
```

**Test C - Beide in umgekehrter Reihenfolge**:
```json
{
  "plugin": [
    "oh-my-opencode@3.1.9",
    "opencode-antigravity-auth@latest"
  ]
}
```

### Schritt 2: Netzwerk-Isolation 🌐
**Ziel**: Prüfe ob Netzwerkzugriffe das Hängen verursachen

```bash
# OpenCode ohne Netzwerkzugriff starten
unshare --net opencode
# oder
firejail --net=none opencode
```

### Schritt 3: Cache/State Reset 🗑️
**Ziel**: Prüfe ob gespeicherter Auth-State das Problem ist

```bash
# Backup erstellen
cp -r ~/.local/state/opencode ~/.local/state/opencode.backup
cp -r ~/.cache/opencode ~/.cache/opencode.backup

# State löschen
rm -rf ~/.local/state/opencode
rm -rf ~/.cache/opencode

# OpenCode neu starten
```

### Schritt 4: oh-my-opencode Downgrade 📦
**Ziel**: Teste ältere kompatible Version

```bash
# In opencode.json:
"plugin": ["oh-my-opencode@3.1.8"]  # oder 3.1.0, 3.0.0
```

---

## Mögliche Lösungen

### Lösung A: Redundante Auth-Plugins entfernen ✅
**Wenn**: Plugin-Konflikt ist die Ursache

Nur **benötigte** Plugins behalten:
```json
{
  "plugin": [
    "opencode-antigravity-auth@latest",  // für Antigravity + Gemini CLI
    "oh-my-opencode@3.1.9"                // für Agent-Framework
  ]
}
```

Entfernen:
- opencode-anthropic-auth (redundant, da über Antigravity verfügbar)
- opencode-gemini-auth (redundant)
- @gitlab/opencode-gitlab-auth (nicht benötigt)

### Lösung B: Plugin-Ladereihenfolge optimieren 🔄
**Wenn**: Race Condition beim Plugin-Loading

```json
{
  "plugin": [
    "oh-my-opencode@3.1.9",           // Zuerst laden
    "opencode-antigravity-auth@latest" // Dann Auth
  ]
}
```

### Lösung C: Timeout-Konfiguration ⏱️
**Wenn**: Provider-Validierung timeout

In opencode.json hinzufügen:
```json
{
  "timeout": {
    "provider": 5000,
    "model": 3000
  }
}
```

### Lösung D: oh-my-opencode Minimal Mode 📦
**Wenn**: Spezifische oh-my-opencode Features das Problem verursachen

```json
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json",
  "google_auth": false,
  "disabled_hooks": ["auto-update-checker", "startup-toast"],
  "mcps": {
    "context7": {"disabled": true},
    "grep_app": {"disabled": true}
  }
}
```

---

## Kritische Dateien & Pfade

### Konfiguration
- `/home/jannis/.config/opencode/opencode.json` - Haupt-Config, Plugin-Liste
- `/home/jannis/.config/opencode/oh-my-opencode.json` - Agent-Config
- `/home/jannis/.config/opencode/antigravity.json` - Antigravity Auth Config

### Logs
- `/home/jannis/.local/share/opencode/log/` - OpenCode Logs
- Neuestes Log: `2026-01-31T182920.log`

### Cache & State
- `~/.cache/opencode/` - Plugin-Installationen, npm packages
- `~/.local/state/opencode/` - Auth-State, Model-Cache
- `~/.config/opencode/node_modules/` - Konfigurationsspezifische Dependencies

### Backups
- `/home/jannis/.config/opencode/oh-my-opencode.json.backup.20260131_053917` - Original
- `/home/jannis/.config/opencode/oh-my-opencode.json.backup.20260131_184917` - Nach erster Korrektur

---

## Dual-Quota-System (für spätere Implementierung)

### Google Antigravity Quota
```
google/antigravity-gemini-3-flash
google/antigravity-gemini-3-pro
google/antigravity-claude-sonnet-4-5
google/antigravity-claude-opus-4-5-thinking
```

### Google CLI Quota (separates Limit!)
```
google/gemini-3-flash-preview
google/gemini-3-pro-preview
google/gemini-2.5-flash
google/gemini-2.5-pro
```

**Vorteil**: Beide Quotas parallel nutzbar durch manuelle Modellnamen-Switches

---

## Provider-Level Fallback (bereits implementiert in oh-my-opencode v3.1.9)

**Funktionsweise**:
- Jeder Agent hat interne Fallback-Chain
- Beispiel: `claude-opus-4-5` → `anthropic` → `github-copilot` → `antigravity`
- Automatischer Wechsel bei Provider-Nichtverfügbarkeit

**Einschränkung**:
- Runtime error-based failover (429-Fehler) noch nicht implementiert
- Feature-Request: https://github.com/code-yeongyu/oh-my-opencode/issues/1114

---

## Diagnoseergebnisse ✅

### Test 1: oh-my-opencode Plugin isoliert
**Konfiguration**: Nur `oh-my-opencode@3.1.9`, keine anderen Plugins, minimale oh-my-opencode.json
**Ergebnis**: ❌ **OpenCode hängt weiterhin**

### Test 2: Komplett ohne oh-my-opencode
**Konfiguration**: Leere Plugin-Liste in opencode.json
**Ergebnis**: ✅ **OpenCode startet sofort und funktioniert einwandfrei**

### Test 3: oh-my-opencode v3.1.8
**Ergebnis**: ❌ **Hängt**

### Test 4: oh-my-opencode v3.0.0
**Ergebnis**: ❌ **Hängt**

## ROOT CAUSE IDENTIFIZIERT 🎯

**Problem**: Das **oh-my-opencode Plugin (alle getesteten 3.x Versionen)** hat einen Bug, der auf diesem System ein Hängen beim Start verursacht.

**Nicht das Problem**:
- ❌ Modellnamen in oh-my-opencode.json
- ❌ google_auth Konflikt
- ❌ Konflikt mit antigravity-auth Plugin
- ❌ Provider-Konfiguration

**Das tatsächliche Problem**:
- ✅ Bug im oh-my-opencode Plugin selbst
- ✅ Tritt auf allen getesteten Versionen auf (3.0.0, 3.1.8, 3.1.9)
- ✅ System-spezifisch (funktioniert auf anderem PC)

## Nächste Schritte (Priorität)

1. ✅ **Vollständige Dokumentation erstellt**
2. ✅ **Test: Nur oh-my-opencode Plugin** → HÄNGT
3. ✅ **Test: Minimale oh-my-opencode.json** → HÄNGT
4. ✅ **Plugin-Downgrade testen** → ALLE HÄNGEN
5. ⏳ **GitHub Issue erstellen** bei oh-my-opencode Repository
6. ⏳ **Workaround finden** oder auf Bugfix warten

---

## Wichtige Kommandos

### OpenCode mit Debug-Logs starten
```bash
timeout 10 opencode --print-logs --log-level DEBUG 2>&1 | tee /tmp/opencode-debug.log
```

### OpenCode ohne Netzwerk
```bash
unshare --net opencode
```

### Plugin-Cache neu aufbauen
```bash
rm -rf ~/.cache/opencode/node_modules
opencode # wird Plugins neu installieren
```

### Verfügbare Modelle auflisten
```bash
opencode models | grep "google\|anthropic\|openai\|github"
```

---

## Referenzen

- **OhMyOpenCode GitHub**: https://github.com/code-yeongyu/oh-my-opencode
- **Multi-Provider Fallback Feature**: https://github.com/code-yeongyu/oh-my-opencode/issues/1114
- **Antigravity Auth Plugin**: https://github.com/NoeFabris/opencode-antigravity-auth
- **OpenCode Providers Docs**: https://opencode.ai/docs/providers/
- **OpenCode Models Docs**: https://opencode.ai/docs/models/

---

**Token-Status**: ~90K/200K verwendet
**Letztes Update**: 2026-01-31 19:30 Uhr

---

## Für neue Sessions ohne Context

**Problem-Zusammenfassung**:
OpenCode hängt beim Start, wenn oh-my-opencode Plugin geladen ist. Log zeigt Hängen bei `/provider` Request nach Plugin-Loading. Wahrscheinlich Auth-Plugin-Konflikt oder Provider-Validierungs-Timeout.

**Aktueller Status**:
Diagnose-Phase - Systematisches Testen von Plugin-Isolationen steht noch aus.

**Sofort-Maßnahmen**:
1. Test mit nur oh-my-opencode (ohne antigravity-auth)
2. Minimale oh-my-opencode.json
3. Cache/State Reset
