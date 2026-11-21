# PSX-Spiel mit PSXRecomp zum Laufen bringen (Windows)

Praxisanleitung, erprobt mit **Breath of Fire III (Europe)**, Serial SLES-01304,
Boot-EXE `SLES_013.04`. Gilt genauso für andere PSX-Spiele als BIN/CUE-Dump.

PSXRecomp übersetzt den Code deines Spiels vorab nach C (statische Rekompilierung)
und baut daraus ein eigenes natives Programm. Es ist kein fertiger Emulator. Du
brauchst pro Spiel ein eigenes Projekt. Die Disc bleibt deine eigene Kopie, und
ein Sony-BIOS brauchst du nicht (es wird OpenBIOS genutzt).

## Ergebnis dieses Durchlaufs

| Was | Ort |
|---|---|
| Framework (Quellcode) | `...\Development\psxrecomp` |
| Toolchain | `C:\RecompDev\Toolchain` |
| Disc + CUE | `C:\Discs\BOF3\` |
| Spiel-Projekt | `C:\RecompDev\bof3-recomp` |
| Spielbares Release | `...\bof3-recomp\build-release\BreathOfFire3.exe` |
| Variante mit Debug-Server | `...\bof3-recomp\build-debugtools\BreathOfFire3.exe` |
| Debug-Client | `...\bof3-recomp\tools\psx_debug.py` |

Stand: Das Spiel startet und zeigt das Titelbild. Gespielt über längere Strecken
wurde noch nicht, spätere Abschnitte sind ungetestet.

## 0. Voraussetzungen

- Windows x64, Git, Python 3 (im PATH).
- Rund 5 GB frei (Toolchain, Quellcode, ca. 2,4 Mio. Zeilen generierter C-Code,
  zwei Builds).
- Eine eigene, legale Disc-Kopie.

## 1. Disc vorbereiten (CUE erstellen)

Die Setup-Skripte brauchen eine `.cue`. Hast du nur `.bin`-Dateien, schreibst du
sie selbst. Lege die Disc **außerhalb** des Framework-Repos ab, z. B. `C:\Discs\<Spiel>\`.

Bei zwei Tracks (Daten + Audio) sah sie so aus:

```
FILE "Spiel (Track 1).bin" BINARY
  TRACK 01 MODE2/2352
    INDEX 01 00:00:00
FILE "Spiel (Track 2).bin" BINARY
  TRACK 02 AUDIO
    INDEX 00 00:00:00
    INDEX 01 00:02:00
```

Vor dem Schreiben prüfen:
- Dateigröße durch 2352 muss ohne Rest aufgehen (Rohsektoren). Sonst ist es kein 2352-Dump.
- Track 1 beginnt mit dem Sync-Header `00 ff ff ff ff ff ff ff ff ff ff 00`.
- Datentrack ist bei PSX meist `MODE2/2352`, Audiotracks heißen `AUDIO`.
- Bei Redump-Dumps mit getrennten Dateien steht bei Audiotracks oft
  `INDEX 00 00:00:00` und `INDEX 01 00:02:00`. Abweichende Pregaps ggf. anpassen.
- Mehr als zwei Tracks: pro Track einen `FILE`-Block ergänzen.

Der Launcher bestätigt später: „Disc verified“, Serial, Region, „ISO header OK“.

## 2. Werkzeuge einrichten (einmalig)

1. Toolchain laden: `cmake-clang-v1-windows-x64.zip` (~210 MB) von
   https://github.com/RetroPortingToolKit/RetroPorting-Toolchains/releases/latest
   und nach `C:\RecompDev\Toolchain` entpacken. Danach muss
   `C:\RecompDev\Toolchain\bin\cmake.exe` existieren.
2. Framework klonen mit Submodulen, oder in einem vorhandenen Klon:
   ```
   git submodule update --init --recursive
   ```
3. In **jedem neuen PowerShell-Fenster** die Umgebung setzen:
   ```powershell
   $env:PSXRECOMP_TOOLCHAIN_DIR = 'C:\RecompDev\Toolchain'
   $env:Path = "$env:PSXRECOMP_TOOLCHAIN_DIR\bin;$env:Path"
   cmake --version; ninja --version; clang --version
   ```
   Alle drei müssen eine Version ausgeben.

## 3. Projekt generieren und bauen

Im Framework-Ordner:

```powershell
powershell -File tools\new_project_layout\setup_project.ps1 `
  -Disc 'C:\Discs\<Spiel>\<Spiel>.cue' -Dir 'C:\RecompDev' `
  -Name <Spielname> -GithubRepo <ordnername> -Players 1 -Yes `
  -EnableRecompUi -NoNetplay -NoFetchBoxart -NoGithub -Generate -EnableBuild
```

Das Skript liest die Disc, legt das Projekt an, erzeugt den C-Code (Spiel und
OpenBIOS) und baut. Es dauert einige Minuten.

**Bekannte Eigenheit:** Am Ende kann „WARNUNG: Generate failed“ stehen, obwohl
„Generate complete“ im Log steht und der Code erzeugt wurde. Die Ursache ist nicht
geklärt (Verdacht: `set: pipefail`-Meldungen der Shell-Skripte unter Windows). Das
Setup baute in unserem Fall nicht zu Ende. Deshalb zusätzlich von Hand:

```powershell
Set-Location C:\RecompDev\<ordnername>
python psxrecomp\psxrecomp_cli.py rebuild --config game.toml --project-root . `
  --build-dir build-release --no-pgo
```

Das Ergebnis ist `build-release\<Spielname>.exe`. Der Ordner `overlay_toolchain`
wird mit gebaut und neben die EXE gelegt. Ein einfaches `cmake --build` ohne den
`rebuild`-Befehl stellt ihn nicht bereit.

Hinweise zu Fehlermeldungen im Log: Compiler-Warnungen zu `operator""` und
`-Wswitch` sind harmlos. Das PowerShell-Fehlerformat `NativeCommandError` bei
„Cloning into …“ ist nur Git-Ausgabe auf stderr.

## 4. Starten und testen

1. `build-release\<Spielname>.exe` starten. Der Launcher zeigt die Disc-Prüfung.
2. **PLAY** klicken (oder `--no-launcher` verwenden, siehe unten).
3. Testkette: Boot, Logo, Titelbild, Neues Spiel, erste Spielszene. Erst wenn
   Bild und Ton wirklich kommen, gilt es als lauffähig. Ein Eintrag im Log reicht nicht.
4. Auf FMV, Szenenwechsel, Kämpfe, Speichern/Laden und Menüs achten. Dort zeigen
   sich fehlender Code und Overlays zuerst.

Nützliche Startoptionen:

| Option | Wirkung |
|---|---|
| `--no-launcher` | Launcher überspringen |
| `--disc "<cue>"` | Disc direkt angeben |
| `--debug-port 4370` | Port des Debug-Servers |
| `--launcher` | Launcher erzwingen |

## 5. Wenn etwas nicht klappt

Grundregel: **Generierten C-Code niemals von Hand ändern.** Du korrigierst Seeds,
Config oder das Framework und generierst neu.

| Symptom | Ursache / Maßnahme |
|---|---|
| Absturz oder Hänger an einer Stelle | Fehlende Funktions-Seeds: Adresse in `seeds/ghidra_funcs.txt` ergänzen, dann neu generieren (`psxrecomp_cli.py generate ...`) und neu bauen |
| Spiel lädt Code von der Disc (Overlays) | Läuft über die mitgebaute `overlay_toolchain`. Meldung `tcc tier active but no bundled toolchain` heißt: mit `rebuild` statt bloßem `cmake` bauen |
| Ruckeln, Timing-Probleme | Einstellungen in `game.toml` unter `[runtime]`, erst mit Belegen aus Log oder Telemetrie |
| FMV/Video-Fehler | Spiel-spezifisch, in `game.toml`/Doku zu FMV prüfen |
| Disc wird nicht erkannt | CUE prüfen (Pfade, Dateinamen, Trackart). `game.toml` → `disc = ...` |
| `cmake`/`clang` nicht gefunden | Umgebung aus Schritt 2 im aktuellen Fenster neu setzen |

Weitere Diagnose: Das Spiel schreibt Sessions mit Eingaben und Telemetrie nach
`saves/diagnostics/session-<zeit>`. Der Ordner lässt sich zippen und zur
Fehlersuche weitergeben. L3 + R3 gleichzeitig markiert einen Vorfall.

Docs im Framework: `docs/GETTING_STARTED.md`, `docs/GAME_PROJECT_SETUP.md`,
`docs/BUILDING.md`, `docs/config_schema.md`, `docs/EXECUTION_MODEL.md`.

## 6. Auf Spieldaten von außen zugreifen (Debug-Server)

Der **Release-Build hat keinen Debug-Server** (`PSX_DEBUG_TOOLS` ist aus). Für
RAM-Zugriff baust du eine zweite Variante in einen eigenen Ordner:

```powershell
python psxrecomp\psxrecomp_cli.py rebuild --config game.toml --project-root . `
  --build-dir build-debugtools --no-pgo --cmake-extra=-DPSX_DEBUG_TOOLS=ON
```

Starten (der Server öffnet sich erst, wenn das Spiel läuft, nicht schon im Launcher):

```powershell
.\build-debugtools\<Spielname>.exe --no-launcher --disc "C:\Discs\<Spiel>\<Spiel>.cue" --debug-port 4370
```

Protokoll: TCP `127.0.0.1:4370`, pro Zeile ein JSON-Objekt, Antwort als eine Zeile.
Beispiele: `{"cmd":"ping"}`, `{"cmd":"read_ram","addr":"0x80096800","len":64}`
(Antwort mit `hex`), `{"cmd":"write_ram","addr":"0x...","val":"0x63"}`,
`{"cmd":"screenshot_file","path":"C:/Temp/bild.png"}`. Weitere Befehle stehen in
`psxrecomp/runtime/src/debug_server.c`.

Mitgelieferter Client `tools/psx_debug.py`:

```
python tools/psx_debug.py ping
python tools/psx_debug.py read 0x80096800 64
python tools/psx_debug.py write 0x800A1234 0x63
python tools/psx_debug.py shot C:/Temp/bild.png
python tools/psx_debug.py snap vorher      # 2 MB RAM sichern
python tools/psx_debug.py snap nachher
python tools/psx_debug.py diff vorher nachher
```

**Validierung (gemacht):** RAM an der Ladeadresse `0x80096800` stimmt Byte für Byte
mit der EXE von der Disc überein. Das PSX-RAM liegt bei `0x80000000` bis
`0x801FFFFF` (2 MB).

**Werte finden (HP, Gold, Position):** Spielstand A sichern (`snap vorher`),
im Spiel genau eine Sache ändern (z. B. Gold ausgeben), dann `snap nachher` und
`diff`. Mit mehreren Durchläufen schränkst du die Adresse ein. Beachte, dass
Werte oft 16- oder 32-Bit sind (Little Endian), und dass die Adresse zwischen
Spielabschnitten wandern kann. Fertige Adressen findest du auch in
Cheat-Datenbanken für das Spiel.

Wer Werte dauerhaft ändern oder anzeigen will, nutzt das Mod-System:
`psxmod.md`, `docs/MOD_MEMORY_ADDRESSES.md`, `docs/MOD_PACKAGES.md`.

## 7. Checkliste für das nächste Spiel

- [ ] CUE vorhanden, Größen durch 2352 teilbar, Sync-Header geprüft
- [ ] Toolchain entpackt, `cmake`/`ninja`/`clang` im PATH des Fensters
- [ ] Submodule initialisiert
- [ ] `setup_project.ps1` mit neuem `-Name`, `-GithubRepo`, `-Disc`
- [ ] `rebuild` in `build-release` erfolgreich, EXE vorhanden
- [ ] Launcher: „Disc verified“, Serial und Region passen
- [ ] Boot bis Titelbild und erste Szene
- [ ] Bei Bedarf: `build-debugtools` bauen, Server testen
- [ ] Probleme dokumentieren: Befehl, Fehlertext, Schritt, Spiel/Disc-Version

## Offene Punkte (ehrlich)

- Ursache von „Generate failed“ am Ende des Setups ist ungeklärt.
- Nur Boot und Titelbild geprüft. Längere Spielstrecken, FMV, Ton und Overlays
  sind nicht systematisch getestet.
- Der Debug-Build kann wegen der Instrumentierung langsamer sein.
- Die Rechtslage der eigenen Disc-Kopie und des Frameworks liegt bei dir
  (Lizenzdateien `LICENSE`, `THIRD_PARTY_ATTRIBUTION.md` im Framework).
