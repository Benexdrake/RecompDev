---
name: alundra-neuaufbau-phase2
description: Phase 2 Widescreen-Neuaufbau umgesetzt (nur Debug-Build grün, Spieltest durch Nutzer offen)
metadata:
  type: project
---

Phase 2 (2026-11-22): `mods/alundra_widescreen.c` enthält jetzt den reinen Widescreen-Teil aus dem Legacy-File: 16:9, Kachelschleife (0x8002CED0/CF04/CEF0/D14C, feste Kartenbreite 52), Kachelpuffer-Arena (0x8002CFD8), Wolken (0x8005C538/C5F4/C4E8), Speicher-Nebel (0x800262EC), Ringmaske (0x8005D5E0), Tor-Schatten (0x8002DDF4). Weggelassen: Hook 0x8002D444 und alles Rand-/Füll-/Raumfarben-Zeug (Phase 3-5).
- Wolken-Randzählung bleibt (`g_cl_now`), Abholen per `alundra_cloud_edge_counts_take(out[4])` (non-static, noch nicht in `alundra_common.h` deklariert; Phase 5 entscheidet).
- `ALU_NO_TILEBUF`-Env-Schalter und `ALU_MASK_TRIM` entfielen.
- Debug-Build kompiliert und linkt. **Nicht spielgetestet** (Testmatrix Phase 0, Nutzer).
**Why:** Neuaufbau trennt Widescreen von Rand/Farbe/Dunkelräumen.
**How to apply:** Erwartet im Test: Rand = Spiel-Clear-Farbe, keine Quads, kein Flackern. Siehe [[alundra-neuaufbau-phase1-api]].
