---
name: alundra-rand-fuellung-maske-mine
description: Alundra Rand-Füllung links (Kamera-Rand außerhalb): Verlauf aus 5 Stützstellen, Median wegen HUD, Füllung hinter der Ring-/Lichtmaske einhängen; Top/Bottom-Streifen ist die Maske selbst
metadata:
  type: project
---

Stand 2026-11-22 (alundra_widescreen.c, `alundra_after_tiles`). Nutzer: Dialograum passt, Mine links passt jetzt; offen: heller Streifen oben/unten (y<8, y>=232), Ursache siehe unten.

- **Erststart-Balken:** Füllfarbe wurde nur bei sichtbarem Kartenrand gesampelt. Jetzt auch bei Rand außerhalb 4:3 (Spalte x=2 links / 316 rechts).
- **Füllung = vertikaler Gouraud-Verlauf** (4 Quads x 36 B, Stützstellen y=0,60,..,240, `alundra_outside_build`), Farbe je Stützstelle als **Median** je Kanal über 13 VRAM-Zeilen (Mittelwert wurde von HUD-Item-Slots bei x<20, y192..224 hochgezogen). Glättung 1/4 Schritt, mind. 1 Stufe (normales Runden blieb 1-2 Stufen daneben stehen).
- **Maske (Mine):** Die Ring-/Lichtmaske (Slot 0, 120 0x2F-Quads) liegt nach Slot 959 und deckt auch den Außenbereich. VRAM-Farbe enthält sie schon -> doppelt angewendet (heller Streifen). Lösung: bei aktiver Maske (Vorframe) werden die Füll-Quads hinter das erste Maskenquad gelinkt (`g_alu_def_*`, in `alundra_mask_stretch`), nach Maske, vor HUD.
- **Dunkelzonen-Test** `alundra_zone_dark` unterdrückt den Kantenquad bei schwarzer Randzone.
- **Top/Bottom-Streifen:** kommen von der Maske selbst (Maskentextur hell in den obersten/untersten Zeilen, VRAM x=100 y0..7 und 232..239 = 0x848c), auch im 4:3-Original. Kein Fehler der Füllung. Option: Maskenstreifen y<8 / y>=232 im Hook entkoppeln.
Ergänzt [[alundra-rand-fuellung-erststart]], [[alundra-ring-maske-stretch]].

**Versuch Top/Bottom-Maskenstreifen weglassen (ALU_MASK_TRIM=8) gescheitert, 2026-11-22:** Die Maske hellt das ganze Bild auf, ohne die obersten/untersten Streifen wurden Ober-/Unterkante schwarz mit sichtbarer Kante zum aufgehellten Bild. Zurück auf `ALU_MASK_TRIM 0` (aus). Das helle Band ist Teil des Originals.

**Stand 2026-11-22 (Ende):** Top/Bottom-Band ist Original (mit widescreen=aus in 4:3 bestätigt). Texturzeilen-Clamp (v=8) sah schlecht aus, `ALU_MASK_TRIM` steht auf 0 = wie im Original. Offene Idee: Band per gemessenem Farb-Quad ersetzen, nur wenn Nutzer es wieder will.
