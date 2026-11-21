---
name: alundra-hud-glyph-start-fix
description: "Alundra HUD \"/10\"-Glyphen saßen beim Start (bis zum ersten Start-Menü) falsch bei den Item-Slots; Fix in alundra_hud.c, bestätigt"
metadata:
  node_type: memory
  type: project
  originSessionId: 891c64ea-4a16-441b-9cbd-71341d6d13fe
  modified: 2026-11-21T15:49:09.069Z
---

Bug (2026-11-21): Beim Start im Borderless/Vollbild saß "/10" unten links über den Item-Slots, bis der Nutzer das Start-Menü einmal öffnete und schloss (F10-Display-Wechsel half nicht).

Ursache: Das Spiel schreibt die x/y der "/10"-Glyphen nur einmal (nicht jeden Frame) und vor dem ersten Menü bei x=3 statt x=160. x=3 ist schon die Endposition neben den Herzen. `alundra_hud_post` klassifiziert nach Original-x: x<0x70 = Item-Slots → falsch nach unten (y+176, x-m).

Fix in `mods/alundra_hud.c`: (1) Glyphen mit Sprite-Cmd 0x64/0x65, x<0x70, y==0x10, v==40, clut 31058 werden nicht verschoben (dx=dy=0, außer beim Menü-Ausblenden). (2) Rückgängig-Tabelle ist jetzt dauerhaft pro Paketadresse (`g_hud_rec[640]`, Tex-Wort wird mitgeprüft) statt einer Liste pro Frame. Nutzer bestätigte: "sieht gut aus".

**Why:** Packet-Position vom Spiel kann in einem Startzustand von der erwarteten abweichen; Klassifikation allein über x ist fragil.
**How to apply:** Bei weiteren HUD-Fehlplatzierungen zuerst die Original-x/y des Pakets per `read 0x80175D00 2560` und `wtrace_add` prüfen (Spiel-eigene Werte vs. Hook), bevor man die Hook-Logik verdächtigt. Siehe [[alundra-hud-menue-ausblenden]].
