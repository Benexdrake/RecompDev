---
name: alundra-rand-fuellung-mine-unter-maske
description: Alundra Mine links: Außenfüllung bei aktiver Maske unter der Maske in Clear-Farbe (0,8,0) statt gesampelt über der Maske; ersetzt die Defer-Variante
metadata:
  type: project
---

Symptom (2026-11-22): Mine, Kamera X>0, linker Außenstreifen (-53..-cam) bräunlich statt schwarz, farbabhängig von der Position, Nebel/Vignette dort abgeschnitten.

**Ursache:** Bei aktiver Maske wurde die Füllung per `alundra_def_add` hinter das erste Maskenquad gehängt (also ÜBER den Nebel), flach in einer VRAM-Farbe aus Spalte x=2 (enthält Maske schon, Kartenrand liegt außerhalb VRAM -> nicht samplebar). Farbe hing so von der Kamera ab.

**Fix:** `defer` (Maske im Vorframe aktiv) -> Füllung normal in OT-Slot 959 (unter der Maske) mit fester Clear-Farbe `g_alu_clear` (0x000800). Entspricht dem Original außerhalb der Karte. Ohne Maske bleibt die gesampelte Farbe. `alundra_def_add` ist jetzt ungenutzt. Release + Debug gebaut. Nutzer 2026-11-22: Nebel wieder im Vordergrund (besser); Farbe passt weiterhin nicht ganz, bewusst so belassen.

Ersetzt den Defer-Teil von [[alundra-rand-fuellung-maske-mine]].
