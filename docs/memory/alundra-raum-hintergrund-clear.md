---
name: alundra-raum-hintergrund-clear
description: Alundra: Skelett-Raum 0x793D39CF und Raum 0x1B8E3013 ohne Kantenquads/Füllung (bestätigt); was nicht ging und warum
metadata:
  type: project
---

Stand 2026-11-22, `mods/alundra_widescreen.c`, nur Debug gebaut. Bestätigt vom Nutzer ("sehr gut", links und rechts passt). Räume in `alundra_after_tiles` über `room_fill`: `0x793D39CF` (Skelett-Raum, lila Kugeln) und `0x1B8E3013` (Kante rechts nie geprüft).

**Lösung:** In diesen Räumen gar nichts am Rand zeichnen (`room_fill`: keine Kantenquads, keine Außenfüllung, keine Lücken-Füllung; `xl/xr` auf ±100000). Das Spiel-Clear-FillRect bleibt original (0,8,0). Die Karte läuft rechts weiter, `g_alu_map_cols` bleibt 52.

**Was nicht ging (alles vom Nutzer abgelehnt oder falsch):**
- Kantenquads: Zeichnen hängt an der Kachel-Heuristik `alundra_tiles_overlap`, die pro Frame wechselt (Wolken/Kameraversatz) -> Flackern. Ohne Quad fehlte zudem die Füllung.
- Außenfüllung aus VRAM: enthält die Wolkenschicht, Farbe wechselt mit den Wolken.
- Feste Füllung (Schwarz oder 0,8,0) in Slot 959: sieht wie "Kantenblock" aus.
- Clear-FillRect auf Schwarz (Pakete 0x801F4388 / 0x801F4688, Stride 0x300, cmd 0x02): Nutzer wollte es wieder weg. Außerhalb sah es zudem zu schwarz gegenüber dem Rest aus.
- Spaltenlimit 12: FALSCH, der Raum geht rechts weiter (Spieler läuft dort), das Limit schnitt echte Karte ab und sah wie schwarzer Block aus. Vorher prüfen, ob "Reste" wirklich Reste sind (Spieler dort hinlaufen lassen).

**Neuen Raum:** Hash per Python (FNV-1a über 24960 B ab Pointer 0x800DD86C; `debug_client.py --port 4370 read`, ohne `--port` geht es nicht), Raumkante am Screenshot (Kachelkante = 24k - cam). Kamera X liegt hier nicht bei 0 (Karte beginnt bei Spalte 2, Kamera z. B. 5/20/174).
Siehe [[alundra-raumfarbe-switch]].
