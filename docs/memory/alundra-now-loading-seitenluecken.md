---
name: alundra-now-loading-seitenluecken
description: Alundra "Now Loading"-Bild: Seiten in 16:9 grün statt schwarz; gelöst im Framework (gpu.c, VBlank-Idle-Clear der Seitenränder), 2026-11-25
metadata:
  type: project
---

# Alundra: Seitenränder im "Now Loading"-Bild (16:9) — gelöst

Stand 2026-11-25, **Nutzer bestätigt**: Seiten werden beim Laden schwarz. Nur Debug-Build (nur `widescreen` aktiv getestet), Release nicht neu gebaut.

## Ursache
- Das Ladebild ist **keine hochgeladene Grafik**: erst zeichnet das Spiel es als normale Kachelkarte (320 px breit, Raumkarte geladen, Clear `0x02000800` = (0,8,0), 2 Sprites `0x64`), danach steht es **still ohne jedes Primitive** und ohne Raumkarte (`alundra_room_sig() == 0`, Zeiger 0x801AC6C4 = 0). Im Ring sind dann alle Frames leer.
- Die 16:9-Seitenränder sind **Host-Flächen** (`gr_wide_*`), keine VRAM-Pixel (VRAM x 320.. ist 0). Sie behalten die letzte Clear-Farbe ((0,8,0) außen, (8,8,0) innen). Nur das erste Primitive eines Frames leert sie, im Standbild passiert das nie.
- Es lag NICHT an `hud_corners` (Nutzer-Verdacht, per Abschalten widerlegt).

## Fix (Framework, `psxrecomp/runtime/src/gpu.c`)
`gpu_vblank_tick`: Zähler `ws_idle_flips` zählt VBlanks seit dem letzten Primitive (Opcode 0x20..0x7F, in `gp0_execute_command` zurückgesetzt). Ab 4 VBlanks ohne Primitive und `ws_native_wide_active()` ruft er einmal `ws_clear_all_reveal_margins()` (schwarz). Gilt für alle Projekte (nach Rebuild), nicht nur Alundra. Nicht auf `GP1(05)` legen: im Standbild kommt kein Flip.

## Gescheiterte Wege (nicht wiederholen)
- Seitenquads im Objektzeichner (`alundra_loading_sides`): Hook feuerte nie, entfernt.
- Fill an 0x8002E888 verbreitern: x wird maskiert, überschrieb UI-Texturen, **UI weiß**.
- Clear-Hook (0x8002E888 bzw. 0x8008952C, Farbe schwarz/rot setzen): keine Wirkung, das Clear wird im Ladebild nicht jeden Frame neu geschrieben, der Standbildzustand ist der Host-Rand. Entfernt.
- Hook im `gp0_exec_cpu_to_vram` (Vollbild-Upload): im Ladebild gibt es keinen großen A0-Upload (`a0_history` hält nur die ersten 128, der Ladebild-Upload steht nie drin).
- Der Memory-Card-Raum hat selbst schwarzen Hintergrund: ein schwarzer Screenshot dort beweist den Fix nicht. Immer im eigentlichen Ladebild prüfen.

## Debug-Tipps
- Ladebild verpasst man leicht (Standbild ~800 Frames). Wächter-Skript pollt `screenshot_wide_hires` und prüft helle Pixel im Schriftzug-Bereich (x 760..1400, y 790..860).
- Der Debug-Server bricht Verbindungen nach ein paar Befehlen ab: pro Befehl neu verbinden.
- Framework-Regel: keine `fprintf`/Log-Dateien (psxrecomp/CLAUDE.md §3), nur Debug-Server-Befehle.
