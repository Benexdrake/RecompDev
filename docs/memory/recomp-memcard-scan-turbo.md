---
name: recomp-memcard-scan-turbo
description: "Spielstand laden (Memory-Card-Scan) lief ~4 s im Vblank-Takt; Framework lässt Vblanks jetzt ungebremst laufen, solange Kartensektoren gelesen werden; bestätigt \"sehr viel schneller\""
metadata:
  node_type: memory
  type: project
  originSessionId: b0d71f8b-4114-4512-8b0d-9145cc7dc2ea
  modified: 2026-11-21T16:44:22.894Z
---

Alundra-Laden (2026-11-21): Das BIOS liest die ganze Memory Card sektorweise (176 Transaktionen, 0x52), ~34 ms pro Sektor = 2 Vblanks, Host-Thread schläft zu 90 % (Host-Sampler `host_profile.py`, ohne CPU-Last). Kein fsync beteiligt (nur bei Schreibzugriff 0x57).

**Fix (bestätigt):** `g_psx_card_read_activity` in `psxrecomp/runtime/src/sio.c` (zählt Sektorlesungen), in `main.cpp` vor `probe_turbo` hält ein Zähler (4 Vblanks) `turbo_loads_active = 1`, nur wenn Spiel gestartet, kein Netplay/Selfcheck. Unabhängig von `g_turbo_loads_enabled`. Debug- und Release-Build neu gebaut. Gilt für alle Projekte mit dem gemeinsamen Framework (BoF3/BoF4/LoD noch nicht neu gebaut).

**Why:** Der CD-Speed-Fix aus [[recomp-cd-speed-ladezeit]] hilft hier nicht, die Karte ist nicht CD-gebunden.

**How to apply:** Nächster Schritt bei Ladezeit: Raumwechsel-Rest (~1,5 s Spiellogik). Debug-Hilfen: `host_profile.py --port 4370 --exe ... --since SEQ` (SEQ ≈ ms seit Start), Befehl `pc` existiert nicht.
