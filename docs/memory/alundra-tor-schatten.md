---
name: alundra-tor-schatten
description: Alundra schwarzer Schatten-Kreis am Torfuß beim Durchlaufen, Ursache und Hook 0x8002DDF4, bestätigt 2026-11-22
metadata:
  type: project
---

Unter einem Tor (Säule mit Schatten, Raum mit Holzkisten/Laterne) erschien ein schwarzer Kreis am Säulenfuß, der beim Herauslaufen wieder im Boden lag. Ursache ist Spiellogik, kein Widescreen-Hook: Die generische Teil-Sprite-Routine (0x8002DC28..0x8002DE44, 14-B-Einträge, Aufrufer 0x8002E1DC) schaltet im Slot des Spielerschattens (a2 = OT-Slot-Pointer, zwei Paritäten, z.B. 0x800CB568 / 0x800CA658) von der normalen Definition (Eintrag 0x800E4D14) auf eine zweite (0x800E4D34) um. Diese zeichnet das Schatten-Quad (cmd 0x2F, uv/clut 0x780C5898) in fester Höhe (t4=116) und mit Spieler-x. Der normale Fußschatten läuft in einem anderen Slot weiter.

Fix: Hook `alundra_shadow_part` in `mods/alundra_widescreen.c`, Site 0x8002DDF4 (Wort 0x8D430000, direkt vor dem OT-Link, t2 = Pakettag, t6 schon +14, a2 = Slot). Lernt die Spieler-Slots (t6 == 0x800E4D30), klappt das Quad zusammen (vier Y = 0xFE00), wenn t6 == 0x800E4D50 im selben Slot erscheint. Schalter `ALU_HIDE_GATE_SHADOW` (Makro vorhanden, Hook-Code ohne #if). Vom Nutzer bestätigt ("verschwindet, sehr gut").

**Why:** Position im 16:9-Bild liess sich nicht anders von den Spielerschatten unterscheiden (gleiche Textur, gleiche Grösse); Unterscheidung nur über Teil-Definition + Slot.
**How to apply:** Bei weiteren Schatten-Artefakten Debug-Hook auf 0x8002DD94 (vor ADDIU t6,t6,14) mit Protokoll nach Datei nutzen; Eintrag = t6-14. Wenn der Spieler beim Start schon unter dem Tor steht, ist der Spieler-Slot noch nicht gelernt (Kreis dann sichtbar bis zum ersten normalen Frame). Siehe [[alundra-recomp-status]].
