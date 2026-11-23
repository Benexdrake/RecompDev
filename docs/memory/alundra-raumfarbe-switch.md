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

**Mine-Raum 3 (2026-11-22, bestätigt "sehr gut"):** Hash `0x56AA69AF` (Rand-Hash `0x52D040E7`). Kamera-Bereich: Karte 52 Spalten, aber nur Spalten 8..22 gefüllt; links/rechts davon leere schwarze Spalten (0,0,0), die Kacheln dazwischen sind (8,8,0). Die sichtbare "Naht" liegt an der ersten gezeichneten Kachelspalte, nicht an der Kartenkante.
- In `alundra_after_tiles` für diesen Raum: `xl = 8*24 - cam`, `xr = 22*24 - cam` (19 war falsch: Kantenquad lag auf der Wand, schwarzer Streifen), `defer = 1`, `clr = g_alu_room_mine1` (0x000808 = (8,8,0)). Hier läuft KEINE Ringmaske-`defer`-Kette, ohne den Zwang waren die Füllquads schwarz (Farbe 0 im Dump).
- Außenfüllung wird für diesen Raum auch gezeichnet, wenn der Kantenquad schon da ist (`!drew_x || room3`), sonst blieb außen (0,8,0).
- Reihenfolge: Die 90-%-Dunkelfüllung (`alundra_dark_fill`, aus `alundra_after_tiles` herausgelöst) wird für Raum 3 VOR den Außenfüllquads gebaut (= liegt darüber). Sonst verdeckte die deckende (8,8,0)-Füllung sie. Andere Räume: alte Reihenfolge am Ende.
- `ALU_DARK_FILL_COLOR` (global, alle Mine-Räume): 0xE6 (90 %) war zu hart -> 0xCC (80 %) -> 0x99 (60 %) -> aktuell **0x66 (40 %)**, vom Nutzer so übernommen. Nur Debug gebaut.
- Methode: Pixelwerte per PIL aus `screenshot_wide_hires` (Übergänge pro Zeile), `gpu_frame_dump` auf OT 959 (Quads/Farbe), Kachelkante = 24k - cam. Frame-Dumps wechseln zwischen leer und voll.

**Neuer Raumfarben-Eintrag (2026-11-23, Neuaufbau, `mods/alundra_bgcolor.c`):** Hash `0x4FB456CC` (Haus mit Teppichen/Rüstungen, Kamera X=0, Y=113). Screenshot-Messung: Rand außerhalb 4:3 (0,0,0), Leere im Raum (8,0,0) -> Clear `0x00000008` (BBGGRR). Debug gebaut, Sichtprüfung durch Nutzer offen.
- Zweiter Raum mit gleicher Farbe: Hash `0x9A06E323` (Kamera X=927), ebenfalls `0x00000008`.
- Dritter Raum, gleiche Farbe: Hash `0x11F00FF2` (Kamera X=0, Y=592), `0x00000008`.
- Vierter Raum, gleiche Farbe: Hash `0xA6A16DE9` (Kamera X=0, Y=90), `0x00000008`.
- Fünfter Raum, gleiche Farbe: Hash `0x40F3F4AC` (Kamera X=0, Y=154), `0x00000008`.
- Sechster Raum, gleiche Farbe: Hash `0x9CB94CD1` (Kamera X=0, Y=544), `0x00000008`. Eingetragen, noch nicht gebaut.
- **Default geändert (2026-11-23):** `alundra_room_color` default = `0x00000008` (8,0,0) statt Schwarz, nach 6 Räumen mit gleichem Befund (Hashes 0x4FB456CC, 0x9A06E323, 0x11F00FF2, 0xA6A16DE9, 0x40F3F4AC, 0x9CB94CD1; Einzeleinträge entfernt). Skelett- und Mine-Räume bleiben explizit.
- **Kantenverlauf (alundra_edgefade.c, 2026-11-23):** Der subtraktive Randverlauf endete in Schwarz, Hintergrund ist jetzt (8,0,0). Pro Seite zusätzlich additiver Quad (E1 0xE1000020, Farbe 0x000008 am Rand -> 0), Arena 384 B (0/64 sub, 256/320 add). Sichtprüfung offen.

**Raum mit Treppe (2026-11-23):** Hash `0x8A1528CF` (Wort-FNV wie `alundra_room_sig`; Byte-FNV `0xB3A82EE5` war falsch) (Kamera X=0x17, Y=0xA8), dunkler Raum mit Wolkenschicht. Nutzer-Farbe (R,G,B)=(0,8,0) -> in der Skelett-Gruppe (`0x00000800`) von `alundra_room_color` eingetragen. Debug gebaut, Sichtprüfung offen.
- Gruft zweite Map: Hash `0xA5781E10` (Kamera X=0, Y=0xDB), ebenfalls (0,8,0). Debug gebaut.
- Gruft dritte Map: Hash `0x5944BC3C` (Kamera X=0, Y=0x60), ebenfalls (0,8,0). Eingetragen, noch nicht gebaut.

**Raum per Screenshot (2026-11-23):** Hash `0x7C900F86` (Rand-Hash `0xD30699D0`), Screenshot-Farbe (R,G,B)=(8,8,0) -> `0x00000808` in `alundra_room_color` (zusammen mit `0xB2956EA2`). Hash per Debug-`read` des Kartenpuffers (Pointer 0x800DD86C) berechnet. Debug gebaut, Sichtprüfung offen.
