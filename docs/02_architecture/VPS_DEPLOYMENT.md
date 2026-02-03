# WANDA VPS Deployment Architecture

> **Ziel**: 24/7 Verfügbarkeit von WANDA, auch wenn der lokale PC aus ist.

---

## Architektur: Hybrid Local + VPS

```
┌──────────────────────────────────────────────────────────────┐
│                      VPS (Always-On)                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Telegram Bot    │  │ Dashboard       │  │ Notifications│ │
│  │ (wanda-telegram)│  │ (nginx/static)  │  │ (webhooks)   │ │
│  └────────┬────────┘  └────────┬────────┘  └──────────────┘ │
│           │                    │                             │
│           └────────────────────┴─────────────────────────────│
│                            ↓ SSH Tunnel / WireGuard          │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                    LOCAL PC (Workstation)                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Ollama (36B)    │  │ Voice Gateway   │  │ OpenCode     │ │
│  │ brainstorm-36b  │  │ STT/TTS/VAD     │  │ Agents       │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│                                                              │
│  [50GB RAM | 8GB VRAM | Full Compute Power]                 │
└──────────────────────────────────────────────────────────────┘
```

---

## Was läuft WO?

| Komponente | VPS | Lokal | Warum? |
|---|:---:|:---:|---|
| **Telegram Bot** | ✅ | ❌ | 24/7 erreichbar für Nachrichten |
| **Dashboard (HTML)** | ✅ | ✅ | Kann überall gehostet werden |
| **Ollama (brainstorm-36b)** | ❌ | ✅ | Braucht 50GB RAM |
| **Voice Gateway (STT/TTS)** | ❌ | ✅ | Braucht GPU für Whisper |
| **OpenCode Agents** | ❌ | ✅ | Braucht lokale Dateisystem-Zugriffe |
| **Notifications Hub** | ✅ | ❌ | Push-Endpunkt immer erreichbar |

---

## VPS Setup (Minimal)

### 1. VPS Requirements
- **RAM**: 2GB (nur für Bot + Nginx)
- **CPU**: 1 vCPU
- **Storage**: 10GB
- **OS**: Ubuntu 22.04 LTS
- **Kosten**: ~5€/Monat (Hetzner, DigitalOcean, etc.)

### 2. Deployment Steps

```bash
# 1. SSH zum VPS
ssh user@your-vps-ip

# 2. Clone Repo
git clone https://github.com/jas0nOW/wanda-agentic-system.git
cd wanda-agentic-system

# 3. Python Setup (nur für Bot)
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
cd wanda_local
python3 -m venv venv
source venv/bin/activate
pip install python-telegram-bot python-dotenv

# 4. .env konfigurieren
cp .env.example .env
nano .env  # Token einfügen

# 5. Als Service starten
sudo cp /path/to/wanda-telegram.service /etc/systemd/system/
sudo systemctl enable wanda-telegram
sudo systemctl start wanda-telegram

# 6. Optional: Dashboard mit nginx hosten
sudo apt install -y nginx
sudo cp -r docs /var/www/html/wanda
```

### 3. Tunnel zum lokalen PC (für Ollama)

```bash
# Auf dem VPS: SSH Tunnel zum lokalen PC
ssh -R 11434:localhost:11434 user@local-pc-ip

# Oder: WireGuard VPN für stabilen Tunnel
```

---

## Lokal: PC Wach Halten

### Option 1: Systemd Inhibit (Linux)
```bash
# Verhindert Suspend während WANDA läuft
systemd-inhibit --what=idle:sleep --who="WANDA" --why="Voice Gateway aktiv" sleep infinity &
```

### Option 2: GNOME Settings
```bash
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
```

### Option 3: Keep-Awake Script (im Installer)
```bash
# Bereits erstellt: ~/wanda-agentic-system/scripts/keep-awake.sh
nohup ~/wanda-agentic-system/scripts/keep-awake.sh &
```

### Option 4: Wake-on-LAN (WoL)
Wenn der PC doch schläft, kann der VPS ihn aufwecken:
```bash
# Auf VPS: Installiere wakeonlan
sudo apt install wakeonlan

# Wecke den PC (MAC-Adresse des lokalen PCs)
wakeonlan AA:BB:CC:DD:EE:FF
```

---

## Fallback-Modus (Wenn Lokal PC aus)

Wenn der lokale PC offline ist, arbeitet die VPS-Komponente im "Lite Mode":

1. **Telegram Bot**: Nimmt Nachrichten entgegen, speichert sie als Queue
2. **Notification**: "Dein PC ist offline. Nachricht wird zugestellt, sobald er wieder online ist."
3. **Wenn PC wieder online**: Queue wird abgearbeitet, alle Nachrichten werden an Ollama gesendet

---

## Sicherheit

- **SSH Key Auth**: Keine Passwörter
- **Firewall**: Nur Ports 22, 80, 443
- **Telegram Token**: Nur auf VPS, nie im Repo
- **WireGuard**: Verschlüsselter Tunnel zwischen VPS ↔ PC

---

## Zusammenfassung

| Szenario | Was funktioniert? |
|---|---|
| **PC an, VPS an** | Volle Funktionalität (Voice + Chat + Mobile) |
| **PC an, VPS aus** | Lokale Voice + OpenCode. Kein Telegram. |
| **PC aus, VPS an** | Telegram nimmt Nachrichten an, Queue. Dashboard verfügbar. |
| **Beide aus** | Nichts. (Aber wer schaltet beide gleichzeitig aus?) |
