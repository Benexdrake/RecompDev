# Phase 1: Umbenennen und Gerüst

Ziel: Alt-Mod aus dem Build nehmen, neue Mod-Dateien mit funktionierender Registrierung bereitstellen.

## Aufgaben

1. **Umbenennen:** `mods/alundra_widescreen.c` → `mods/alundra_widescreen_legacy.c.txt` (Endung `.txt`, damit nichts versehentlich kompiliert wird). Dient nur als Vorlage zum Herauskopieren. Die `.bak*`/`.pre_*`-Dateien bleiben liegen.
2. **Neue Dateien anlegen** (Vorschlag):

   | Datei | Inhalt (Phase) |
   |---|---|
   | `mods/alundra_common.h` | Konstanten (`ALU_TILE_W`, `ALU_CAM_X`, `ALU_MAP_ROWS_PTR` ...) und Raum-Hash `alundra_room_sig()` |
   | `mods/alundra_widescreen.c` | Aspekt, Aktivierung, Kacheln (Phase 2) |
   | `mods/alundra_ws_clouds.c` | Wolken, Nebelstreifen (Phase 2) |
   | `mods/alundra_ws_mask.c` | Ringmaske, Tor-Schatten (Phase 2) |
   | `mods/alundra_bgcolor.c` | Phase 3 |
   | `mods/alundra_edgefade.c` | Phase 4 |

   Die Aufteilung des Widescreen-Kerns in mehrere Dateien ist optional. Wichtig: ein Feature = ein Plugin-Name = klarer Besitzer pro Hook.
3. **Manifest** `mods/preloaded/packages/alundra.enhancement.widescreen/1.0.0/manifest.toml` um zwei Features ergänzen:
   - `background_color` (Plugin `alundra.bgcolor`, Gruppe Visual, `default_enabled = true`)
   - `map_edge_fade` (Plugin `alundra.edgefade`, Gruppe Visual, `default_enabled = true`)

   Beschreibung von `widescreen` anpassen (nur 16:9). Im Debug-`state.toml` braucht jedes `[[feature]]` zusätzlich `package_id = "alundra.enhancement.widescreen"`.
4. **CMakeLists.txt:** neue `.c` per `target_sources(psx-runtime PRIVATE ...)` eintragen, den alten Eintrag entfernen.
5. **Technische Klärungen** (kleine Testmods, bevor Code verschoben wird):
   - Dürfen zwei Plugin-IDs `psx_mod_register_instruction_plugin` auf **dieselbe Adresse und dasselbe Wort** setzen? Wenn nein: ein Dispatcher am Site, der intern die aktiven Features aufruft.
   - Wie fragt ein Plugin ab, ob ein anderes Feature an ist (z. B. ob `widescreen` aktiv ist)? Gibt es eine API?
   - Eine Activation pro Plugin-ID: wo legt man Arenen an, wenn ein Feature mehrere Dateien hat?
   - Läuft das Spiel mit ausgeschaltetem `widescreen` (4:3) unverändert, wenn die anderen Features an sind? Erwartung: Rand und Farbe tun in 4:3 nichts oder sind harmlos.

## Ergebnis

Build läuft grün mit leeren Plugins, drei Schalter im Debug-`state.toml`, Antworten zu den vier Fragen als Memory-Eintrag.

## Abnahme

Debug-Build startet, Spiel spielbar (mit noch kaputtem 16:9, das ist erwartet), keine Startfehler "Mods unavailable".
