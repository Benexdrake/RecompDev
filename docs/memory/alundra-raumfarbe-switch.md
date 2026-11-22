---
name: alundra-raumfarbe-switch
description: Alundra: Außenfarbe unter der Maske pro Raum per switch auf FNV-Hash der Kartenzeilen; Mine-Problemraum auf Schwarz, default wie bisher
metadata:
  type: project
---

Stand 2026-11-22, `mods/alundra_widescreen.c`: `alundra_room_sig()` (FNV-1a über 416*60 B ab Pointer 0x800DD86C) und `alundra_room_clear()` (`switch`, `default` = `g_alu_clear` 0,8,0). Nur bei aktiver Maske (`defer`), sonst misst die Randfarbe wie bisher aus dem VRAM.

**Warum Hash:** Keine Karten-ID im RAM gefunden (Diff zweier Räume, zu verrauscht). Hash der Kartenzeilen ist pro Raum stabil (beim Scrollen gleich) und unterscheidet Räume.

**Räume:**
- `0x877DDF27` Mine-Problemraum (Kamera X=0, Außenbereich graugrün neben fast schwarzen Randkacheln): erst Schwarz (Nutzer: falsche Farbe), dann aus Screenshot gemessen: mit Schwarz außen (0,0,0) / innen (8,8,0), im Maskenband oben/unten außen (24,24,24) / innen (32,32,24). Maske addiert beidseitig gleich -> Füllung = Differenz = (8,8,0) = `0x000808` (BGR) für alle 5 Stützen. Messmethode: Screenshot per PIL, Median links/rechts der Naht pro Stützzeile (HUD-Zeilen auslassen). Das Clear-Grün (0,8,0) fehlte der Rotanteil.
- `0xD78EE04C` anderer Mine-Raum: Farbe passt schon, bleibt `default`.

**Bestätigt 2026-11-22: "Sieht gut aus" (Mine-Problemraum mit 0x000808).**

**Neuen Raum hinzufügen:** RAM-Dump (`read` in 16-KB-Blöcken), FNV-1a über die Kartenzeilen berechnen, `case` mit 5 Farben (0xBBGGRR, Stützen y=0,60,..,240) ergänzen. Release + Debug gebaut.

Siehe [[alundra-rand-fuellung-mine-unter-maske]], [[alundra-rand-fuellung-maske-mine]].

**Dorf (2026-11-22, bestätigt):** Hash `0xB440C2D` (`ALU_ROOM_VILLAGE`, Variable `fixed` in `alundra_after_tiles`). Außen fest Schwarz (`g_alu_black`, auch ohne Maske), Gradientenquad auf beiden Seiten erzwungen (Kachel-Heuristik `alundra_tiles_overlap`/`alundra_zone_dark` übergangen). Rechts 28 px (`ALU_EDGE_W`), links `ALU_EDGE_W_VILLAGE_L` = 12 px. Grund: Die erste Kartenspalte links (~25 px) ist eine hellgraue Felswand; breitere Verläufe (16/24/28/40/64) schwärzten sie und ließen die Wandkante hart wirken, ohne Verlauf (0) steht die Wand hart neben dem Schwarz. Der Quad selbst war nie falsch herum (Pakete geprüft: FF am Rand, 0 innen). Release + Debug gebaut. Sicherung: `mods/alundra_widescreen.c.pre_village`.
