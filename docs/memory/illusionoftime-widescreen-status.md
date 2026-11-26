---
name: illusionoftime-widescreen-status
description: Illusion of Time SNES 16:9 (2026-11-26): Feld-Raender per WsShadow natural (Standard), Menues clamp; Culling/HUD/Mode7 offen; cart_readHirom-Assert gepatcht
metadata:
  type: project
---

Projekt `illusionoftime-recomp`, Paket `illusionoftime.widescreen`, Plugin `src/illusionoftime_widescreen.c` (Kopie des Terranigma-Musters, ohne Weltkarte). Debug-Build mit TRACE=ON, Start `build\Debug\IllusionOfTimeSNESRecomp.exe "<ROM-Pfad>"`, Debug-Server 4377 (set_controller/step/screenshot, siehe [[terranigma-widescreen-status]]).

Getestet per Screenshot: Intro (Erde), Titel, Dateimenue ueber Karte, Schul-Szene, Feldszene (Dach/Gras) - alle in 398x224 ohne Fehler, Raender per `clamp`.

**Offen:** Welt-Streaming der Raender (Kamera-WRAM suchen, Provider wie Terranigma `WorldTile`), Sprite-/Objekt-Culling-Hooks (OAM-Emitter im ROM finden), HUD (oben, BG3?), Weltkarte/Mode7, BG3-Rahmenstreifen pruefen. Terranigma-Adressen NICHT uebertragbar.

**How to apply:** Zuerst Spielwelt weiterlaufen lassen und Randverhalten pro Szene beurteilen; dann erst Reverse-Engineering der Kartendaten.

**Update (Abend):** Feldszenen: BG1/BG2 sind 64x32-Ringe (512 px), Welt-X in WRAM `$068A` (== hScroll BG1; `$068C` != vScroll am Kartenrand, deshalb nur X pruefen). `natural` = `WsShadowSetWorld/SetScroll/RetainHistory(true)/West+EastKeep 12` + `WsShadowFrame` fuer Layer 0/1, BG3 (HUD) clamp 0x04; sonst alles clamp 0x07. Standard `natural`, Env `IOT_WS`. Ohne History bleiben Raender schwarz. NPCs erscheinen ausserhalb 4:3 (Culling vermutlich nicht noetig).
**Hänger:** Echte Ursache war `assert(0)` in `cart_readHirom` (cart.c:417, Lesen ausserhalb ROM) -> jetzt `cpu_trace_offrails`, Patch in `patches/snesrecomp-pal.patch`. Zweite Falle: Debug `step` pausiert das Spiel, Fenster "reagiert nicht" bis `continue`; Skripte immer mit `continue` beenden. Debug-`save_state N` (Datei) laedt in frischem Prozess nicht sauber; `savestate N`/`loadstate N` (UI-Slot) nutzen.
**Fix beim Laufen:** `$068A` eilt dem PPU-Hscroll um ~2 px/Frame voraus; strikte Gleichheit schaltete beim Scrollen auf clamp/schwarz. Jetzt Toleranz `|Signed10($068A - hScroll)| < 64`, Welt-X = `$068A + Signed10(hScroll[L] - $068A)`. In Bewegung (links/rechts) per Screenshot geprueft.

**Rand-Glitches rechts (Abend 2):** Ursache: Spiel streamt Spalten nur 32 Tile-Spalten voraus (Kamera+$100, Routine `$C2:B5F5` -> Builder `$C2:B6A6`), die 9 Randspalten rechts zeigten veralteten Ring-Inhalt (50-85 % falsch). **Loesung:** `PrepareMargins` ruft den Spiel-Builder `$C2:B6A6` offline auf (CpuState-Kopie, X=Layer*2, `$18`=Welt-X, `$1C`=`$068E`), liest den Staging-Puffer (`$06B2,X`: [dest][32 Words] links, +0x42 [dest][32 Words] rechts, Ring-Zeilenreihenfolge) in einen Cache je (Layer, Metatile-Spalte) und liefert ihn per `WsShadowSetWorldProvider` (ohne retainHistory, Welt-X + 512). Davor `RtlSaveSnapshotToMemory`, nach jedem Aufruf `RtlLoadSnapshotFromMemory` (nur WRAM-Restore reichte NICHT: Sim wich ab). Ergebnis: Rand links/rechts 0 % Abweichung (Pixelvergleich spaeterer nativer Frames), 60 fps Debug. Schutz: nur wenn `$06B2==$3100 && $06B6==$3184` und Spalte `< $0692,X` (Kartenbreite), sonst Hang (Interpreter-Cap 2 Mio. Schritte pro Aufruf). Cache-Epoche wechselt bei neuer `camY>>4` und alle 64 Frames.
**NPC/Objekt-Culling:** Hooks (`interp_bridge_add_pre_opcode_hook`, Bank b als $0b/$8b/$Cb): `$00:98F7`, `$02:AE21` (`CMP #$111/BCS`, Fenster [-80,$111+80)), `$03:C867` / `$03:C877` (Objekt-Emitter, +/-80). Nur in Feldszenen aktiv; sie aendern die Objektlisten (`$0C00`), gewollt.
**Tools:** `ram.py`/`shot.py`/`seam.py`/`dis.py` (65816-Disassembler) im Session-Scratchpad; Test "Rand stimmt?": Frame A, spaeter Frame B (gleicher vScroll, Delta-X>=60), A-Rand mit B[x-d] pixelweise vergleichen.

**Raumwechsel-Glitch (Kirche/Schule, 2026-11-26, vom Nutzer bestaetigt):** Beim Betreten kleiner Raeume erschien kurz Kachel-Muell im rechten Rand (Cache/Ring vom alten Raum). Fix: `TrackRoomChange()` in `illusionoftime_widescreen.c` hasht die Karten-Parameter (`$0692..$069F`, `$06B2..$06BB`); bei Aenderung Cache-Epoche erhoehen + `kSettleFrames = 6` Frames `clamp`. 120 Frames waren zu lang (Seiten gruen/schwarz, Raum nur 4:3 zentriert). Die Schule ist 512 px breit, im Bild sieht man bei Kamera rechts eine Naht bei ~x=157: das ist echte Raumarchitektur, kein Bug. Test per Debug-Server: `loadstate 1`, `set_controller up`, `step N`, `screenshot` (BMP landet im Exe-Ordner).
