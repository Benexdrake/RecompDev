---
name: alundra-pillarbox-raumliste
description: Alundra schwarze Seitenbalken (4:3) in Szenen, die in 16:9 fremde Räume am Rand zeigen; Raumliste, Slot 959, Cutscene-Flag ungeeignet
metadata:
  type: project
---

Feature `pillarbox` (Plugin `alundra.pillarbox`, `mods/alundra_pillarbox.c`, Manifest + `CMakeLists.txt`), Stand 2026-11-23, nur Debug gebaut, Balken in der Melzas-/Kars-Szene bestätigt sichtbar (Nutzer: "es geht").

Hook auf Site 0x8002D444 (wie edgefade). Pro Seite ein deckend schwarzes Flat-Quad (cmd 0x28, davor eigener E1 0xE1000200), x -m..0 und 320..320+m, y 0..240. Auslöser: Raumliste `g_alu_box_rooms[]` ({sig, bsig} aus `alundra_room_sig` / `alundra_room_border_sig`). Eingetragen: `B3BDE1C5` / `E93D8AA1` (Melzas-/Kars-Szene). Neue Räume: Nutzer sagt "jetzt", Hash per RAM-Lesen von 0x800DD86C (FNV-1a über 416*60 B) berechnen und eintragen.

**Why:** Szene wechselt zwischen Maps, jede Map hat eigenen Hash, daher eine Zeile pro Map. Der Nutzer wollte erst einen Cutscene-Schalter.
**How to apply:**
- Draw-Reihenfolge im GPU-Dump: OT-Slots werden aufsteigend gezeichnet, Welt liegt bei ~64..954. Slot 5 wird VOR der Welt gezeichnet (Balken unsichtbar), Slot 959 danach, HUD-Block (Slots 0..9) kommt zuletzt.
- Cutscene-Flag gesucht, nicht gefunden: 0x800A8250 war in der Cutscene 1, blieb aber danach (auch im freien Spiel) auf 1, ist also kein Live-Flag. Weitere Kandidaten (0x80127DC8, 0x80138DBC, 0x80149BD8, 0x80149CC0) ungeprüft, andere Treffer schwanken mit der Animation. Figurposition neben der Kamera (0x800E4328/32C) nicht gefunden. Nutzer-Idee "Kamera folgt Figur nicht mehr" wartet auf eine Positionsvariable.
- Die Schiffs-Map `66E3A38D` ist freies Spiel, braucht keine Balken.
- Schalter: `build-*/mods/state.toml`, `[[feature]] id = "pillarbox"`, `enabled = false`. Der Schalter selbst ungetestet.
