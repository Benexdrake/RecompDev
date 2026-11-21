# PAL-Spiele mit 60 Hz statt 50 Hz laufen lassen (PSX-Recomp)

**Status: Standard in allen vier Projekten (bof3, alundra, bof4, lod), alle getestet.**
Abschalten (zurück auf 50 Hz): `$env:PSX_FORCE_60HZ = 0`.

Getestet mit **Breath of Fire III (Europe, SLES-01304)**: vorher 50,0 fps
(Ruckeln), mit Schalter 59,9 fps, laut Nutzer „läuft perfekt".
Nicht geprüft: Ton/Musik-Sync, FMVs, andere Spiele.

## Warum 50 Hz?

Europäische Discs setzen im GPU-Befehl GP1(08h) das PAL-Bit (Bit 3).
Die Runtime leitet daraus alles ab: VBlank-Takt, HBlank-Timer (Timer 1)
und das Host-Frame-Pacing. Das Spiel selbst läuft also auf 50 Hz, weil
es das so anfordert.

## Die Änderung

Datei `psxrecomp/runtime/src/psx_video_timing.c` (liegt in allen vier
Projekten: bof3, alundra, bof4, lod). Der Override sitzt in
`psx_video_timing_set_pal`, weil dort alle Ableitungen zusammenlaufen.

```c
#include <stdlib.h>

/* Enhancement: PSX_FORCE_60HZ=1 runs a PAL title on NTSC (60 Hz) timing. */
static int force_60hz(void) {
    static int cached = -1;
    if (cached < 0) {
        const char* e = getenv("PSX_FORCE_60HZ");
        cached = (e && e[0] && e[0] != '0') ? 1 : 0;
    }
    return cached;
}

int psx_video_timing_set_pal(int pal) {
    pal = (pal && !force_60hz()) ? 1 : 0;   // war: pal = pal ? 1 : 0;
    ...
```

Rest der Funktion bleibt unverändert.

## Anwenden in einem anderen Projekt

1. Obige Änderung in `<projekt>\psxrecomp\runtime\src\psx_video_timing.c`
   einfügen (Stand beim Test: bof3 hat sie bereits; die anderen drei nicht).
2. Neu bauen:
   ```powershell
   cmake --build C:\RecompDev\<projekt>\build-release --config Release
   ```
   (für Debugtools analog `build-debugtools`)
3. Starten:
   ```powershell
   $env:PSX_FORCE_60HZ = 1
   .\build-release\<Spiel>.exe
   ```
   Ohne Variable läuft das Spiel wie bisher mit 50 Hz.

## Prüfen

- Im Log sollte `[FPS] game: 59.9 fps` stehen (vorher `50.0 fps`).
- Die Warnung „host panel 60.0 Hz does not match guest cadence; keeping
  50.00 Hz pacing" darf nicht mehr erscheinen; stattdessen
  „present cadence: driver vsync (60.0 Hz panel ...)".
- Mit Debug-Build und `--debug-port 4370` geht `python tools/psx_debug.py ping`
  und `shot`. Das Tool liegt im Root (`C:\RecompDev\psx_debug.py`) und als
  Kopie in `tools\` von bof3, lod, bof4 und alundra. Nur eine Instanz pro
  Port 4370, laufendes Spiel vorher beenden. Hinweis: Der Screenshot war im
  Test schwarz bzw. sehr dunkel (Intro/Ladescreen oder Screenshot-Problem,
  nicht geklärt).
- LoD (SCES-03045) getestet: Patch eingebaut, Debug-Build zeigt 60,0 fps.
  Musik/FMV nicht geprüft.

## Was man wissen sollte

- **Das Spiel wird ~20 % schneller**, weil die Logik am VBlank hängt. Das
  entspricht dem Tempo der NTSC-Fassung. Es ist kein „flüssigeres Bild bei
  gleicher Geschwindigkeit".
- Beim Booten wechselt die Runtime kurz zwischen NTSC und PAL (GP1(00h)
  setzt NTSC zurück, das Spiel setzt dann PAL). Das ist normal.
- Noch offen: Verhalten von Musik/Sprache, FMVs (laufen sie zu schnell?),
  Spiele, die den PAL-Status aus GPUSTAT lesen und davon Logik abhängig machen.
- Als dauerhafte Option wäre ein `game.toml`-Eintrag sauberer als die
  Umgebungsvariable (dafür muss `config_loader.cpp` ein neues Feld lesen,
  analog zu `disc_speed`).
