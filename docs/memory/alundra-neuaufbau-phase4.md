---
name: alundra-neuaufbau-phase4
description: Phase 4 Widescreen-Neuaufbau: Kartenrand-Verlauf als eigener Mod map_edge_fade mit Raumtabelle (Debug-Build grün, Spieltest offen)
metadata:
  type: project
---

Phase 4 (2026-11-22): `mods/alundra_edgefade.c`, Plugin `alundra.edgefade`, Feature `map_edge_fade`, Hook 0x8002D444 (Wort 0x00007021, Site schon in game.toml, kein generate nötig). Raumtabelle `g_alu_edge_rooms` {sig, w_l, w_r, cols, dark}: Dorf `0x0B440C2D` und `0xB4655671` (12 / 28 / 52 Spalten / 0xFF). Alle anderen Räume: kein Quad. Nur bei margin > 0. Quad-Aufbau wie Alt-Mod (Slot 959, 128-B-Arena).
- `dark` = Grauwert, der am Rand subtrahiert wird (statt "Zielfarbe"); bei Clear != Schwarz anpassen.
- Debug-Build grün, **nicht spielgetestet**. Offen: Verlauf im Dorf bei Clear = Schwarz nötig? (Test mit Feature an/aus), Kamera X=0/927.
**How to apply:** Neuer Raum = Eintrag in der Tabelle. Siehe [[alundra-neuaufbau-phase3]].
