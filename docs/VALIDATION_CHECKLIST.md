# WANDA Schnell-Validierung 🚀

> **Ziel**: In 5 Minuten das gesamte System prüfen.

---

## 1. System-Check (30 Sekunden)

```bash
# Diagnostik laufen lassen
bash ~/wanda-agentic-system/scripts/diagnostics.sh
```

**Erwartetes Ergebnis**:
- ✅ Python3, Node.js, Bun: OK
- ✅ Ollama: running
- ✅ Docker: OK
- ✅ OpenCode config: **symlinked** (Wurde gerade gefixt!)
- ✅ NVIDIA GPU: 8192MB VRAM
- ✅ Modelle: `brainstorm-36b`, `neo-20b`, `heretic-12b`

---

## 2. Agenten-Check (1 Minute)

```bash
# OpenCode starten und Agenten prüfen
opencode
```

Im OpenCode prompt tippen:
```
/agents
```

**Erwartete Agenten** (von oh-my-opencode):
- `oracle` - Recherche
- `librarian` - Dokumentation
- `brainstormer` - Ideation
- `frontend-dev` - UI/UX (via micode)

**Keine Duplikate!** Wenn du denselben Agenten zweimal siehst, ist etwas falsch.

---

## 3. Telegram Bot (1 Minute)

```bash
cd ~/wanda-agentic-system/wanda_local
source venv/bin/activate  # Falls venv existiert
pip install python-dotenv python-telegram-bot
python telegram_bot.py
```

**Dann in Telegram**:
1. Öffne: https://t.me/wandavoice_bot
2. Sende `/start` → Sollte Willkommensnachricht zeigen
3. Sende `/status` → Sollte System-Status zeigen
4. Sende eine Voice Note → Sollte "Transkribiere..." antworten

---

## 4. Handbook Dashboard (30 Sekunden)

```bash
# Öffne das Dashboard im Browser
xdg-open ~/wanda-agentic-system/docs/WANDA_HANDBOOK.html
```

**Prüfe**:
- ✅ Die **Intelligenz-Pyramide** ist sichtbar (Mermaid Diagramm)
- ✅ **Model Matrix** zeigt:
  - Cloud Core (Indigo): Claude 4.5, Gemini 3
  - Local Voice (Grün): Ollama brainstorm-36b
- ✅ Keine alten/falschen Modellnamen

---

## 5. Safety Test (30 Sekunden)

```bash
cd ~/wanda-agentic-system
python -c "from wanda_local.src.safety import SafetyChecker, SafetyLevel; c=SafetyChecker(); print('rm -rf / :', c.check('rm -rf /').level); print('git status:', c.check('git status').level)"
```

**Erwartetes Ergebnis**:
```
rm -rf / : SafetyLevel.DENY
git status: SafetyLevel.ALLOW
```

---

## 6. Profile-Switch Test (30 Sekunden)

```bash
# Aktuelles Profil prüfen
ls -la ~/.config/opencode/opencode.jsonc

# Zu Experimental wechseln
ln -sf ~/wanda-agentic-system/wanda_cloud/profiles/experimental/opencode.jsonc ~/.config/opencode/opencode.jsonc

# Zurück zu Stable
ln -sf ~/wanda-agentic-system/wanda_cloud/profiles/stable/opencode.jsonc ~/.config/opencode/opencode.jsonc
```

---

## ✅ Validation Complete Checklist

| Test | Status |
|---|---|
| Diagnostics: All OK | ☐ |
| OpenCode: Config symlinked | ☐ |
| Agenten: Keine Duplikate | ☐ |
| Telegram: Bot antwortet | ☐ |
| Handbook: Pyramide sichtbar | ☐ |
| Safety: rm -rf blocked | ☐ |
| Profile: Switch funktioniert | ☐ |

**Wenn alles ☑️ ist: WANDA ist einsatzbereit!** 🎉
