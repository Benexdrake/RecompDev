---
name: alundra-randfarbe-fill-stale-spalte
description: "Alundra 16:9 Außenbereich neben Kartenrand per VRAM-Farbe füllen, Stale-Spalte und Lücken-Fill im Game-Over-Bild; bestätigt 2026-11-21, Release+Debug gebaut"
metadata:
  node_type: memory
  type: project
---

Alle drei Fixes in `mods/alundra_widescreen.c`, Hook `alundra_after_tiles` (Site 0x8002D444). Nutzer: "perfekt". Release + Debug 2026-11-21 20:38 gebaut.

**1. Kantenquad-Schwelle 4** (`alundra_tiles_overlap`, `seen[4]`): Minenraum, Kamera X=0, linke Zone hatte genau 3 clut|u (7A40/00, 7A80/00, 7A80/18) -> dunkler Streifen. Jetzt >=4 nötig. Ergänzt [[alundra-kantenquad-fuellspalte]].

**2. Außenbereich-Fill in Kartenfarbe** (`alundra_edge_sample`, `alundra_outside_build`): Außerhalb der Karte zeigt das Spiel den Clear-Fill (Fill-Befehl 0x02, 0x000800 = RGB 0,8,0), die Randkacheln innen sind z.B. (8,8,0) bzw. grau-braun -> harte, sichtbare Kante. Lösung: flacher deckender Quad (cmd 0x28, OT-Slot 959) im Außenbereich in der Farbe der Randspalte. Farbe aus dem VRAM des Vorframes (`gpu_vram_peek`, Draw-Area über `gpu_get_drawing_environment`; Mod darf `#include "gpu.h"`), Modus aus 15 Zeilen in Spalte xl+2 bzw. xr-3. Nur wenn der Rand im 320-px-Bild liegt messen, Farbe pro Seite merken (`g_alu_rgb_l/r`), sonst gemerkte nutzen (Rand außerhalb VRAM, Kamera X>0 -> sonst falsche, helle Farbe). Nur wenn auf der Seite kein Gradientenquad gezeichnet wird. Arena 256 B = 4 Pakete (Gradient L/R, Fill L/R). Fallen: Bedingung `xl > 0` war falsch (bei Kamera X=0 liegt der Außenbereich bei x<0, `xl > -m` nötig). Früher abgelehnt: schwarzer Quad (alles schwarz), additiver Verlauf. Stale: gemerkte Farbe kann nach Raumwechsel veraltet sein, bis der Rand einmal im Bild war.

**3. Game-Over-Bild rechts** (`alundra_fix_stale_col` + Lücken-Fill): Die Szene ist nur ~14 Spalten breit, das Spiel zeichnet 15 Spalten (x bis 360, in 4:3 unsichtbar). Die 15. Spalte (x=336) enthält stale Kacheln (alle 16 gleich, clut 7840/u0/v10) = hellgrauer 24-px-Balken in 16:9. Fix: rechteste Spalte mit x>=320, 16 identische Kacheln, die sich von der Nachbarspalte unterscheiden, bekommt u/v/clut der Nachbarspalte. WICHTIG: die oberste Zeile (y=0) liegt im OT-Slot 0, Durchläufe 1/2 scannen ab Slot 0 (Suche nach xmax ab Slot 5, wegen HUD in 0..4). Danach bleibt rechts ein Streifen (360..373), weil nur 15 Spalten gezeichnet werden: Fill-Quad in Farbe von VRAM-Spalte 316, nur wenn Kartenrand nicht im Bild (`xr >= 320 + m`).

**Grenzen/Risiko:** Echte, senkrecht uniforme Spalte am rechten Rand (Wand, Fluss aus 16 gleichen Kacheln, x>=320) würde fälschlich überschrieben. Bei Feinscroll in Y (y nicht durch 16 teilbar) greift die Stale-Korrektur nicht. Es gibt keine Kartenbreite im RAM: Kamera-Clamp 927 und 52 Spalten stehen fest im Code (0x8002CEA4). Kartenzeilen-Daten (0x800DD86C) halfen nicht. Release-Exe zeigte vorher im Todesbild schwarzen 28-px-Balken links (alter Kantenquad) plus grauen Balken rechts.

**Debug-Tipp:** Frame-Dump nach `op 0x28 / 0x3A` filtern; Tile-Spalten per x gruppieren; Kamera `read 0x800E4328 8`.
