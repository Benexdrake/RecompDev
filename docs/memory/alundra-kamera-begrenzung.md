---
name: alundra-kamera-begrenzung
description: Alundra Kamera im 16:9 am Kartenrand begrenzen (Feature camera_clamp, Hook 0x8002D1B8), bestätigt 2026-11-26
metadata:
  type: project
---

Feature `camera_clamp` (Datei `alundra-recomp/mods/alundra_camclamp.c`, Plugin `alundra.camclamp`, im selben Manifest-Paket `alundra.enhancement.widescreen` wie `widescreen`/`hud_corners`, aber eigener Schalter in `state.toml`). Im Dorf bestätigt ("Sehr gut"): Kamera stoppt am Kartenrand, keine Sicht über die Karte hinaus.

**Wie:** Das Spiel klemmt Kamera X (US 0x801EF434) bei 0x8002D188..0x8002D1B0 hart auf [0, 927] (4:3-Fenster). Hook direkt danach auf Site 0x8002D1B8 (Wort **0x3C04801F**, LUI a0) verengt auf [m, cols*24-321-m], m = `psx_mod_widescreen_view_x_margin()` (zur Laufzeit 53, nicht 39). **Seit 2026-11-26 (Nutzer bestätigt: funktioniert) in ALLEN Räumen**: Spaltenzahl aus `alundra_edge_room_cols()` (`alundra_edgefade.c`: Dorf, Wald), sonst Fallback 52 (`ALU_MAP_COLS`). Erst war es nur auf diese Tabelle beschränkt; Nutzer wollte es als Default überall zum Testen. Kleine Innenräume (Häuser/Höhlen) wurden nicht gezielt geprüft, mögliche Verschiebung ~53 px; Zurück auf Raumliste = `if (cols <= 0) return;` in `alundra_camclamp.c`, nur Rebuild. Der weiche Kartenrand (`map_edge_fade`) wird dort per `g_alu_cam_clamp_on` pro Frame übersprungen, ist bei ausgeschaltetem Feature wieder da. Kamera Y unverändert (Höhe gleich).

**Why:** Nutzerwunsch, statt des dunklen Übergangsrands lieber nicht über den Rand sehen.
**How to apply:** Der Randverlauf wird nur in Räumen der Tabelle `g_alu_edge_rooms` (edgefade.c) übersprungen; die Klemme gilt überall. Neue Site 0x8002D1B8 steht in `game.toml` `mod_instruction_sites` (brauchte `generate`).

**Fallen:** (1) Erst falsches Hook-Wort (0x3C022AAA aus falsch gelesener Disasm-Zeile) -> Hook lief still nie; Wort immer per `read addr 4` gegen RAM prüfen (little-endian). (2) Projektordner wurde nach `C:\Users\BeneX Drake\Desktop\Development\RecompDev` verschoben: `build-debugtools` hatte alten CMake-Cache (`c:/RecompDev`), `CMakeCache.txt`, `CMakeFiles`, `_deps` löschen half. (3) Toolchain `cmake-clang-v1` fehlte, `psxrecomp_cli.py ensure-toolchain` holte sie neu (danach Recompiler-Neubau, einige Minuten). (4) `generate` ohne `--build-dir`/`--cmake-extra`. Nur Debug gebaut.
