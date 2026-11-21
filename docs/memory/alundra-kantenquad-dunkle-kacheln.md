---
name: alundra-kantenquad-dunkle-kacheln
description: "Alundra Kantenquad: Zone mit nur schwarzen (rgb 0) oder einer einzigen wiederholten Kachel bekommt keinen Quad; bestätigt 2026-11-21"
metadata:
  node_type: memory
  type: project
  originSessionId: b0d71f8b-4114-4512-8b0d-9145cc7dc2ea
  modified: 2026-11-21T16:36:30.440Z
---

Raum mit Kamera X=0 und dunkler Füllfläche links der Raumwand: Kacheln x<72 sind rgb-0-Sprites (0x65000000) und eine wiederholte Füllkachel (clut/uv 0x..1090). Der Quad machte daraus einen harten schwarzen Block (zusätzlich zum schwarzen Rand jenseits der Karte).

**Fix (bestätigt, Nutzer: "Ist weg"):** `alundra_tiles_overlap` in [mods/alundra_widescreen.c](../../../../RecompDev/alundra-recomp/mods/alundra_widescreen.c) ignoriert Sprites mit rgb 0 und verlangt mindestens zwei verschiedene helle Kacheln (Wort p+12 = clut|v|u) in der Quadzone. Debug- und Release-Build neu gebaut.

**Offen:** Außenbereich mit einheitlichem Rand (reines Gras) könnte jetzt keinen weichen Rand mehr bekommen; ungetestet. Ergänzt [[alundra-kantenquad-kleine-raeume]].
