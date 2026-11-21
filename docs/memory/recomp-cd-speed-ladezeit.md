---
name: recomp-cd-speed-ladezeit
description: CD-Speed 16 für Alundra aktiv (Raumwechsel 5 s → ~2 s); Framework-Fixes in fntrace.c/cdrom.c; fast-loading und instant bringen nichts
metadata:
  node_type: memory
  type: project
  originSessionId: 19e43e8f-83a2-4a6a-8a35-fbfbccd8b0c4
  modified: 2026-11-21T16:19:49.028Z
---

Alundra-Ladezeit (2026-11-21): Feature `psx.enhancement.cd-speed` in `build-*/mods/state.toml` (`[[feature]] package_id/id = cd-speed`, `multiplier = "16"`, `instant = "false"`). Raumwechsel/Hauswechsel ~5 s → ~2 s (vom Nutzer bestätigt). Release neu gebaut.

**Warum:** Der Divisor kam anfangs nie an, weil ein wiederhergestellter Boot-Snapshot ihn überschrieb. Fixes im Framework: `psxrecomp/runtime/src/fntrace.c` (`fntrace_restore_game_started` ruft `cdrom_notify_game_started`) und `cdrom.c` (`cdrom_snap_parse` liest gespeicherte Disc-Speed-Werte nur und verwirft sie). Prüfen per `cdrom_bursts` (Feld `divisor`, 16 erwartet; 1 = nicht angewendet).

**Grenzen:** Reine Lesezeit liegt bei ~0,25–0,6 s, die restlichen ~1,5 s sind Spiellogik (frame-gebunden, vermutlich Fades). `instant` (divisor 0, 32 Sektoren/Frame) war nicht schneller als 16, daher nicht gewählt. `fast-loading` (Host-Pacing) greift bei Alundra nicht (`turbo_frames` nur vom Boot), wieder entfernt. Nächster Schritt wäre ein Alundra-eigener Hook auf die Wartezeiten, nicht angefangen.

**How to apply:** Nicht erneut Multiplikatoren über 16 oder `instant` testen. Beim Bearbeiten von `state.toml` beachten: das Spiel sortiert die Datei um (Packages zuerst, dann Features), nie per Textabschnitt abschneiden. Gleiche Fixes helfen BoF3/BoF4/LoD (gemeinsames Framework, noch nicht dort aktiviert). Siehe [[recomp-docs-in-claude-md]].
