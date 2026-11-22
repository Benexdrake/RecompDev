# Phase 4: Mod Kartenrand-Verlauf (`map_edge_fade`)

Ziel: Der weiche Übergang ins Schwarze am Kartenrand (heute im Dorf) wird ein eigener, einzeln schaltbarer Mod. Nur dort, wo er explizit angelegt ist.

## Ausgangslage (bestätigt im Alt-Mod)

- Pro Kartenseite ein Gouraud-Semitrans-Quad (cmd 0x3A, davor E1 0xE1000040, subtraktiv B-F), Farbe 0xFF am Rand → 0 nach innen, y 0..240, OT-Slot 959 (über Welt, unter Wolken und HUD).
- Pakete in einer 128-B-Arena (`psx_mod_alloc_gpu_dma_memory`), jeden Frame neu geschrieben.
- Kartenrand-Bildschirm-X = `-camX` (links) bzw. `52*24 - camX` (rechts). Quad wird übersprungen, wenn außerhalb des Bildes.
- Dorf: rechts 28 px (`ALU_EDGE_W`), links 12 px (`ALU_EDGE_W_VILLAGE_L`). Die erste Kartenspalte links ist eine hellgraue Felswand; breitere Verläufe schwärzten sie.
- Hook bisher auf Site 0x8002D444 (Wort 0x00007021).

## Aufgaben

1. `alundra_edgefade.c`, Plugin `alundra.edgefade`, Hook auf 0x8002D444 (Mehrfachregistrierung siehe Phase 1, sonst Dispatcher).
2. **Keine Heuristik mehr.** Statt `alundra_tiles_overlap`/`alundra_zone_dark` eine Raumtabelle: Hash → {Breite links, Breite rechts, Kartenspaltenzahl, Zielfarbe}. Anfangseinträge: Dorf `0x0B440C2D` und `0xB4655671` (links 12, rechts 28). Alle anderen Räume: kein Quad.
3. Kartenbreite aus der Tabelle statt fest 52 (Innenräume können abweichen).
4. Verlauf ist subtraktiv gegen Schwarz. Hat ein Raum eine andere Clear-Farbe, muss das Verlaufsziel zur Clear-Farbe passen, sonst Farbsprung (Tabellenfeld `Zielfarbe`).
5. Prüfen, ob der Verlauf im Dorf bei Clear = Schwarz noch nötig ist (vorher stand die Wand ohne Verlauf hart neben dem Schwarz; vermutlich ja).
6. Weitere Räume nur auf Nutzerwunsch eintragen (Außenrand mit einheitlichem Gras ist ungetestet).

## Test

- Dorf links und rechts, mit `map_edge_fade` an/aus, mit `background_color` an/aus (Kombinationen).
- Räume ohne Eintrag: nichts gezeichnet, kein Flackern.
- Kamera am Rand (X=0, X=927), Übergang beim Raumwechsel.

## Abnahme

Nutzer bestätigt, dass das Dorf wie im Alt-Mod aussieht ("fertig, bestätigt").
