---
name: alundra-heller-rand-schwarz
description: "Alundra 16:9: heller Kartenrand (Baumkronen) bekommt schwarzen Außenbereich + Verlaufsquad wie das Dorf; bestätigt 2026-11-22, nur Debug-Build"
metadata:
  node_type: memory
  type: project
---

Stelle: linker Kartenrand weit oben auf der Karte (Baumkronen). Vorher füllte der VRAM-Randfarben-Fill (siehe [[alundra-randfarbe-fill-stale-spalte]]) den Außenbereich olivgrün mit vertikalem Verlauf, weil `alundra_tiles_overlap` den Kantenquad verwarf. Weiter unten auf der Karte passte es schon.

**Fix (bestätigt, Nutzer: "sieht gut aus", 2026-11-22):** In `alundra_after_tiles` ([mods/alundra_widescreen.c](../../alundra-recomp/mods/alundra_widescreen.c)) pro Seite `fixed_l` / `fixed_r`. Gemessen wird direkt hinter der Quadzone (links xl+ALU_EDGE_W+2, rechts xr-ALU_EDGE_W-3, geklemmt), damit der Quad die Messung nicht verfälscht. Hat eine der 5 Verlaufsstufen einen Kanal >= 0x50 (`alundra_col_bright`), wird die Seite wie das Dorf behandelt: Außenbereich schwarz (`g_alu_black`), Verlaufsquad immer gezeichnet. Dunkle Ränder (Mine, (8,8,0)-Wände) unverändert.

**Stellschraube:** Schwelle 0x50 in `alundra_col_bright`. Falls helle Ränder woanders ungewollt schwarz werden, erhöhen.

**Test:** Nur Debug-Build gebaut (`build-debugtools`), Release nicht neu gebaut (Nutzerwunsch, steht in CLAUDE.md). Mine und Dorf nach der Änderung vom Nutzer als ok gemeldet ("sieht gut aus").
