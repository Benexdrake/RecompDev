---
name: alundra-cheat-gilder
description: Alundra US Gilder-Adresse und Cheat cheat_infinite_money (Debug-Build)
metadata:
  type: project
---

Gilder (US, SLUS-00553): s16 bei Zeiger(0x80119AE8)+8 (aktuell 0x801DD824), gelesen von 0x8004F5F4, Deckel 9999. 0x800AA0FC ist nur die animierte Anzeige (zaehlt +10/Frame hinterher, Schreiben dort bringt nichts).
Cheat: Feature `cheat_infinite_money`, Plugin `alundra.cheat_money` in `mods/alundra_cheats.c`, Default aus, schaltbar im Mod-Menue / `state.toml`. Nur Debug gebaut (2026-11-25), ungetestet.
