---
name: alundra-rand-fuellung-blinken
description: Alundra Dialog: Außen-Füllquad links blinkte, weil alundra_edge_sample den Puffer-Ursprung aus dem Clip-Fenster nahm
metadata:
  type: project
---

Im NPC-Dialog (Kamera X=0, Raum links schwarz) blinkte der Streifen x -53..0 nach einer Weile.

**Ursache:** `alundra_edge_sample` (mods/alundra_widescreen.c) las den VRAM-Ursprung aus `env.area.left/top`. Dialoge setzen ein kleines Clip-Fenster (z. B. 80,148,319,181), dadurch wurden zufällige Pixel gesampelt und die Füllfarbe des Außenquads (cmd 0x28) wechselte.

**Fix (bestätigt 2026-11-22):** Ursprung fest x=0, y = 0 oder 240 (nach `area.top >= 240`); neue Farbe nur bei Mehrheit >= 8 von 15 Stichproben, sonst alte behalten. Release + Debug gebaut.

**How to apply:** Bei Sampling aus dem VRAM nie `area.left/top` als Bufferursprung nehmen. Der schwarze Streifen selbst ist der echte Kartenrand, der in 16:9 sichtbar wird, kein Fehler.
