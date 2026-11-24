# Alundra USA (SLUS-00553) – Übergabe

Stand: 2026-11-24 (abends). Branch `usa-slus-00553` in `alundra-recomp` (abgezweigt von `main`, noch nichts committet).

## Ergebnis bisher

- Die USA-Version bootet im **Debug-Build** (`build-debugtools\Alundra.exe`). Intro läuft, getestet bis zur Kars-/Melzas-Szene.
- **16:9 läuft** für: Kacheln, Wolken/Schatten-Overlay (Bootsszene), Pillarbox (Kars-Szene) und Ringmaske/Nebel-Vignette (Kars-Szene). Jeweils per Screenshot im Debug-Build geprüft. Details und Adressen unten.
- **Noch nicht portiert:** Kartenrand/Kantenquad, Speicher-/Laderaum-Nebel, HUD in den Ecken, Mine/dunkle Räume (inkl. Raumfarben, `bgcolor`, Dunkelraum-Zähler der Wolken). Die zugehörigen DE-Hooks (`alundra_hud.c`, `alundra_edgefade.c`, `alundra_bgcolor.c`, Rest von `alundra_widescreen.c`) sind im Build, greifen aber nicht, weil ihre Sites nicht in `mod_instruction_sites` stehen. Sie rechnen mit DE-Adressen.
- Nicht getestet: alles nach dem Intro (Titel, Spielstart, Menüs, Speichern, FMV, Audio), andere Szenen mit Wolken. Release-Build nicht gebaut.

## Portierte Features (US-Adressen)

`mod_instruction_sites` in `game.toml` (alle als Strings): `0x8002D1CC 0x8002D204 0x8002D1EC 0x8002D2F0 0x8002D4B0 0x8002D778 0x8005E6B0 0x8005E6F8 0x8005E7B8 0x8002D7A4 0x8005F784 0x8002E150`. Hooks in `mods/alundra_widescreen.c` (`alundra_us_*`) und `mods/alundra_pillarbox.c`.

| Feature | Sites | Besonderheiten gegenüber DE |
|---|---|---|
| 16:9-Kacheln (Routine ~0x8002D0C0..0x8002D7A4) | 0x8002D1CC / 0x8002D204 (Spaltenzahl 15/14), 0x8002D1EC (erste Spalte), 0x8002D2F0 (Kachelpuffer-Arena, ersetzt zugleich den Überlauf-Fix), 0x8002D4B0 (X-Tabelle -> privat), 0x8002D778 (Schleifenende) | Spaltenzahl in **s3** (nicht t8), X-Tabelle in **t6** (0x800203F0), Schleifenende vergleicht gegen Original-Tabelle + 2*Spalten (Wort 0x01C2102A, Hook rechnet auf die private Tabelle um). US-Kachelpuffer 0x801D0FF8 + 13600*Parität |
| Wolken/Schatten (Routine 0x8005E488..0x8005E804) | 0x8005E6B0 (Arena, Layer-Index in **s2**), 0x8005E6F8 (Zeilenstart: a3 -= 4 mit Wrap 40, t1 = -64), 0x8005E7B8 (Schleifenende t1 < 416) | 21 -> 30 Spalten. Ohne Dunkelraum-Erkennung (`g_cl_hide`, Randzähler) |
| Pillarbox (Kars-/Melzas-Szene) | 0x8002D7A4 (Wort 0x0000C021) | OT-Basis in **fp** (DE: sp+0x58). Raum-Hashes identisch zu DE (`0xB3BDE1C5` / `0xE93D8AA1`) |
| Tor-Schatten (bestätigt 2026-11-24) | 0x8002E150 (Wort 0x8D430000, t2/t6/a2 wie DE) | Definitionen `ALU_SHADOW_T6_PLAYER` 0x800CC928 / `ALU_SHADOW_T6_GATE` 0x800CC948 (DE 0x800E4D30 / 0x800E4D50). Hook `alundra_shadow_part` |
| Ringmaske / Nebel-Vignette | 0x8005F784 (JR ra; a2 = Sprite, t4 = OT-Slot) | Texpage fest 0x3D (DE: Tabelle). Streifen-Routine 0x8005F5C8, Aufrufer 0x8005ECB8 |

**Wichtig:** `mods/alundra_common.h` ist auf US umgestellt (Karten-Zeiger `ALU_MAP_ROWS_PTR` 0x801AC6C4, Kamera X/Y 0x801EF434 / 0x801EF438; DE-Werte stehen im Kommentar). Der DE-Stand ist damit nur noch auf `main` korrekt. Die Karten- und Raumdaten selbst sind in US und DE identisch (gleiche Raum-Hashes), nur Code und Variablenadressen unterscheiden sich. Die DE-Raumfarben und -Hashes sind daher vermutlich weitgehend übertragbar.

**Hintergrund (Spiel-Clear):** funktioniert ohne Mod. Nutzer sieht die Farbe als etwa (8,0,0); der Standardwert `g_alu_clear_rgb` in `alundra_bgcolor.c` ist 0x00000008 (R=8). Nicht per Pixelwert geprüft.

## Die Disc

Quelle: `C:\Users\BeneX Drake\Downloads\Alundra - Definitive Edition v4 (USA)\...` (Fan-Patch auf die US-Version, 565 580 736 Byte, 1 Track MODE2/2352). Dieses Original bleibt unverändert.

Aufbau der Disc:
- `SYSTEM.CNF` bootet `EPIX.EXE` (45 KB, Load 0x80010000, Entry 0x80017A54). Das ist ein Lader mit Menü. Laut `PROGRAMS.TXT` startet er `EASY_005.53`, `HARD_005.53`, `DEBUG.EXE`, `INTRO.EXE` und `END.EXE`.
- Das Spiel selbst: `EASY_005.53` und `HARD_005.53` (je 1 241 088 Byte), Load 0x80020000, **Entry 0x80036044**, text_size 0x12E800.
- Zum Vergleich DE: Entry 0x800360F4, text_size 0x12B000, ebenfalls Load 0x80020000. Der Aufbau ist ähnlich, die Adressen liegen oft nahe beieinander, sind aber nicht einheitlich verschoben.

**Gepatchte Kopie `C:\Discs\AlundraUS\` (`game.bin` + `Alundra.cue`):**
- `SYSTEM.CNF` (Sektor 48460): `BOOT=cdrom:\SLUS_005.53;1` (Leerzeichen entfernt, damit die Länge 65 Byte bleibt).
- Verzeichniseintrag `EASY_005.53;1` (Root-Verzeichnis, Sektor 22) umbenannt in `SLUS_005.53;1`.
- Grund: Der Runtime bestimmt die Serial aus dem BOOT-Dateinamen. Bei `EPIX.EXE` gibt es keine, und das BIOS würde den Lader statt des Spiels starten. `EASY_...` würde als "EASY-00553" erkannt.
- Folge: Start immer im Modus EASY, HARD ist nicht erreichbar. Die EDC/ECC-Daten der Sektoren sind nicht neu berechnet (der Runtime stört sich nicht daran).
- Digests der Kopie: MD5 `b1a1a01a890cc9f939dd7d14e833bd27`, SHA1 `e0172f00b07467ff3555fd00e51e593d418820ab`, CRC32 `c14e9fca`.

## Was im Projekt geändert wurde (nur auf dem Branch)

| Datei | Änderung |
|---|---|
| `game.toml` | id `SLUS-00553`, exe `disc/SLUS_005.53`, disc `C:\Discs\AlundraUS\Alundra.cue`, Entry 0x80036044, text_size 0x0012E800, Digests, Netplay-fp, `mod_instruction_sites = []` |
| `CMakeLists.txt` | `GEN_MARKER`/`GEN_FULL_GLOB` auf `SLUS_005.53` |
| `.recomp.json`, `catalog_identity.json`, `disc_probe.json` | Serial/Boot-Exe/Region auf US (`disc_probe.json` und `catalog_identity.json` teils nur per sed, Digests dort ggf. noch alt) |
| `mods/preloaded/packages/alundra.enhancement.widescreen/1.0.0/manifest.toml` | `game_id = "SLUS-00553"` |
| `seeds/ghidra_funcs.txt` | neu: nur Entry + JAL-Ziele aus dem Spiel-EXE (493 Seeds), nicht die handgepflegten DE-Seeds |
| `disc/SLUS_005.53` | aus `EASY_005.53` extrahiert (PS-X EXE) |

Gesichert (DE-Stand): `game.toml.de_main`, `.recomp.json.de_main`, `catalog_identity.json.de_main`, `disc_probe.json.de_main`, `generated.de_main/`, `build-debugtools.de_main/`. Das Release-Build `build-release` ist noch DE und unverändert.

**Zurück auf DE:**
1. `git switch main`
2. `generated` und `build-debugtools` löschen oder wegräumen, dann `generated.de_main` → `generated` und `build-debugtools.de_main` → `build-debugtools` zurückbenennen.
3. Die `*.de_main`-Dateien zurückkopieren, falls sie auf `main` nicht schon stimmen (die Konfigdateien sind versioniert, `game.toml.de_main` ist eine Sicherung).

## Wie ich gebaut und gestartet habe

```
export PATH="$HOME/.local/share/retcomm/toolchains/cmake-clang-v1/1.0.14/bin:$PATH"
python psxrecomp/psxrecomp_cli.py generate --config game.toml --project-root . --force-prepare
python psxrecomp/psxrecomp_cli.py rebuild --config game.toml --project-root . --build-dir build-debugtools --no-pgo --cmake-extra=-DPSX_DEBUG_TOOLS=ON
cd build-debugtools
PSX_DEBUG_SERVER=1 ./Alundra.exe --no-launcher --disc "C:/Discs/AlundraUS/Alundra.cue" --debug-port 4370
```

- `rebuild` allein regeneriert den Code nicht. Nach jeder Änderung an `game.toml` (Sites, Seeds, exe) zuerst `generate`. `mod_instruction_sites` sind Strings (`"0x8002D1CC"`), Zahlen werden abgelehnt. Reine Mod-Änderungen brauchen nur `rebuild`.
- Screenshot im Debug-Client: `python psxrecomp/tools/debug_client.py screenshot_wide_hires "path=C:\...\datei.png"` (Windows-Pfad mit Backslashes). `screenshot_file` mit Schrägstrich-Pfad lieferte "cannot open file".
- Vor jedem Rebuild `taskkill //F //IM Alundra.exe`.

## Testen (Nutzerwunsch, 2026-11-24)

**Zum Testen startet immer Claude das Debug-Build** (nach jedem Rebuild, ohne Nachfrage): `cd build-debugtools; PSX_DEBUG_SERVER=1 ./Alundra.exe --no-launcher --disc "C:/Discs/AlundraUS/Alundra.cue" --debug-port 4370` (im Hintergrund). Der Nutzer lädt den Spielstand von Hand und spielt. Vorher `taskkill //F //IM Alundra.exe`.

## Stand 2026-11-24 (später): Hintergrund + Kartenrand

- `alundra_bgcolor.c`: Site 0x8008952C (US, Wort 0xAC850000, a1 = Farbe, a3+4 = 0x00F00140). Default (8,0,0) für alle Räume ohne Tabelleneintrag; das Spiel selbst clear't im Dorf mit (0,0,0).
- `alundra_edgefade.c`: Site 0x8002D7A4 (Wort 0x0000C021, OT-Basis in fp). Verlauf endet additiv in (8,0,0). Farben/Hintergrund vom Nutzer bestätigt (2026-11-24: stimmen immer; evtl. liegt es an der angepassten Fan-Patch-ISO). Dorf-Hash in US ungeprüft (Tabelle: 0x0B440C2D, 0xB4655671, Randsignatur 0x1D39BE10).
- Beide gebaut (Debug). Hinweis: HUD-Sites 0x8004D588 / 0x8004D6B4 (`alundra_hud.c`) stehen ebenfalls in `mod_instruction_sites`, Details hier noch nicht dokumentiert.
- Branch `usa-slus-00553` wurde am 2026-11-24 in `main` gemergt (DE-Stand liegt damit nur noch in `*.de_main` und der Git-Historie).

## Nächste Schritte

1. **Weiter portieren** (Reihenfolge nach Nutzen): Kartenrand/Kantenquad (DE-Site 0x8002D444 entspricht in US der Kachelschleifen-Ausgang 0x8002D7A4, dort hängt bereits die Pillarbox), HUD in den Ecken (DE-Sites 0x8004C0C0 / 0x8004C220), Speicher-/Laderaum-Nebel (DE 0x800262EC, Nebel aus 0x66-Sprites über die generische Objektroutine), Mine/Raumfarben (`alundra_bgcolor.c`, Site DE 0x80086CC4). Jedes Mal: Paket im `gpu_frame_dump` finden, `wtrace_add` auf die Paketadresse, Schreiber-PC per `disasm` lesen, Hook-Wort aus dem RAM lesen (muss exakt stimmen, sonst greift der Hook still nicht).
2. **Testen:** Titelbild, Neues Spiel, erste Spielszene, Speichern/Laden, FMV. Fehlende Seeds zeigen sich als Absturz/Hänger (Adresse in `seeds/ghidra_funcs.txt` ergänzen, `generate`, Rebuild).
3. **Statischen US-Code** gibt es nicht aus dem Disc-File (stimmt bei DE nicht mit dem RAM überein). Zum Lesen: RAM per `read_ram` in 16-KB-Blöcken dumpen (0x80020000..0x80150000) und/oder `disasm addr= count=`. Ein Wortvergleich DE/US (difflib) brachte wenig, der Code ist zu verschieden aufgebaut.
4. **Offene Fragen:**
   - Was bewirkt der Fan-Patch im Code? Kann `HARD_005.53` oder der Lader (`EPIX.EXE`) genutzt werden (Menü, Schwierigkeit)? `DEBUG.EXE`, `INTRO.EXE`, `END.EXE` sind eigene Programme.
   - `catalog_identity.json` / `disc_probe.json` auf Digests und Region prüfen, bevor etwas veröffentlicht wird.
   - Mod-Dateien ggf. so aufteilen, dass DE und US aus demselben Code gebaut werden können (Adressen per Define). Aktuell nur Branch-Lösung.
   - PAL → 60 Hz (`PSX_FORCE_60HZ`) spielt bei der US-Version (NTSC) keine Rolle.

## Weiterführend

- Projekt-Memory: `docs/memory/alundra-usa-port.md`
- Allgemein: `docs/PSX_SPIEL_PORTIEREN.md`, `docs/ALUNDRA_WIDESCREEN_HANDOFF.md` (DE-Details zu Kacheln, HUD, Wolken)
- DE-Referenz der Mods: `alundra-recomp/mods/alundra_widescreen.c`, `alundra_hud.c`, `alundra_pillarbox.c`
