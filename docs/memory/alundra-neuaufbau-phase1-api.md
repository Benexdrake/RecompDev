---
name: alundra-neuaufbau-phase1-api
description: Phase 1 Widescreen-Neuaufbau erledigt; Antworten zu Plugin-API-Fragen (Hook-Adressen, Feature-Abfrage, Activation)
metadata:
  type: project
---

Phase 1 (2026-11-22): Alt-Mod nach `mods/alundra_widescreen_legacy.c.txt` (git mv). Neu: `alundra_common.h` (Konstanten, `alundra_room_sig`), `alundra_widescreen.c` (nur 16:9-Aktivierung), `alundra_bgcolor.c`, `alundra_edgefade.c` (leere Gerüste). Manifest: Features `background_color` / `map_edge_fade`. CMake eingetragen. Debug-Build grün.

Antworten (aus Runtime-Code `mod_packages.cpp` / `mod_runtime.cpp`, nicht per Spieltest):
- Zwei Plugin-IDs auf derselben Adresse + Wort: **erlaubt**. Die Duplikatprüfung gilt nur pro Plugin-ID (`mod_register_instruction_plugin`). Aktive Hooks werden stabil nach Adresse sortiert, Reihenfolge = Plan-Reihenfolge der Plugins. Dieselbe ID darf dieselbe Adresse nur einmal registrieren.
- Abfrage anderer Features: keine direkte API. `psx_mod_widescreen_view_x_margin()` ist > 0 nur im 16:9-Betrieb (Widescreen an) und taugt als Indikator; `psx_mod_option_value` nur für eigene Optionen.
- Activation: eine pro Plugin-ID (`psx_mod_register_activation_plugin`). Mehrere Dateien müssen sich eine ID teilen oder eigene IDs/Features haben; Arenen daher in der Activation der jeweiligen ID anlegen. Deaktivierte Features sind inert (Hooks laufen nicht).
- 4:3 mit anderen Features an: Rand/Farbe müssen bei margin <= 0 selbst nichts tun (in den Phasen 3/4 einbauen).

**Ungeprüft:** Start des Debug-Builds (Debug-Server kam bei mir nicht hoch, Log endet nach Launcher-Init) und Schalter im Debug-`state.toml`. Nutzer muss starten/prüfen.
