---
name: alundra-clear-layer-ansatz
description: Alundra: Rand nicht mehr füllen, sondern die Clear-Schicht (FillRect hinter allen Grafiken) pro Raum einfärben; Debug-Testhilfe PSX_DEBUG_FILL_ONLY / PSX_DEBUG_FILL_RGB; nächster Schritt Widescreen-Mod in einzelne Dateien aufteilen
metadata:
  type: project
---

Stand 2026-11-22. Nutzerentscheidung: der bisherige Weg (Rand mit Quads/Füllung/Verlauf füllen) wird durch einen anderen Ansatz ersetzt. **Die Schicht hinter allen Grafiken, das Clear-FillRect, wird einfach in der gewünschten Farbe gefüllt.** Das gilt dann links und rechts, auf der ganzen Karte, ohne Randerkennung (Kachel-Heuristik `alundra_tiles_overlap`, Kantenquads, Spaltenlimit, `room_fill` entfallen dafür).

**Warum:** Die Randfüllungen flackerten, hingen an Heuristiken und sahen in manchen Räumen wie Blöcke aus (siehe [[alundra-raum-hintergrund-clear]], [[alundra-rand-fuellung-blinken]], [[alundra-raumfarbe-switch]]). Die Clear-Schicht liegt ohnehin unter allem und deckt jede Stelle ab, die das Spiel nicht übermalt.

**Farbe pro Raum:** Standard Schwarz, per Switch (Raum-Hash wie in [[alundra-raumfarbe-switch]]) je Karte eine andere Farbe. Es gibt wohl nur wenige Varianten: Grabstätte, Mine, Schuppen, Haus hatten alle dieselbe Randfarbe. Konkrete Farbwerte pro Raum noch zu ermitteln.

**Befund Clear-Paket:**
- Erstes Paket jedes Frames, vor allen Sprites (ot=65535, also im OT-Ende-Block neben E3..E6): FillRect, Befehl 0x02, 320x240, Farbe im Wort `0xCCBBGGRR`, d. h. Bytes +0..+2 = R, G, B, +3 = 0x02.
- Die Adresse wechselt mit dem Puffer (Seitenwechsel, Stride 0x300): beobachtet 0x801F4028, 0x801F3728, 0x801F3428. Nicht fest verdrahten, Paket über die Liste oder den Befehl finden. Hook-Vorschlag: Alundra-Variante der Clear-Routine (Schreiber 0x80086AAC ist nur der DMA-Walker).
- Einfach per Debug-`write` ins RAM schreiben blieb ohne Wirkung (Spiel schreibt das Paket neu); deshalb Eingriff im GPU-Decoder.
- Alter Eintrag aus [[alundra-raum-hintergrund-clear]]: Clear auf Schwarz per Paket (0x801F4388 / 0x801F4688) war schon einmal versucht; außerhalb wirkte es "zu schwarz" gegenüber dem Rest, weil Randkacheln dunkelgrün-schwarz sind. Die Farbe pro Raum soll das lösen.

**Testhilfe (Debug-Build, nur per Umgebungsvariable, `psxrecomp/runtime/src/gpu.c` vor `ws_shared_ui_packet`):**
- `PSX_DEBUG_FILL_ONLY=1`: alle Zeichenprimitive 0x20..0x7F werden verworfen (VRAM-Uploads bleiben, Spiellogik läuft). Zu sehen ist nur die Clear-Schicht. FMVs (MDEC) bleiben sichtbar.
- `PSX_DEBUG_FILL_RGB=BBGGRR` (hex, **Blau zuerst**): überschreibt die Farbe jedes FillRect (0x02). `FF0000` = Blau, `0000FF` = Rot. Alle FillRects werden gefärbt, auch Clears anderer Art.
- Start: `PSX_DEBUG_SERVER=1 PSX_DEBUG_FILL_ONLY=1 PSX_DEBUG_FILL_RGB=FF0000 ./Alundra.exe --debug-port 4370`. Nur Debug-Build, Release nicht gebaut. Im Spielfeld noch nicht bestätigt (nur Titel/FMV-Screenshot gesehen).
- Mods dafür abgeschaltet: `build-debugtools/mods/state.toml` braucht pro `[[feature]]` zusätzlich `package_id = "alundra.enhancement.widescreen"`, sonst startet das Spiel nicht (Mods unavailable). Original ist `state.toml.orig`.
- `debug_client.py screenshot_file <pfad>` nimmt den Pfad positional (nicht `path=`), relativ zum Build-Ordner.
- Weitere Startoptionen: `--headless` (kein Fenster/Audio), `--hidden-window`, `--headless-opengl`.

**Nächster Schritt (Nutzer):** Widescreen aufteilen, jeder Mod in eine eigene Datei. Heute steckt vieles in `mods/alundra_widescreen.c` (Kacheln, Kartenrand, Wolken, Speicherraum-Wolken, Maske, Tor-Schatten, Kachelpuffer, Raumfarbe) plus `mods/alundra_hud.c`. Aufteilung in je ein Feature/Plugin/Manifest-Eintrag; dabei den Rand-Code durch den Clear-Layer-Ansatz ersetzen. Sites in `game.toml` brauchen danach `generate`.
