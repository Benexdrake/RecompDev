---
name: alundra-kantenquad-fuellspalte
description: "Alundra Kantenquad: Füllspalte mit gleicher clut+u (nur v wechselt) zählt nicht als verschiedene Kacheln, mind. 3 verschiedene clut|u nötig; bestätigt 2026-11-21"
metadata:
  node_type: memory
  type: project
  originSessionId: 5b9d2bb4-acbb-4e8f-a40b-8975cb0423ae
---

Stelle mit Kamera X=927 (rechter Kartenrand, Raum mit Holzbrücke/Plattformen): breiter schwarzer Streifen am rechten Rand. Messung: Dunkle Randkacheln sind (0,8,0), gleich dem Clear-Fill außerhalb. Der subtraktive Quad drückt sie nach ~1 px auf 0, danach springt es auf 8 zurück: sichtbarer schwarzer Streifen (28 px breit). Die Zone enthielt 6 Kacheln mit clut 0x7940, u=0x30/0x90, v=0x60..0xB0; die alte Regel (>=2 verschiedene clut|v|u) zählte das als abwechslungsreich.

**Fix (bestätigt, Nutzer: "er ist weg"):** `alundra_tiles_overlap` in [mods/alundra_widescreen.c](../../../../RecompDev/alundra-recomp/mods/alundra_widescreen.c) vergleicht nur clut|u (ohne v) und verlangt mindestens 3 verschiedene. Debug-Build gebaut, Release noch NICHT neu gebaut.

**Nachtrag 2026-11-21 (Minenraum, Kamera X=0, linker Rand, bestätigt "ist weg"):** Die Zone hatte genau 3 verschiedene clut|u (7A40/00, 7A80/00, 7A80/18), Quad erschien als dunkler Streifen. Schwelle jetzt 4 (`seen[4]`). Ergebnis: nur noch eine harte Kante zwischen schwarzem Außenrand und Karte (akzeptiert, wie bei den anderen Fixes). Release + Debug gebaut (20:38).

**Fehlversuche (nicht wiederholen):** Flacher schwarzer Quad außerhalb der Karte (alles schwarz, Nutzer: kaputt). Additiver Quad (0,8,0) über der Zone (Gradient oder flach): sah anders aus, machte mehr kaputt. Der Nutzer wollte, wie bei den anderen Fixes, dass der Quad dort entfällt.

**Offen:** Heuristik. Heller Rand mit nur 1-2 Kachelarten (einheitliches Gras) bekommt evtl. keinen weichen Rand mehr. Im Mod gibt es kein VRAM-Lesen (`gpu_vram_peek` existiert nur im Runtime, Palette wird mit hellen Kacheln geteilt). Ergänzt [[alundra-kantenquad-dunkle-kacheln]], [[alundra-kantenquad-kleine-raeume]].
