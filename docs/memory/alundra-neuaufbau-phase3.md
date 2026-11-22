---
name: alundra-neuaufbau-phase3
description: Phase 3 Widescreen-Neuaufbau: Clear-FillRect pro Raum umgefärbt (Hook 0x80086CC4), vom Nutzer bestätigt
metadata:
  type: project
---

Phase 3 (2026-11-22): `mods/alundra_bgcolor.c`, Plugin `alundra.bgcolor`, Feature `background_color`. Das Clear-FillRect (0x02, 320x240) wird jeden Frame von einer Kopierschleife bei 0x80086CC4 (`SW a1,0(a0)`, Wort 0xAC850000) aus der DRAWENV-Vorlage (0x8013FAE8 / 0x8013FA64) in den OT-Ende-Block geschrieben (Pakete 0x801F4268 / 0x801F4568). Hook ändert a1 vor dem Schreiben, nur wenn Wort 0x02xxxxxx und das Wort bei a3+4 == 0x00F00140 ist. Site steht in `game.toml` (generate gelaufen).
- Nur bei margin > 0 (16:9) und Raum-Hash != 0. Default Schwarz, Tabelle: Skelett-Räume (0,8,0), Mine-Räume (8,8,0) (Werte aus dem Alt-Mod).
- Nutzer bestätigt: Hintergrund schwarz "perfekt"; Test mit Rot funktionierte (danach auf Schwarz zurück).
- Ungetestet: Schalter `background_color=false`, Flackern bei Laden/Menü/Dialog/FMV, Raumtabelle pro Raum. Nur Debug gebaut.
**Why:** Ersetzt Kantenquads/Füllung (siehe [[alundra-clear-layer-ansatz]]).
**How to apply:** Neue Raumfarbe = `case` in `alundra_room_color` (Format 0x00BBGGRR). Siehe [[alundra-neuaufbau-phase2]].
