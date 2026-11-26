# Terranigma (SNES) – 16:9 Widescreen, Stand 2026-11-26

Projekt `terranigma-recomp`, Framework `snesrecomp/`. Nur Debug-Build getestet. Das ist ein früher Stand: Menü bestätigt, Spielwelt noch nicht untersucht.

## Der Mod (Paket `terranigma.widescreen`, Feature `widescreen`)
Kein PSX-artiger Instruction-Hook-Mod. Der SNES-Host rendert den Frame im PPU breiter, die Spielsimulation bleibt 256 px breit. Das Feature ist `presentation_only` und per Launcher (Mods-Seite) schaltbar, Standard **an**.

Dateien:
- `mods/preloaded/packages/terranigma.widescreen/1.0.0/manifest.toml`: Paket, Ziel `terranigma-deu` + ROM-SHA256, Feature, Option `edge_policy` (clamp Standard / natural / mirror / repeat), Plugin `terranigma.widescreen`.
- `src/terranigma_widescreen.c/.h`: Plugin (`snes_mod_register_presentation_plugin`, Reset-Callback). `TerraWsFrameWidth()` liefert 398 (aktiv) oder 256, `TerraWsApplyPolicy(ppu)` setzt die Randpolitik für BG1-3 (Maske 0x07). In `CMakeLists.txt` unter `add_executable` eingetragen.
- `src/main.c`: `native_widescreen = 1`, `prepare_frame` nimmt die Breite vom Mod (398 = 224 * 16/9, 71 Zusatzspalten pro Seite).
- `src/game_rtl.c` (`GameDrawPpuFrame`): ruft `TerraWsApplyPolicy(g_ppu)` jeden Frame. `PreparePpuFrame` setzt vorher `PpuSetExtraSpace`, das die Policies zurücksetzt, daher muss es jeden Frame sein.
- Testschalter `TERRA_WS=natural|mirror|repeat|clamp` (Umgebungsvariable vor dem Start) überschreibt die Option.
- Änderungen am Mod brauchen einen Rebuild; Feature-Wechsel im Launcher wirken nach Neustart.
- Weitere Framework-Werkzeuge für später: `PpuSetWidescreenLayerClampBand` / `RepeatBand` / `AnchorBand` / `ElasticBand` (pro Zeilenband), `PpuSetExtraSideSpace` (dynamische Ränder), `PpuSetWidescreenViewAnchor`, `PpuSetWidescreenHudSplit`. Checkliste P1-P16: `snesrecomp/docs/WIDESCREEN_PATTERNS.md`. Dort neue Politik/Hooks in `terranigma_widescreen.c` ergänzen, Culling-Hooks (`mod_hook`, `snesrecomp/docs/MOD_HOOK.md`) kommen in dieselbe Datei.

## Ergebnisse
| Szene | Politik | Ergebnis |
|---|---|---|
| Datei-Menü (NEU / KOPIEREN / LÖSCHEN) | `natural` | Falsche Holztextur an den Rändern (Tilemap-Wrap holt Kacheln von der Gegenseite) |
| Datei-Menü | `mirror` | Text seitenverkehrt links und rechts, schlecht |
| Datei-Menü | `clamp` | **sauber**, Tafel mittig, Ränder nur dunkler Hintergrund (bestätigt) |
| Spielwelt (Dorf, Überwelt, Gegner, HUD) | – | noch nicht getestet |

Vermutung: Menüs wollen `clamp`, die Spielwelt `natural` (echte Kartenkacheln). Wahrscheinlich Umschaltung je Szene nötig; dafür fehlt noch ein Spielzustands-Byte (Modus, Menü/Welt). Per `set_wram_watch` suchen (P5/P6).

## Noch zu tun
1. Spielwelt ansehen, Politik pro Szene wählen (Menü/Titel/Welt/Weltkarte/Intro).
2. Sprite-Culling im generierten Code und OAM-Emitter verbreitern (P7/P8), sonst verschwinden Objekte an der alten 4:3-Kante.
3. Ränder der Karte aus Level-Daten vorbefüllen (P2), Kartenrand-Verhalten.
4. HUD verankern, Fades, Mode-7-Szenen prüfen.
5. P16-Gate: 4:3-Frames mit und ohne Widescreen vergleichen.

## Änderungen im Submodul `snesrecomp` (nur Working Tree, nicht committet)
- `runner/src/snes/ppu.c`/`.h`: `g_snes_ppu_report_pal` (PAL-Region-Fix, `$213F` Bit 4), gesetzt in `GameInitialize()`.
- `runner/src/snes/ppu.c`, `ppu_read`: Zweig `default` gibt 0 zurück statt `assert(0)`. Terranigma liest ein Write-Only-Register (Open Bus), das Debug-Build brach sonst ab. Release war nie betroffen.

## Build und Debug
```
cmake -S . -B build -G "Visual Studio 18 2026" -A x64 -DSNESRECOMP_ENABLE_TRACE=ON
cmake --build build --config Debug --parallel
```
- Ohne `-DSNESRECOMP_ENABLE_TRACE=ON` ist der **Debug-Server nicht im Build** (Port 4377 bleibt zu). Mit ON läuft er automatisch (ohne Netplay), kein Startparameter nötig.
- Start mit Randpolitik-Override: `$env:TERRA_WS="clamp"; .\build\Debug\TerranigmaSNESRecomp.exe` (Arbeitsverzeichnis `build\Debug`).
- Screenshot (398x224 aus dem PPU, BMP): in `snesrecomp/tools`: `python -c "from sneslib.client import DebugClient; print(DebugClient(4377).query('screenshot <pfad>.bmp'))"`. Zum Ansehen BMP in PNG wandeln (kein PIL installiert, eigenes Skript nötig). Befehle `ping`, `step`, `set_wram_watch` u. a.: `snesrecomp/docs/DEBUG_ROUTES.md`.
- Vor dem Rebuild `Get-Process TerranigmaSNESRecomp | Stop-Process`.

## Spielwelt-Untersuchung (2026-11-26, Abend)
- **BG3** (Mode 1, TM=0x16 = BG2+BG3+OBJ in Dorfszene, BG1 aus) hat einen dunklen 8-px-Rand an den alten 4:3-Kanten: das sind die schwarzen Streifen. Test mit `SNESRECOMP_LAYER_MASK=0x13` (BG3 aus). Windows sind nicht beteiligt (`windowsel` 0). Fix steht aus.
- **BG2 = Welt**, Tilemap 32x32 (`bgXsc[1]=0x38`), PPU-Scroll ist Weltposition (10 Bit). Das Spiel streamt pro 8 px Scroll **eine Spalte (32 Kacheln) an der nativen Vorderkante**, Staging-Puffer WRAM `$7E:4000` (64 B), Schreiber laeuft im NMI (`interp@$868009/$86800D`, Bank $86). Ein Debug-PC ist im Interpreter nicht verfuegbar (`func` zeigt nur den Einstieg).
- `TerraWsApplyPolicy` (Policy `natural`) nutzt jetzt den Welt-Shadow fuer BG2 (`WsShadowSetWorld/SetScroll/RetainHistory`, West/EastKeep 12). Ergebnis: bereits besuchte Raender stimmen, Vorderkante (Neuland) zeigt gewrappten VRAM. Rest = P2: Zusatzspalten aus Kartendaten vorbefuellen (`WsShadowPrefillTile`), Kartenquelle/-format noch unbekannt (Spalte ist aus Metatiles abgeleitet, im WRAM nicht direkt als Karte auffindbar).
- Sprites (OBJ) erscheinen in den Raendern korrekt (Blasen).
- Werkzeuge: `tools`-Disassembler in der Session (65816, nicht im Repo), Debug-Befehle `trace_vram`, `wram_writes_at`, `watch_add`/`watch_clear`/`continue`, `get_vram_trace nostack`.

## Ergebnis Spielwelt (2026-11-26, Nutzer bestaetigt, `TERRA_WS=natural`)
Welt links/rechts, Kartenrand, Raeume und NPCs ausserhalb 4:3 funktionieren. Umsetzung (Weltkarte-Provider, Randregeln, Cull-Hooks `$00:EB41/EB4C` und `$ECBA/$ED21/$EEA3/$EF2E/$EFBB/$F048`, Raum-Modus) steht in `docs/memory/terranigma-widescreen-status.md`. Offen: BG3-Randstreifen im Normalbetrieb, Weltkarte/Intro/Titel/Mode7/HUD, `natural` als Standard setzen, Release-Build.
