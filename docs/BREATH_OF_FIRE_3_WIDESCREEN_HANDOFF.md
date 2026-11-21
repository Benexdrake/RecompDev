# BoF3 Widescreen (16:9) — Übergabe für eine neue Session

Stand: 2026-11-20. Projekt: `c:\RecompDev\bof3-recomp` (Breath of Fire III, EU, SLES-01304, statische Rekompilierung auf psxrecomp).

## Zum Einstieg in die neue Session

Sag Claude zum Beispiel: *"Lies WIDESCREEN_HANDOFF.md und mach bei Abschnitt 'Nächste Schritte' weiter."*
Die Notiz im Memory (`bof3-widescreen-status`) enthält eine Kurzfassung davon.

## Ziel und Stand

- **Ziel:** 16:9 Widescreen im Kampf, im Feld und auf der Weltkarte.
- **Erreicht:** 16:9 läuft. Der Nutzer hat bestätigt, dass Kampf und Feld das Bild in voller Breite füllen.
- **Offener Fehler:** Am linken und rechten Rand erscheinen schwarze, leere Stellen. Sie werden beim Bewegen gefüllt und wieder gelöscht (Pop-in). Es ist im Kampf und im Feld gleich. Das spricht für gemeinsamen Code oder eine gemeinsame Ursache. Der Nutzer hat bisher keine Weltkarte, keine Städte und keine FMVs bewertet.
- Auf dem Bildschirm sichtbar war es zum Beispiel an der linken Höhlenwand im Kampf, dort sind Polygone gezackt abgeschnitten.

## Was die 16:9-Anzeige ermöglicht (bereits umgesetzt)

1. **Warum `game.toml` / `settings.toml` allein nicht reichen:** Die Runtime setzt jeden Aspect-Wert dort auf 4:3 zurück (`psxrecomp/runtime/src/main.cpp` ca. Zeile 20253, Meldung `widescreen is mod-owned on PSX; clamping display aspect`). Widescreen darf nur ein Mod-Plugin einschalten.
2. **Plugin:** [mods/bof3_widescreen.c](mods/bof3_widescreen.c) registriert ein Aktivierungs-Plugin `bof3.widescreen`, das `psx_mod_set_fixed_display_aspect(16, 9)` aufruft.
3. **Manifest:** [mods/preloaded/packages/bof3.enhancement.widescreen/1.0.0/manifest.toml](mods/preloaded/packages/bof3.enhancement.widescreen/1.0.0/manifest.toml). Es braucht `format_version = 11`. Mit Version 5 wurde es ignoriert, weil `channel` pro Feature erst ab Version 6 geht. Das Feature ist `experimental` und standardmäßig an.
4. **CMake:** [CMakeLists.txt](CMakeLists.txt) bindet das Plugin per `target_sources(psx-runtime ...)` und `target_include_directories(... runtime/include)` ein.
5. **Spielmodus-Erkennung:** In [game.toml](game.toml) steht `[widescreen] gte_game_mode = true`. Ohne diese Zeile stuft das Framework BoF3-Szenen (keine Sprite-Tags) als Nicht-Spielmodus ein und zeigt sie in 4:3 mit Pillarbox (`gpu_ws_present_native_43` in `psxrecomp/runtime/src/gpu.c`, Zeile `native_43 = !game_mode || ws_2d_only_scene()`).
6. **Weitere Zeilen in `game.toml`:** `aspect_ratio = "16:9"` und `[widescreen.cull] auto_screen_x = true`. Die letzte Zeile bewirkt in BoF3 nichts (siehe unten), sie ist harmlos.
7. `build-release/settings.toml` steht auf `aspect_ratio = "16:9"`. Das ist nur Kosmetik und wird vom Launcher überschrieben.

Wichtig: Das ist **Native-wide**, nicht Squash. Es wird breiter gerendert und die Spiel-Culls müssen mitgeweitet werden. Genau diese Culls fehlen noch.

## Bauen und Starten

Die Werkzeugkette liegt außerhalb des Standard-PATH:

```bash
cd /c/RecompDev/bof3-recomp
TC="$HOME/.local/share/retcomm/toolchains/cmake-clang-v1/1.0.14/bin"
PATH="$TC:$PATH" python psxrecomp/psxrecomp_cli.py rebuild \
  --config game.toml --project-root . --build-dir build-release --no-pgo
```

- Das Spiel vorher beenden (`taskkill //F //IM BreathOfFire3.exe`), sonst ist die EXE gesperrt.
- Start: `build-release/BreathOfFire3.exe`, Arbeitsverzeichnis `build-release`.
- Ein Runtime-Rebuild braucht einige Minuten. Eine Neugenerierung des Spiel-C (`psxrecomp_cli.py generate ... --disc "C:/Discs/BOF3/Breath of Fire III (Europe).cue"`) dauert über 10 Minuten und ist nur nötig, wenn sich Recompiler-Ausgabe ändert (z. B. neue `[widescreen.cull]`-Sites).
- Im Log erkennt man den Erfolg an `mod selected fixed display aspect 16:9` und `widescreen 16:9 (native-wide, present 1:1; engages at game entry)`.
- Das BIOS-Logo bleibt laut Framework absichtlich 4:3, FMVs sind pillarboxed. Das ist gewollt.

## Cull-Suche: was bisher ausgeschlossen ist

Zum Weiten braucht das Framework exakte Befehlsadressen (`[widescreen.cull]`, siehe `psxrecomp/docs/WIDESCREEN.md`). Alle bisherigen Kandidaten waren falsch.

| Quelle | Ergebnis |
|---|---|
| `psxrecomp-analyze --scan-widescreen` auf die Haupt-EXE | Gefundene Breiten `0x100,0x101,0x103,0x119`, Höhe `0x121`. Das passt zu keinem PSX-Modus, ist also geraten. Bias-/Range-Paare: keine. |
| `0x8014E408`, `0x8014E524`, `0x80163570`, `0x801635F4` (`sltiu …,256`) | Schleifenzähler (Tabelle löschen/kopieren). Kein Cull. |
| `0x80180B08`, `0x80180BF8`, `0x80180D88` (`slti 0x101`) | Liegen in einem Datenbereich, kein Code. |
| `0x80199920` (`slti 0x141`, daneben `addiu 0x140`) | Zähler (+32 bis 320), nie ausgeführt. |
| `0x801D4Exx` (`slti 0x119/0x121/0x161/0x191`) | Setup von GPU-Paketen (Draw-Env). Kein Cull. |
| 14 ausgeführte `bltz` (`0x801A98D8`, `0x801BDD60`, `0x801D2110`, `0x801D5AC4`, `0x801D5B00`, `0x801D5D38`, `0x801D5D70`, `0x801D7628`, `0x801D89C8`, `0x801D89F4`, `0x801D8A1C`, `0x801E009C`, `0x801E4004`, `0x801E6320`) | Stichproben (die ersten vier) sind Index- und Bereichsprüfungen. Nicht jede einzeln geprüft. |
| 10 ausgeführte `ori …,0x8000` (`0x80196E4C`, `0x801A50A4`, `0x801A50E4`, `0x801A6FEC`, `0x801B5C90`, `0x801BE7B8`, `0x801D1A10`, `0x801E6134`, `0x801EEDE0`, `0x801EEE44`) | Stichproben (die ersten sechs) sind Flag-Setzer (Bit 15 als Statusbit). Kein Cull. |
| `sltiu` mit Immediate ab `0x140` unter ausgeführtem Code | **Kein einziger Treffer.** Deshalb erkennt `auto_screen_x` in BoF3 nichts. |

Folgerung: Das Culling hat in BoF3 nicht die Form, die die statischen Muster finden. Weitere Befehlsmuster-Suchen sind wenig sinnvoll.

## Mögliche Ursachen (offen)

1. Polygon- oder Objekt-Cull in Overlay-Code, der anders aufgebaut ist (z. B. Vergleiche über Register statt Immediate).
2. Kein Polygon-Cull, sondern ein Spawn-/Tile-Fenster des Spiels (Objekte werden nur in einem Kamerabereich erzeugt und gelöscht). Das würde das Framework nicht automatisch weiten.
3. Die relevanten Overlays sind noch nicht in den Captures, weil nicht jede Szene gespielt wurde.

## Nächste Schritte (Laufzeit-Messung)

1. **Debug-Build neu bauen**, damit er das Widescreen-Plugin enthält. `build-debugtools/BreathOfFire3.exe` existiert, ist aber älter. Mit demselben `rebuild`-Befehl und `--build-dir build-debugtools` (Debug-Tools und TCP-Server sind dort an). Standard-Port des Debug-Servers: 4370 (`[runtime] debug_port` oder `--debug-port`).
2. **Eine Szene mit sichtbaren Lücken halten**, z. B. den Kampf in der Höhle. Dann per Debug-Client (`psxrecomp/tools/debug_client.py`) arbeiten:
   - `gpu_frame_dump` (siehe `psxrecomp/docs/GPU_FRAME_TOOLS.md`) liefert jedes GP0-Paket mit `func`, `pc`, `ra`. So sieht man, welche Funktion Polygone am Rand zeichnet und welche nicht.
   - `ws_census on|off|<start> <end>` schreibt einen Zeichen-Ring als CSV. Daran sieht man, welche Primitive im aufgedeckten Rand fehlen.
   - `ws_margin <v|-1>` erzwingt den Cull-Rand live (nur wirksam, wo Sites eingetragen sind).
   - `screenshot_wide_hires` und `screenshot_hires` zeigen das tatsächliche Fensterbild. `screenshot` allein zeigt nur das 4:3-VRAM.
3. **Zwei Bilder vergleichen:** Dasselbe Bild einmal mit nahem Kamerarand und einmal nach dem Weiterbewegen. Prüfen, welche Polygone an der Kante erst später auftauchen. Von dort aus mit `ra` zur verwerfenden Funktion zurückgehen (`overlay_xref.py … func <VA>`).
4. Erst wenn die Ursache klar ist, passende `[widescreen.cull]`-Sites (`slti_sites`, `bltz_sites`, `bgez_sites`, `screen_x_sites`, `[[widescreen.cull.sxy]]`, `a1_sites`) eintragen, Spiel-C neu generieren und testen.
5. Außerdem noch ungeprüft: Weltkarte, Städte, Menüs, Dialoge, FMVs. Dort auf HUD-Verzerrung und schwarze Ränder achten (`auto_ui_squash` und `auto_ui_anchor` in `[widescreen]` sind dafür vorgesehen).

## Hilfsmittel

- **Overlay-Captures:** `build-release/overlay_captures.json.d/` (229 Captures, 56 Basisadressen, 25 Dateien). Werkzeug: `psxrecomp/tools/overlay_xref.py -d build-release/overlay_captures.json.d <index|word|dis|func|scan|imm|callers|cover>`. Beispiel: `... scan --op sltiu --imm-min 0x140 --exec-only`. Mit `--exec-only` nur tatsächlich ausgeführten Code anzeigen.
- **Analyzer:** `psxrecomp/recompiler/build/psxrecomp-analyze.exe disc/SLES_013.04 --scan-widescreen` (nur die Haupt-EXE, keine Overlays). Wurde gebaut mit demselben Toolchain-PATH wie oben.
- **Mini-Disassembler (nur Haupt-EXE):** Ein einfaches Python-Skript für MIPS-Befehle lag im Scratchpad; es ist nicht gesichert. `overlay_xref.py dis/func` deckt die Overlays ab.
- **Dokumentation im Framework:** `psxrecomp/docs/WIDESCREEN.md` (Konfiguration, Cull-Sites, Native-wide), `psxrecomp/docs/MOD_PACKAGES.md` (Plugins und Manifest), `psxrecomp/docs/TCP_COMMANDS.md` (Debug-Befehle), `psxrecomp/docs/FUNCTION_DISCOVERY.md` (`--scan-widescreen`), `psxrecomp/docs/GPU_FRAME_TOOLS.md`.
- **Wichtig laut Framework-Regeln:** Generierten Code nie von Hand ändern (er wird vom Recompiler erzeugt). Kein `fprintf`-Debugging, sondern TCP-Debug-Befehle benutzen. Das steht in `psxrecomp/CLAUDE.md`.

## Rahmenbedingungen

- Der Nutzer beurteilt das Bild selbst, Claude kann die Darstellung nicht sehen. Nach jeder Änderung braucht es eine Rückmeldung zum Bild.
- Das Projekt ist kein Git-Repository. Vor größeren Änderungen eine Sicherung von `game.toml` und `CMakeLists.txt` anlegen.
- Die Disc liegt unter `C:\Discs\BOF3\Breath of Fire III (Europe).cue`.

## Update 2026-11-20 (spät): Lücken behoben

- Ursache: Bildschirm-X-Culls im **Haupt-EXE** (`lhu SX; addiu +Bias; andi 0xFFFF; sltiu W`), nicht in Overlays. Die frühere Suche hatte nur Overlays abgedeckt.
- Fix: `[widescreen.cull] screen_x_sites` in `game.toml` mit 0x8014C73C, 0x80153668, 0x80156344, 0x8015656C, 0x80156810, 0x80157CC4. Spiel-C neu generiert, Rebuild fertig. Der Nutzer bestätigt: im Kampf (Mine) sind die Lücken weg.
- Debug-Build: `rebuild ... --build-dir build-debugtools --no-pgo --cmake-extra=-DPSX_DEBUG_TOOLS=ON` (sonst ist der GP0-Ring leer). Start mit `PSX_DEBUG_SERVER=1 ./BreathOfFire3.exe --debug-port 4370`.
- Noch offen: Weltkarte, Städte, Menüs, Dialoge, FMVs prüfen (HUD-Verzerrung, Ränder). Falls dort Pop-in auftritt, im Haupt-EXE weitere SX-Vergleiche suchen.
