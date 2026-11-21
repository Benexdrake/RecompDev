# RecompDev – PSX-Recomp-Projekte

Der Nutzer schreibt Deutsch: Antworten auf Deutsch. Stand: 2026-11-21.

Projekte (alle mit gemeinsamem `psxrecomp/`-Framework im jeweiligen Projektordner):

| Projekt | Ordner | Serial | Stand |
|---|---|---|---|
| Alundra (DE) | `alundra-recomp` | SLES-01256 | 16:9, HUD-Ecken, Wolken, weicher Kartenrand fertig |
| Breath of Fire III | `bof3-recomp` | SLES-01304 | 16:9 fertig, bestätigt |
| Breath of Fire IV (EU) | `bof4-recomp` | SLES-03552 | gebaut, ungetestet, kein Widescreen |
| Legend of Dragoon (DE, 4 CDs) | `lod-recomp` | SCES-03045 | 16:9 im Kampf fertig |

Projekt-Memory (Status, Erkenntnisse): `docs/memory/` (Index `MEMORY.md`), neue Erkenntnisse dort ablegen.

Weitere Doku in `docs/`: `ALUNDRA_WIDESCREEN_HANDOFF.md`, `BREATH_OF_FIRE_3_WIDESCREEN_HANDOFF.md`, `PAL_ZU_60HZ.md`, `PSX_SPIEL_PORTIEREN.md`, `alundra-dialogbox-plan.md`.

## Gemeinsamer Workflow

**Build** (Git Bash). Toolchain auf den PATH, dann:
```
export PATH="$HOME/.local/share/retcomm/toolchains/cmake-clang-v1/1.0.14/bin:$PATH"
python psxrecomp/psxrecomp_cli.py rebuild --config game.toml --project-root . --build-dir build-release --no-pgo
```
- Debug-Build: `--build-dir build-debugtools --cmake-extra=-DPSX_DEBUG_TOOLS=ON` (ohne den Extra bleibt das GPU-Ring leer, `gpu_frame_dump` liefert nichts).
- Vor dem Rebuild `taskkill //F //IM <Spiel>.exe`.
- "Generate failed" nach "Generate complete" ist harmlos.
- **Neue Hook-Sites** (`[recompiler] mod_instruction_sites` in `game.toml`, `[widescreen.cull]` usw.) brauchen `generate`; ein Rebuild allein ignoriert sie stillschweigend. Das dauert einige Minuten, bei BoF3 über 10 Minuten. Reine Plugin-Änderungen brauchen nur einen Rebuild (~2 Minuten).
- Neues Plugin: in `CMakeLists.txt` per `target_sources(psx-runtime PRIVATE .../mods/xyz.c)` eintragen. Features und Plugins stehen im Manifest `mods/preloaded/packages/<id>/1.0.0/manifest.toml`.
- Instruction-Hook: `psx_mod_register_instruction_plugin(id, adresse, instruktionswort, fn)`. Läuft direkt vor der Instruktion, das Wort muss mit dem RAM übereinstimmen. Kann Register und Daten ändern, aber den PC nicht umlenken.
- Features lassen sich in `build-*/mods/state.toml` ausschalten: `[[feature]]` mit `id = ...` und `enabled = false`.

**Debug-Workflow:** `cd build-debugtools; PSX_DEBUG_SERVER=1 ./<Spiel>.exe --debug-port 4370`. Der Server steht nach ~15 s, der Nutzer lädt den Spielstand von Hand. Client: `python psxrecomp/tools/debug_client.py <cmd> k=v`.
- `gpu_ring_stats` (newest_frame), `gpu_frame_dump frame=N` (Einträge mit op/src/ot/w; abwechselnde Frames können leer sein), `screenshot_wide_hires path=...` (per Read ansehbar), `screenshot_file` (4:3 nativ), `vram_peek x= y= w= h=`, `read addr len`, `disasm addr= count=` (Hauptprogramm-Code, JSON mit `lines[].text`).
- `wtrace_add lo hi` / `wtrace` / `wtrace_del 0`: Write-Trace, Ring nur 256 Einträge, nach Adresse filtern, zuerst die alten Boot-Watches löschen. Runtime-interne Schreibzugriffe werden nicht getrackt.
- Keine riesigen Ausgaben ausgeben (Zähler statt Listen).
- 4:3 zum Vergleich: Feature `widescreen` per `state.toml` abschalten (Original als `state.toml.orig` sichern).

**CHD-Discs:** kein `chdman`. libchdr bauen (`ninja chdr` in `psxrecomp/recompiler/build`), dann `python tools/psx_chd.py <chd> --extract <dir> --no-hash` bzw. auf `.cue` + `.bin` umwandeln. `setup_project.ps1` prüft nur `.cue`. Nicht zwei `setup_project.ps1` parallel laufen lassen, mit `-ExecutionPolicy Bypass` und `-NoBuild` starten.

**PAL → 60 Hz:** `psx_video_timing.c` erzwingt in allen vier Projekten standardmäßig NTSC-60-Hz-Timing. `PSX_FORCE_60HZ=0` stellt 50 Hz wieder her. Das Spiel läuft dadurch ~20 % schneller (so gewollt). Doku: `docs/PAL_ZU_60HZ.md`. Debug-Builds wurden dafür nicht neu gebaut.

**Widescreen-Grundlagen:**
- Der Runtime erzwingt 4:3 aus der toml. Nur ein vertrauenswürdiges Mod-Plugin kann mit `psx_mod_set_fixed_display_aspect(16, 9)` 16:9 aktivieren (Manifest `format_version = 11`).
- 3D-Spiele: `[widescreen] gte_game_mode = true` plus Cull-Sites. 2D-Spiele: `full_2d = true`, NICHT `gte_game_mode`.
- Cull-Sites für Bildschirm-X im Hauptprogramm suchen, nicht nur in Overlay-Captures.
- Für 2D-PSX-Spiele: Kachel- oder Cull-Schleife per `wtrace` auf ein Kachelpaket finden. Schleifen auf die Kartenbreite begrenzen statt Randspalten zu klonen. Wenn ein Grafikfehler nur in 16:9 auftritt, Pakete von 4:3 und 16:9 bei gleicher Kamera vergleichen und RAM-Tabellen prüfen, bevor man die Hooks verdächtigt.

---

## Alundra (`alundra-recomp`)

Release: `build-release\Alundra.exe`, Debug: `build-debugtools\Alundra.exe`. Beide enthalten alle Funktionen unten (Stand 2026-11-21 16:02). Disc: `C:\RecompDev\Alundra (DE).chd`, umgewandelt nach `C:\Discs\Alundra\Alundra.cue` + `game.bin`. Boot `SLES_012.56`, Entry 0x800360F4. Das Disc-File `SLES_012.56` stimmt NICHT mit dem RAM zur Laufzeit überein, nicht für statische Lookups nutzen. Statischer Code liegt in `build-debugtools/cache/tmp/*/out/overlay_8002A000.psx_full.c` (`generated/SLES_012.56_full_*.c` ist falsch). Ältere Details: `docs/ALUNDRA_WIDESCREEN_HANDOFF.md`.

Code: `mods/alundra_widescreen.c` (Widescreen, Feature `widescreen`, Plugin `alundra.widescreen`), `mods/alundra_hud.c` (HUD, Feature `hud_corners`, Plugin `alundra.hud`). Backups: `mods/alundra_widescreen.c.pre_diag`, `.bak2`.

**Ungetestet:** Sprite-/Objekt-Pop-in, Menüs, Dialoge mit neuem HUD, FMV, Audio, Save/Load, Kantenquad auf anderen Karten. Innenräume haben evtl. andere Kartenbreite als 52 (`ALU_MAP_COLS` ist fest 52). Das Release-Exe hing einmal beim ersten Start (kein Fenster, 0 % CPU, Debug startete normal), noch einmal prüfen.

### 16:9 Kacheln
Reines 2D-Kachelspiel, also `full_2d = true`. Kachelschleife im Hauptprogramm 0x8002CE..0x8002D440 (24x16-Sprites, Befehl 0x65, jetzt 21 Spalten, private X-Tabelle in Expansion-1-Mod-Speicher), verbreitert über Instruction-Hooks. `gpu` Debug zeigt `ws.active 0` auch wenn es klappt; `present_native_43` prüfen (0 = 16:9). Kachelpuffer: s0 = 0x800DD878 + 13600*Parität, 12000 B (600 Pakete à 20 B). Paketlayout: base = ptr-13, +4..6 rgb, +7 cmd, +8 x s16, +10 y, +12 u, +13 v, +14 clut. Kacheln werden zeilenweise per Head-Insert in OT-Slots eingetragen, OT-Basis bei sp+0x58.

Nützliche Adressen: Kamera X/Y 0x800E4328/32C, Karten-Zeilenbasis-Pointer 0x800DD86C (Einträge 8 B, Zeilen 416 B, 60 Zeilen, Extras-Pool bei ptr+26500), Farbpalettentabelle-Pointer 0x800E4320, Kachel-Frame-Tabelle 0x800E42F0 (7 B pro Seite).

### Kartenrand
Karte 52 Spalten breit (Kamera X max 927). Spaltenzahl in den Hooks 0x8002CED0 / 0x8002CF04 wird auf `52 - first_col` begrenzt, jenseits des Rands ist es schwarz (bestätigt). Vom Nutzer abgelehnt: Randspalte klonen (Streifen) und Klon per Sprite-Modulation ausblenden. Sites 0x8002D150 / 0x8002D220 / 0x8002D390 stehen noch in `mod_instruction_sites` (für Paket-Hooks ohne Regen nutzbar; bei der nächsten Regen entfernen, wenn unbenutzt).

### Weicher Kartenrand (fertig, bestätigt)
Pro Kartenseite ein Gouraud-Semitrans-Quad (cmd 0x3A, davor E1 0xE1000040, subtraktiv B-F), Breite `ALU_EDGE_W` = 28 px, Farbe 0xFF am Rand → 0 nach innen, y 0..240. Hook `alundra_after_tiles` auf Site 0x8002D444. Quad wird in OT-Slot 959 head-eingefügt (über der Welt, unter Wolken und HUD). Pakete (2 x 64 B) in 128-B-`psx_mod_alloc_gpu_dma_memory`-Arena, jeden Frame neu geschrieben. Kartenrand-Bildschirm-X = -camX (links) bzw. 52*24-camX (rechts), Quad wird übersprungen, wenn außerhalb des Bildes. Die alte gestufte Kachelmodulation ist über `ALU_EDGE_TILE_SHADE 0` aus (Nutzer fand die Stufen hässlich). Stellschrauben: `ALU_EDGE_W`, `ALU_EDGE_DARK`, `ALU_EDGE_SLOT`.

### Wolken/Schatten-Overlay (fertig, bestätigt)
Verbreitert über Hooks 0x8005C538 / 0x8005C5F4 / 0x8005C4E8 in eine 28-KB-GPU-DMA-Arena (Makro `ALU_CLOUD_WIDEN 1`, 0 schaltet Arena und Hooks ab). Originalpuffer: zwei Display-Buffer 0x80187A58 / 0x8018A4D8 (5440 B pro Layer), Auswahl per Flag 0x8018CF5C, Pointer-Ablage 0x80181BE0 durch 0x8005C8B8.

### Speicher-/Laderaum-Wolken (fertig, flackerfrei bestätigt)
Diese Szene nutzt NICHT die Routine 0x8005C294 (Overlay nicht geladen, die Hooks oben sind dort irrelevant). Der Nebel besteht aus 6 Semitrans-Sprite-Streifen (cmd 0x66, 64x128, y=0x78, Texturperiode 320 px = 5 Streifen, k=0..4, Streifen k=4 auf Texpage E1 0x1D, die anderen 0x1C), gezeichnet über die generische Objektzeichenfunktion im Hauptprogramm (Schreibzugriffe 0x80025FFC..0x80026048, 20-B-Pakete in zwei Puffern 0x801572D0 / 0x80159550, E1-Paket s1 separat). Originale sind immer 6 aufeinanderfolgende Streifen x_l+64i mit x_l in [-64,0), deckten also nur 4:3 ab. Fix: Hook `alundra_cloud_strip` auf Site 0x800262EC (Wort 0x8FBF008C, direkt nach dem letzten OT-Link; fp = Objekt, s0 = Sprite-Paket, s1 = E1-Paket, OT-Basis bei 0x8015AE90, Slot = fp.s16[4]*4+0x70, nur wenn fp+8 == -1) fügt um ±320 px verschobene Kopien für Streifen mit 0<=x<64 (Kopie bei x+320) und 192<x<256 (Kopie bei x-320) hinzu, nur wenn sichtbar (View-Margin). Erste Version mit x<=64 / x<=256 doppelte einen Streifen einen Frame pro ~3,5 s (Flackern am Rand). Der Kantenquad wird in diesem Raum nicht gezeigt (nicht nötig).

### HUD in Bildschirmecken (fertig, bestätigt "Sehr gut", 2026-11-21)
Eigenes schaltbares Feature `hud_corners` (Plugin `alundra.hud`, Datei `mods/alundra_hud.c`, Manifest `mods/preloaded/packages/alundra.enhancement.widescreen/1.0.0/manifest.toml`, Eintrag in `CMakeLists.txt`). Sites in `game.toml`: 0x8004C0C0 (pre, Wort 0x00003021) und 0x8004C220 (post, Wort 0x8E03827C).
- HUD-Pakete liegen in einem statischen GPU-Puffer 0x80175D00..0x80176700 (zwei Paritäten, OT-Slots 0..4), gebaut jeden Frame von der Routine bei ~0x8004C0C0 aus der HUD-Basis (0x800A8258 x, 0x800A825A y; = 0,16).
- Post-Hook scannt den Puffer (0x65/0x64-Sprites mit n=4, 0x3B-Quads mit n=8) und verschiebt nach Gruppe anhand des Original-x: x<0x70 Item-Slots → linker Rand, y+176 (unten); 0x70<=x<0xF0 Herzen und "10/10"-Glyphen → x-104-Margin, oben; x>=0xF0 Gilder → x+Margin, y+192 (rechts unten).
- Pre-Hook (und Anfang des Post-Hooks) macht die Verschiebung pro Paket über eine Record-Tabelle rückgängig, nur wenn Vertex 0 noch den verschobenen Wert hat.
- Bug (behoben): Die Glyphenpakete von "/10" werden nicht jeden Frame vom Spiel neu geschrieben. Das Zurücksetzen muss wertgenau sein, sonst werden sie doppelt verschoben (landeten dann unten links bei den Items).
- Menü-Slide (2026-11-21, bestätigt): Beim Öffnen des Start-Menüs gleitet die HUD-Basis (0x800A825A) von 16 nach -41. Post-Hook blendet das HUD aus (dy -400), solange die Basis-Y != 0x10 ist, sonst erschien es kurz doppelt.
- 10-HP-Stein (fertig, bestätigt, 2026-11-21): Das Spiel fasst 10 HP zu einem großen Stein zusammen (Sprite 0x65, u=96 v=40, clut 31186). Er sitzt oben links über den kleinen HP-Punkten (`ALU_HUD_STONE_Y`), die "/N"-Glyphen (clut 31058, x<0xF0) sind ausgeblendet. Erkennung über die Textur, nicht über die Position.
- **Startzustand-Falle:** Bis zum ersten Start-Menü schreibt das Spiel HUD-Pakete an anderen Positionen (Stein bei 51,192; 6. Herz-Spalte und "/N" bei x=3). Das war schon zweimal die Ursache für Fehlplatzierungen. HUD immer frisch testen (neu starten, laden, Start NICHT drücken), Pakete per Textur erkennen. Details in `docs/memory/alundra-hud-stein-startzustand.md`.
- Schalter: `build-*/mods/state.toml`, `[[feature]] id = "hud_corners"`, `enabled = false`. Der Schalter selbst ist noch nicht getestet. Menüs und Dialoge mit dem HUD ungetestet.

### Grüne-Blöcke-Bug (gelöst, Ursache unklar, 2026-11-21)
Dunkelgrüne 24x16-Blöcke in Baumkronen. Ursache: Kachel-Tabelleneinträge (Page, u, v bei 0x800DCD28 + id*3; IDs 0x4f und 0xA4 bei 0x800DCE15 / 0x800DCF14) wurden in u/v überschrieben durch `SH 1` des OT-Flag-Arrays des Spiels (0x800DC5A8 + a2*2, 960 Einträge), das über sein Ende hinaus indiziert. NICHT durch die Kachel- oder Wolken-Hooks verursacht (per Abschalten verifiziert), trat nur in manchen Läufen auf (evtl. Lade-Race oder alter automatisch gespeicherter Debug-Zustand). Schnelltest: `read 0x800DCF10 8` → `0001480001600001` korrekt, `...0100...` kaputt. Falls es wiederkommt: herausfinden, wer ins Flag-Array schreibt (Index >960 heißt Page-Byte 255 oder Zeile >59).

### Debug-Hinweise Alundra
- Wenn `gpu_frame_dump` nur ~50 Einträge pro Frame zeigt, sind das trotzdem die echten Pakete. Den Schreiber per `wtrace_add` auf die Paketadressen finden (Paketadressen per RAM-Scan in 64-KB-Blöcken über 2 MB finden).
- Im Dump hat jeder Eintrag `ot` (OT-Slot); Welt liegt in Slots ~721..954, HUD in 0..4. `pc` im Dump ist nur der DMA-Walker, nicht der Schreiber.
- Wenn eine Packet-Position nach einem Hook "driftet", prüfen, ob die Routine das Paket wirklich jeden Frame neu schreibt.

### Kantenquad dunkle Kacheln + Spielstand-Ladezeit (fertig, bestätigt, 2026-11-21)
- Kantenquad: `alundra_tiles_overlap` ignoriert rgb-0-Sprites und verlangt >=2 verschiedene helle Kacheln (clut|v|u) in der Quadzone, sonst kein Quad (schwarzer Balken in Raum mit Kamera X=0 weg). Ungetestet: Außenrand mit einheitlichem Gras.
- Spielstand laden: Das BIOS liest die ganze Memory Card sektorweise (~34 ms/Sektor, 2 Vblanks). Framework-Fix: `g_psx_card_read_activity` (`sio.c`) hält in `main.cpp` Turbo (`turbo_loads_active`) an, solange Sektoren gelesen werden. Gilt für alle Projekte nach Rebuild. Release + Debug gebaut.
- Profiling-Hilfe: `psxrecomp/tools/host_profile.py --port 4370 --exe <exe> --since SEQ` (Host-Sampler, SEQ ~ ms seit Start). Der Debug-Befehl `pc` existiert nicht.

### Ring-/Lichtmaske gestreckt (fertig, bestätigt, 2026-11-21)
Overlay aus 120 0x67-Streifen (4 px hoch) wird per Hook `alundra_mask_stretch` (Site 0x8005D5E0) durch um 4/3 gestreckte Quads ersetzt. Details: `docs/memory/alundra-ring-maske-stretch.md`.

### Offene Idee
`docs/alundra-dialogbox-plan.md`: Sprechboxen durch eigene Grafik und TTF-Text ersetzen (nur Plan, nichts implementiert).

---

## Breath of Fire III (`bof3-recomp`)

SLES-01304, 16:9 läuft (Kampf + Feld vom Nutzer bestätigt, 2026-11-20). Randlücken (schwarze Keile) behoben. Doku: `docs/BREATH_OF_FIRE_3_WIDESCREEN_HANDOFF.md`.
- `mods/bof3_widescreen.c` setzt 16:9, `game.toml`: `[widescreen] gte_game_mode = true`. Der Analyzer-`auto_screen_x` greift nicht, weil BoF3 die gepaarte `sltiu 0x140/0xE0`-Form nicht nutzt.
- Das Hauptprogramm hat Objekt-/Kachel-SX-Culls (`lhu SX; addiu +bias; andi 0xFFFF; sltiu W`, jeweils mit Y-Test gepaart): 0x8014C73C, 0x80153668, 0x80156344, 0x8015656C, 0x80156810, 0x80157CC4 (Fenster ~[-50..370], schmaler als 16:9 mit ~-53..373). Eingetragen in `game.toml` `[widescreen.cull] screen_x_sites`, Regen + Rebuild erledigt.
- Die Y-gepaarten `sltiu` bei 0x8014C758, 0x80153688, 0x80156360, 0x80156588, 0x80157CE4 sind NICHT X.
- Falls weitere Lücken: Hauptprogramm (`disc/SLES_013.04`, Text bei 0x80096800, Dateioffset 0x800) nach weiteren SX-Vergleichen (slti/sltiu mit anderen Immediates, bltz-Ketten) und RTP4/RTPT-Aufrufern (0x80156xxx-0x801581xx Kachelrenderer) absuchen.
- `ws_census` nimmt Positionsargumente (start end file). Backups: `game.toml.bak`, `CMakeLists.txt.bak`.
- Ungetestet: Weltkarte, Städte, Menüs, FMVs.

## Breath of Fire IV (`bof4-recomp`)
SLES-03552, Boot `SLES_035.52`, Entry 0x80136DA0, `build-release\BreathOfFire4.exe`, Disc `C:\Discs\BOF4\*.cue` (2 Tracks). Eingerichtet und gebaut am 2026-11-20, ungetestet, kein 16:9. 3D-Spiel: als nächstes gte_game_mode + Mod für festes Seitenverhältnis + screen_x-Cull-Sites wie bei BoF3.

## Legend of Dragoon (`lod-recomp`)
SCES-03045 (CD 2-4: SCES-13045/23045/33045), Boot `SCES_030.45`, Ladeadresse 0x80188888, Entry 0x801C0620, nur 73 Seeds (overlay-lastig, evtl. Seed-Arbeit nötig), `build-release\LegendOfDragoon.exe`. Discs in `C:\Discs\LOD\D1..D4`, `game.toml` hat von Hand `discs` + `disc_serials` (Schrägstriche, LF-Zeilenenden).
- 16:9 im Kampf bestätigt (2026-11-20), Randpolygon-Pop-in behoben: `mods/lod_widescreen.c` (setzt nur 16:9) + Manifest + `[widescreen] gte_game_mode` + `[widescreen.cull] slti_sites` (39x `slti x,193`) / `slti_lower_sites` (40x `slti x,-192`) im Kampf-Overlay 0x800CC..0x800DE (per `overlay_xref.py` über Captures gefunden). LoD zeichnet mit Zentrums-Ursprung, 384 breit, daher ±192. Overlay-Sites brauchen keine Spiel-Regen.
- Feldszenen: vorgerenderte scrollende Hintergrundstreifen (4-6 Kacheln à 128x256) bleiben 4:3 breit, schwarze Seitenränder bleiben (Nutzer wollte es so lassen). Stretch-Versuch (Kacheln per `gpu_ws_tag_background_prim` in einem List-Kick-Hook) füllte die Breite, erzeugte aber cyanfarbene CLUT-Artefakte; Referenzkopie `lod-recomp/analysis/lod_widescreen_backdrop_stretch.c.txt`.
- Ungetestet: Weltkarte, Städte, Menüs, FMV.
