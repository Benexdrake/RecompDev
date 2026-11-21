# Alundra Widescreen (16:9) — Übergabe für eine neue Session

Stand: 2026-11-20. Projekt: `c:\RecompDev\alundra-recomp` (Alundra, DE, SLES-01256, statische Rekompilierung auf psxrecomp). Schwesterprojekt mit Vorlage: `c:\RecompDev\bof3-recomp\WIDESCREEN_HANDOFF.md`.

## Zum Einstieg in die neue Session

Sag Claude zum Beispiel: *"Lies C:\RecompDev\ALUNDRA_WIDESCREEN_HANDOFF.md und mach bei 'Offen / nächste Schritte' weiter."*
Die Kurzfassung steht auch im Memory (`alundra-recomp-status`).

## Ziel und Stand

- **Ziel:** 16:9 ohne schwarze Balken, auch an Kartenrändern, bei Sprites, Menüs und Videos sauber.
- **Erreicht:** Der Nutzer bestätigt, dass es im Release-Build gut aussieht (Hintergrund-Kacheln füllen die ganze Breite, keine Balken mehr).
- **Ungeprüft:** Kartenränder (Kamera ganz links/rechts), Sprite-/Objekt-Pop-in am Rand, Menüs, Dialogboxen, Videos, Städte, Dungeons mit anderen Kamera-Modi.

## Was anders ist als bei BoF3

Alundra ist ein **reines 2D-Kachelspiel** und nutzt das GTE praktisch nicht. Deshalb funktionieren die BoF3-Wege nicht:

- `gte_game_mode = true` hält die Anzeige für immer auf 4:3, weil nie Vertices projiziert werden (`ws_game_mode()` in `psxrecomp/runtime/src/gpu.c`). Richtig ist **`[widescreen] full_2d = true`**. Dann ist `game_mode` immer 1.
- Es gibt keine GTE-Screen-X-Culls (`screen_x_sites` entfallen). Die Breite steckt im Kachel-Code selbst (siehe unten) und wird per Instruktions-Hook geändert.
- Die Debug-Anzeige `gpu` zeigt `ws.active 0` und `configured 0`, obwohl es läuft. Verlässlich ist `present_native_43`: 0 heißt 16:9, 1 heißt 4:3 (bei Videos und Logos gewollt).

## Was umgesetzt ist

1. **Plugin** [alundra-recomp/mods/alundra_widescreen.c](alundra-recomp/mods/alundra_widescreen.c): schaltet `psx_mod_set_fixed_display_aspect(16, 9)` ein (Aktivierung) und enthält vier Instruktions-Hooks für die Kachel-Schleife (nächster Abschnitt).
2. **Manifest** `mods/preloaded/packages/alundra.enhancement.widescreen/1.0.0/manifest.toml` (`format_version = 11`, Target `SLES-01256`, Feature standardmäßig an, `experimental`).
3. **CMake:** `target_sources(psx-runtime ...)` und `target_include_directories(... runtime/include)` in [alundra-recomp/CMakeLists.txt](alundra-recomp/CMakeLists.txt).
4. **game.toml:** `[widescreen] full_2d = true` am Dateiende und unter `[recompiler]` die Zeile `mod_instruction_sites = ["0x8002CED0", "0x8002CEF0", "0x8002CF04", "0x8002D14C"]`. Beides braucht eine **Neugenerierung des Spiel-C** (über 10 Minuten).
5. Sicherungen: `game.toml.bak`, `CMakeLists.txt.bak` (Stand vor allen Widescreen-Änderungen).

## Der Kachel-Code (Haupt-EXE)

Der Hintergrund wird von einer Funktion zwischen `0x8002CE..` und `0x8002D440` gezeichnet. Aufrufer `0x8002CDE0`.

- Kacheln sind **24×16-Sprites** (GP0 `0x65`), pro Frame ca. 330 Stück. Kamera-X liegt bei `0x800E4328` (wird auf max. 927 begrenzt), Kamera-Y bei `0x800E432C`.
- Erste sichtbare Spalte = `camX / 24`, Feinversatz `s6 = camX % 24`. Spaltenzahl steht in `24($sp)`: 15 Spalten, oder 14 bei Feinversatz >= 16 (`0x8002CED0` bzw. `0x8002CF04`).
- X-Positionen kommen aus einer **festen Tabelle im EXE bei `0x800203F0`**: `0, 24, 48, ... 336` (15 Werte, `u16`). Direkt dahinter liegt die Y-Tabelle (`0x80020410`), deshalb lässt sie sich nicht verlängern. Die Schleife liest sie über `t7` (Setzen bei `0x8002D144/0x8002D148`).
- Die Kartendaten liegen als 52 Spalten × 8 Byte pro Zeile (Zeilenabstand 416 Byte), Ende einer Zeile ist `0xFFFF`. Die Schleife prüft, ob Spaltenindex und Tile-ID gültig sind (`< 960`).
- Zeilenschleife: `0x8002D100`..`0x8002D43C`, Zeilenanzahl aus `0x800ED868`.

### Die vier Hooks (alle im Plugin)

| Adresse | Original | Hook |
|---|---|---|
| `0x8002CED0` | `SW t8,24($sp)` (t8 = 15) | Spaltenzahl auf 15 + 6 = 21 |
| `0x8002CF04` | `SW t8,24($sp)` (t8 = 14) | Spaltenzahl auf 14 + 6 = 20 |
| `0x8002CEF0` | `SW s6,16($sp)` (s6 = erste Spalte) | Start bis zu 3 Spalten früher (nie vor Spalte 0, `shift = min(3, col)`) und eigene X-Tabelle neu schreiben: `x[i] = (i - shift) * 24` |
| `0x8002D14C` | `ADDIU t1,s0,13` (direkt nach `t7 = 0x800203F0`) | `t7` auf die eigene Tabelle im Expansion-1-Speicher (`psx_mod_alloc_guest_memory`) |

Ergebnis im Debug-Build: Kachel-X von -95 bis 385 statt -23 bis 337. Die Hooks laufen vor der Instruktion; deshalb wird `t7` erst nach seinem `ADDIU` gesetzt.

Mehr Spalten brauchen: X-Bereich für 16:9 etwa -53..373, dazu Feinversatz. Mit 3 Spalten links und 21 gesamt ist das abgedeckt. Für 21:9 müsste man `ALU_LEFT_COLS`, `ALU_EXTRA_COLS` und `ALU_TABLE_LEN` im Plugin erhöhen.

## Bauen und Starten

```bash
cd /c/RecompDev/alundra-recomp
export PATH="$HOME/.local/share/retcomm/toolchains/cmake-clang-v1/1.0.14/bin:$PATH"
# Spiel-C nur bei Änderung an game.toml (Cull/Hook-Sites, full_2d) neu erzeugen:
python psxrecomp/psxrecomp_cli.py generate --config game.toml --project-root .
# Runtime bauen:
python psxrecomp/psxrecomp_cli.py rebuild --config game.toml --project-root . --build-dir build-release --no-pgo
# Debug-Build (sonst ist der GP0-Ring leer):
python psxrecomp/psxrecomp_cli.py rebuild --config game.toml --project-root . --build-dir build-debugtools --no-pgo --cmake-extra=-DPSX_DEBUG_TOOLS=ON
```

- Spiel vorher beenden (`taskkill //F //IM Alundra.exe`), sonst ist die EXE gesperrt.
- Start: `build-release/Alundra.exe`, Arbeitsverzeichnis `build-release`.
- Debug-Start: `cd build-debugtools; PSX_DEBUG_SERVER=1 ./Alundra.exe --debug-port 4370`. Der Server braucht nach dem Start 30–60 s, vorher kommt "Cannot connect".
- Die Meldung "Generate failed" nach "Generate complete" ist harmlos. Bei Rebuild-Fehler zuerst prüfen, ob das Spiel noch läuft.
- Die Disc liegt als `C:\Discs\Alundra\Alundra.cue` (aus der CHD erzeugt, siehe Memory).

## Nützliche Debug-Befehle (Client: `python psxrecomp/tools/debug_client.py <cmd> k=v`)

- `gpu` (Anzeige/ws-Status), `gpu_ring_stats` (neuester Frame), `gpu_frame_dump frame=<n>` (jedes GP0-Paket mit `pc`, `ra`, `func`). Auszählen: Op `0x65` = Kachel, `0x7F` = 16×16-Sprite, `0x2D/0x2F` = Polygone.
- `wtrace_add <lo> <hi>`, `wtrace`: wer schreibt ein Paket? Das hat die Kachel-Funktion gefunden.
- `disasm addr=0x... count=N`, `read <addr> <len>`, `screenshot_wide_hires path=...` (zeigt das echte Fensterbild; Read kann PNGs lesen). Bei Videos zeigt der Screenshot Rauschen, das ist nur das Roh-VRAM.
- `input 0x0008` (Start) und `clear_input`, um Intro und Menüs zu überspringen.

## Offen / nächste Schritte

1. **Kartenränder prüfen:** Kamera ganz links/rechts. Links wird nie vor Spalte 0 gelesen (dort bleibt dann ein schwarzer Streifen, was korrekt wäre). Rechts liest die Schleife über das Kartenende hinaus; das Zeilenende `0xFFFF` sollte das abfangen. Wenn dort Müll erscheint, an `0x8002D150..0x8002D174` ansetzen. Bekannt ist, dass die Kamera-X-Grenze 927 nicht zu einer Kartenbreite von 960 passt; nicht geklärt.
2. **Weitere Ebenen:** Es gibt wohl noch Vordergrund-Ebenen oder andere Kachel-Funktionen, die nicht durch diese vier Hooks laufen. Mit `gpu_frame_dump` prüfen, ob in einer Szene Ränder fehlen, und andere `pc`/`func`-Werte außer `0x8002D...` verfolgen.
3. **Sprites und Objekte:** Nicht angefasst. Objekt-Culls gegen X 0..320 vermutlich im Haupt-EXE (siehe Tomba-Muster in `psxrecomp/docs/WIDESCREEN.md`, ca. Zeilen 440–500: `addiu +Bias`, `sltiu`, Spawn/Despawn). Mit `0x7F`-Paketen und `wtrace` die Erzeuger finden. Falls dort Pop-in auftritt, entweder weitere `mod_instruction_sites` oder `screen_x_sites`/Cull-Sites.
4. **Menüs, Dialoge, HUD:** Prüfen, ob Boxen mittig bleiben oder gestreckt wirken. Optionen sind `auto_ui_squash` und `auto_ui_anchor` unter `[widescreen]`.
5. **Videos und Logos:** Bleiben absichtlich 4:3 (Pillarbox).
6. **Weitere Szenen:** Städte, Dungeons, Kämpfe gegen Bosse, Kamera-Sprünge und Szenenwechsel (Spielstände unter `saves/`).

## Rahmenbedingungen

- Der Nutzer beurteilt das Bild selbst; Claude kann nur per `screenshot_wide_hires` selbst schauen. Nach Änderungen Rückmeldung einholen.
- Das Projekt ist kein Git-Repository. Vor größeren Änderungen `game.toml` und `CMakeLists.txt` sichern.
- Framework-Regeln (`psxrecomp/CLAUDE.md`): Generierten Code nie von Hand ändern, kein `fprintf`-Debugging, nur TCP-Debug-Befehle.
- Dokumentation im Framework: `psxrecomp/docs/WIDESCREEN.md`, `psxrecomp/docs/MOD_PACKAGES.md` (Plugins, `[[patch]]`, Instruktions-Hooks), `psxrecomp/docs/MOD_MEMORY_ADDRESSES.md`, `psxrecomp/docs/GPU_FRAME_TOOLS.md`.

## Update 2026-11-21 (Kartenrand)

- **Behoben:** Am rechten Kartenrand (Kamera-X max 927, Karte 52 Spalten breit) las die erweiterte Schleife in die nächste Zeile und zeichnete Müll. Die Spaltenzahl wird jetzt in den Hooks `0x8002CED0`/`0x8002CF04` auf `52 - erste Spalte` begrenzt (Plugin, ohne Neugenerierung). Dahinter ist Schwarz; der Nutzer fand das gut.
- **Verworfen:** Randspalte klonen (Hook `0x8002D150`) und Klon zu Schwarz abdunkeln (Hooks `0x8002D220`/`0x8002D390`, Cmd `0x64` + Farbe): Streifen und Grafikfehler. Aus dem Plugin entfernt; die drei Sites stehen noch in `game.toml` und im generierten C (wirkungslos), beim nächsten Regen entfernen.
- **Offen:** a) Weicherer Übergang ins Schwarze (Idee: nur die letzten echten Spalten abdunkeln oder Verlaufs-Overlay). b) Frisch gebauter Release-Build hing beim Start (kein Fenster, Log endet nach der Overlay-Autocompile-Zeile); der Debug-Build startet normal. Ursache unbekannt, neu prüfen.
