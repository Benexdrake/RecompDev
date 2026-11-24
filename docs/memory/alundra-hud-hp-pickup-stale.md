---
name: alundra-hud-hp-pickup-stale
description: Alundra US HUD: nach HP-Stein-Pickup (max 10->11) bleibt das HUD-Layout bis zum Menue veraltet; Hook platziert Stein/Herzen absolut (bestätigt 2026-11-24)
metadata:
  type: project
---

Beim Pickup (max HP 10 -> 11, `0x800AA0F0`) ändert das Spiel nur die Texturen der HUD-Pakete. Positionen schreibt es erst beim nächsten HUD-Gleiten (Start-Menü): Stein bleibt bei (-53,16) geparkt, 6. Herz-Spalte bei (3,16)/(3,24), Herzen im 10-HP-Layout. Der Hook schob den Stein dadurch per Item-Zweig nach (-106,192).

Fix (`mods/alundra_hud.c`): `alundra_hud_layout_stale` (max == 11 und Stein-x < 0 in einer Parität) -> `alundra_hud_slot_target` setzt Stein (16-m,16), Nachbarteil (24-m,16) und 12 Zellen (32-m+8i, 16/24) absolut. Slots: Stein 0x80119630/0x80119694, Zellen ab 0x801196BC / 0x80119734 / 0x801197AC / 0x80119824 (20 B). Zusätzlich prüft das Undo nur noch die Position, nicht die Textur.

**Why:** Spiel-Layout ist nach HP-Änderung bis zum Menü veraltet, relative Verschiebung trifft dann falsche Ausgangswerte.
**How to apply:** Gilt nur für max == 11. Bei max >= 12 ist das Zellenlayout unbekannt (ungetestet). Nur Debug-Build gebaut. Tools: Write-Trace-Polling in Dauerschleife blockiert das Spiel, nicht verwenden.
