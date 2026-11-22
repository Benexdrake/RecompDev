---
name: alundra-mine-schatten-randquad
description: Alundra Schattenschicht (Mine u. a.) nur 4:3 breit: raumunabhängige Randquads aussen bei 50 %, Erkennung per Wolkenzellen-Zählung, bestätigt 2026-11-22, nur Debug
metadata:
  type: project
---

**Problem:** Die Schattenschicht (0x7F-Wolkensprites, Vignette) ist nur 4:3 breit (Bildschirm-X 0..320). Außerhalb zeigen sich unabgedunkelte Kacheln mit harter Naht. Nach Phase 5 (Clear-Schwarz statt Füllquad) trat das in der Mine auf.

**Lösung (bestätigt, "funktioniert"):** `mods/alundra_edgefade.c`, Hook-Site 0x8002D444. Pro Seite ein subtraktiver Gouraud-Quad (-m..0 bzw. 320..320+m, 8 px Rampe ins Band `ALU_BAND_RAMP`), OT-Slot 959, 4 Pakete à 64 B in 256-B-Arena. Stärke `F` = 0x808080 (**50 %**; getestet 100 %, 50, 30, 40 %, Nutzer blieb bei 50 %).
- **Erkennung raumunabhängig:** `alundra_cloud_edge_counts_take()` (aus `alundra_widescreen.c`, zählt in `alundra_cloud_loop` die Zellen colL x=0, outL x<0, colR x=304, outR x>=320). Seite links aktiv, wenn colL >= 12 und outL == 0; rechts analog. Gleiche Regel wie im Alt-Mod (`alundra_dark_fill`).
- **Falle (Ursache der ersten Fehlversion):** Eine Raum-Hash-Liste (`alundra_room_sig`) taugt dafür nicht. Der Hash läuft über alle Kartenzeilen und ändert sich, wenn die Karte sich ändert (Gras zerstört: `0x877DDF27` → `0x61AB56F0`), der Effekt verschwand dann. Rand-Signatur (`0x1C2DEAF6` für den Startraum) war nur ein Zwischenschritt, ist nicht mehr nötig.

**Wenn es woanders Probleme gibt:**
- Quad erscheint fälschlich (Außenbereich/Wolken): Schwelle 12 oder die Bedingung outL/outR == 0 prüfen; Zähler per Debug loggen.
- Quad fehlt in einem Raum: Zellenzahl am Rand dort messen (evtl. < 12 Zeilen oder Zellen außerhalb vorhanden).
- Rest-Naht: Das Band ist in der Mitte heller als oben/unten, ein konstanter Quad passt nie überall. Option: Y-Verlauf oder Schicht strecken wie [[alundra-ring-maske-stretch]].
- Nur Debug gebaut. Siehe [[alundra-neuaufbau-phase5]].
