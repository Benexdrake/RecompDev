---
name: alundra-kantenquad-kleine-raeume
description: "Alundra Kantenquad nur zeichnen, wenn Kachel-Sprites (0x65) in seiner Zone liegen; sonst schwarzer Balken in kleinen Räumen; bestätigt 2026-11-21"
metadata:
  node_type: memory
  type: project
  originSessionId: ba0a8d6e-87ec-44f6-be3c-12bd942891f2
  modified: 2026-11-21T15:59:30.874Z
---

Kleine Innenräume (z.B. Raum mit 3 Truhen, Kachel-x nur ~61..277): Die Karte ist im RAM immer 52 Spalten breit, der Raum füllt nur ~10. Der Clear-Fill ist (0,8,0). Der subtraktive Kantenquad (Slot 959) färbte die leere Fläche links rein schwarz, sichtbar als breiter schwarzer Balken.

**Fix (bestätigt, Nutzer: "ist weg"):** In `alundra_after_tiles` ([mods/alundra_widescreen.c](../../../../RecompDev/alundra-recomp/mods/alundra_widescreen.c)) prüft `alundra_tiles_overlap(ot, x0, x1)`, ob in den OT-Slots 5..958 ein 0x65-Sprite die Quad-Zone überlappt. Nur dann wird die Seite gezeichnet.

**Why:** Der erste Versuch über den Kachelpuffer 0x800DD878 (+13600*Parität) schlug fehl: Das Paketlayout stimmte nicht (src-Adressen sind 4 mod 20 versetzt, Inhalt wechselte). Die OT-Ketten-Suche ist robust.

**How to apply:** Bei weiteren Rand-/Quad-Artefakten in kleinen Räumen zuerst per `gpu_frame_dump` prüfen, ob 0x3A bei ot 959 noch auftaucht. Der Übergang dunkelgrüne Raumfläche → schwarz ist vermutlich Original und bleibt. Siehe [[recomp-docs-in-claude-md]].
