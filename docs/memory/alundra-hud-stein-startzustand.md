---
name: alundra-hud-stein-startzustand
description: Alundra HUD: großer 10-HP-Stein über die Punkte, "/N" ausgeblendet; Startzustand-Falle (Spiel schreibt HUD-Pakete vor dem ersten Start-Menü an anderen Positionen); bestätigt 2026-11-21
metadata:
  type: project
---

Ab 10 Max-HP fasst das Spiel 10 HP zu einem großen Stein zusammen (Sprite 0x65, 16x16, u=96 v=40, clut 31186, im Puffer 0x80175D00). Gewünscht und umgesetzt (`mods/alundra_hud.c`): Stein oben links über den kleinen HP-Punkten (`ALU_HUD_STONE_Y` = 0), "/N"-Glyphen (clut 31058, x<0xF0) ausgeblendet (dy -400). Nutzer bestätigt.

**Startzustand-Falle (wiederholt aufgetreten, auch bei den "/10"-Glyphen, siehe [[alundra-hud-glyph-start-fix]]):** Bis der Nutzer das Start-Menü einmal geöffnet und geschlossen hat, schreibt das Spiel HUD-Pakete an anderen Positionen: Stein bei (51,192) statt (104,16), 6. Herz-Spalte bei x=3 (schon Endposition), "/N" bei x=3. Positions-/Bereichsklassifikation (x<0x70 = Item-Slot, `y < 0x40`-Filter) verfehlt sie dann, sie landen unten bei den Items oder werden nie angefasst.

**Graue Stein-Variante (2026-11-22, gefixt, vom Nutzer bestätigt "Perfekt"):** Bei weiterem Spielfortschritt erschien der Stein grau und blieb unverschoben bei (51,192) unten; Menü auf/zu half nicht. Ursache: der graue Stein ist eine andere Textur, u=144 (0x90), v=40, gleiche CLUT 31186, 16x16, cmd 0x65 (Paketwort +12 = 0x79D22890). Die Erkennung kannte nur den orangen mit u=96. Match jetzt: cmd 0x65, v=40, u in {96, 144}, Größe 0x00100010. Die CLUT war NICHT das Problem (erste Vermutung war falsch). Weitere Stein-Varianten (andere u) sind denkbar: Das Spiel zeigt vermutlich je nach HP-Zustand/Fortschritt verschiedene Texturen. Tritt es wieder auf: Debug-Build, `read 0x80175D00 2560`, per Python Pakete mit y>100 und x<0x70 auflisten (Wort +12 = clut<<16|v<<8|u), das fehlplatzierte 16x16-Sprite bei etwa (51,192) suchen und sein u in die Stein-Bedingung in `alundra_hud.c` aufnehmen.
**Test-Falle:** Immer den Debug-Build (`build-debugtools`) testen UND neu bauen; Release allein zu bauen hat zu einem Test auf altem Code geführt. Ein fehlendes Diagnose-Logfile hieß: falscher Exe lief.

**Why:** Der Fehler war nur im frischen Start ohne Menü sichtbar; ein Test nach einmal Start-Drücken sieht korrekt aus und täuscht.
**How to apply:** HUD-Änderungen immer im frischen Zustand testen (Spiel neu starten, Spielstand laden, Start NICHT drücken). Pakete über die Textur (u, v, clut) erkennen, nicht über Position. Bei Fehlplatzierung `read 0x80175D00 2560` im fehlerhaften Zustand auslesen (oder temporär per `fopen` in den Hook loggen: der Hook sieht die Spiel-Koordinaten nach dem Undo), bevor man die Logik umbaut.
