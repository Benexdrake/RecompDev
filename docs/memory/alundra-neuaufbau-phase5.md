---
name: alundra-neuaufbau-phase5
description: Phase 5 Widescreen-Neuaufbau: Mine-Räume per Clear-Farbe Schwarz statt Füllquad (Debug-Build grün, Sichtprüfung offen)
metadata:
  type: project
---

Phase 5 (2026-11-22): In `mods/alundra_bgcolor.c` stehen die drei Mine-Räume (`0x877DDF27`, `0xD78EE04C`, `0x56AA69AF`) explizit auf Clear (0,0,0). Begründung: Alt-Mod = Außenfüllung (8,8,0) minus ~40 % Schwarz = praktisch Schwarz. Kein Füllquad im neuen Mod.
- Die Wolken-Randzählung (`alundra_cloud_edge_counts_take`, `g_cl_now`) bleibt in `alundra_widescreen.c` als Fallback für einen kleinen Dunkelfüllquad, falls Clear allein nicht reicht. Alt-Code `ALU_DARK_FILL_COLOR` liegt nur noch in `alundra_widescreen_legacy.c.txt`; Löschen/Aufräumen erst nach Nutzerabnahme (Phase 6).
- Debug-Build grün, **nicht spielgetestet**. Offen: Naht Wolkenschicht/Außen, Maskenband (24/32er Grau), Raum 3 ((8,8,0)-Kacheln gegen (0,0,0)-Leerspalten), Messung per Screenshot.
**How to apply:** Falls Naht sichtbar: Farbe im `case` anpassen (0x00BBGGRR); reicht das nicht, Quad im Wolken-Teil des Widescreen-Mods. Siehe [[alundra-neuaufbau-phase3]], [[alundra-mine-dunkel-fuellung]].
