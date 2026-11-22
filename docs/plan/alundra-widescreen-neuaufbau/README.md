# Plan: Alundra-Widescreen neu aufbauen (Widescreen / Hintergrundfarbe / Kartenrand)

> **Hinweis:** Zurückgestellte Punkte (Messungen am Spiel, Referenzbilder, Clear-Farben) stehen in [offen.md](offen.md).

Stand: 2026-11-22. Projekt: `alundra-recomp`. Betroffen: `mods/alundra_widescreen.c` (842 Zeilen), Manifest, `CMakeLists.txt`, `game.toml`.

## Ziel

Der heutige Mod `alundra_widescreen.c` vermischt alles: Kacheln, Wolken, Maske, Schatten, Kartenrand-Quads, Außenfüllung, Raumfarben-Switch, Mine-Dunkelfüllung. Die Rand-Heuristiken (`alundra_tiles_overlap`, `room_fill`, Spaltenlimit, Außenfüllung aus VRAM) haben immer wieder geflackert oder Blöcke gezeigt (siehe `docs/memory/alundra-raum-hintergrund-clear.md`).

Neuer Ansatz (`docs/memory/alundra-clear-layer-ansatz.md`): Die Clear-Schicht (FillRect 0x02, 320x240, hinter allen Grafiken) wird pro Raum eingefärbt. Das gilt links und rechts ohne Randerkennung.

Drei getrennte, einzeln schaltbare Mods:

| Mod (Feature) | Plugin | Aufgabe |
|---|---|---|
| `widescreen` | `alundra.widescreen` | **Nur** 16:9: Aspekt, Kacheln verbreitern, Wolken/Nebel, Maske, (Tor-Schatten). Kein Eingriff in Farben oder Ränder. |
| `background_color` | `alundra.bgcolor` | Clear-Schicht pro Raum einfärben. Default Schwarz, Raumtabelle per Hash-Switch. |
| `map_edge_fade` | `alundra.edgefade` | Weicher Übergang ins Schwarze am Kartenrand (heute nur Dorf). |

## Entscheidungen (vom Nutzer)

- Der heutige Mod wird **umbenannt** (Referenz, nicht mehr gebaut), der neue Widescreen-Mod startet sauber und übernimmt nur, was Widescreen ist.
- Default der Hintergrundfarbe ist **Schwarz** (wie im Standard). Abweichungen werden pro Raum gefunden, nach Beobachtung auch über andere Mechanismen (viele Räume haben einen festen Farbton, z. B. die Mine).
- Der Randübergang im Dorf wird ein eigener Mod.
- Der Raumfarben-Switch (FNV-1a-Hash der Kartenzeilen) wandert in den Hintergrundfarben-Mod.
- Test nur im Debug-Build (`build-debugtools`), Release nur auf Nachfrage.

## Phasen

| # | Datei | Inhalt | Neue Sites / `generate`? |
|---|---|---|---|
| 0 | [phase-0-vorbereitung.md](phase-0-vorbereitung.md) | Sicherung, Testmatrix, Referenzbilder, Clear-Farben messen | nein |
| 1 | [phase-1-umbenennen-geruest.md](phase-1-umbenennen-geruest.md) | Alt-Mod umbenennen, leeres Gerüst, gemeinsamer Header, Manifest/CMake | nein |
| 2 | [phase-2-widescreen-kern.md](phase-2-widescreen-kern.md) | Reines Widescreen aus dem Alt-Mod herauslösen | nein |
| 3 | [phase-3-hintergrundfarbe.md](phase-3-hintergrundfarbe.md) | Clear-Schicht einfärben, Raum-Switch, Default Schwarz | evtl. ja |
| 4 | [phase-4-kartenrand-mod.md](phase-4-kartenrand-mod.md) | Dorf-Randverlauf als eigener Mod | nein |
| 5 | [phase-5-dunkle-raeume.md](phase-5-dunkle-raeume.md) | Mine/dunkle Räume ohne Extra-Quads, falls möglich | nein |
| 6 | [phase-6-abschluss.md](phase-6-abschluss.md) | Gesamttest, Aufräumen, Doku, Memory, CLAUDE.md | optional (Aufräumen) |

Reihenfolge ist verbindlich: 2 vor 3 (sonst überlagern sich Alt-Rand-Code und Clear-Farbe), 3 vor 4 und 5.

## Übergreifende Risiken

1. **Clear-Paket wird vom Spiel jeden Frame neu geschrieben.** RAM-Schreiben wirkt nicht; es braucht einen Hook am echten Schreiber oder eine Anpassung im GPU-Decoder (Phase 3a klärt das zuerst).
2. **Mehrere Plugins auf derselben Hook-Site.** Heute teilen sich Kern, Rand und Dunkelfüllung `0x8002D444` (`alundra_after_tiles`). Ob zwei Plugin-IDs dieselbe Adresse und dasselbe Wort registrieren dürfen, ist ungeprüft (Phase 1).
3. **Eine Activation pro Plugin?** Die Arenen (`psx_mod_alloc_*`) werden heute zentral in `alundra_widescreen_activate` angelegt; bei mehreren Dateien pro Feature muss geklärt sein, wie das aufgeteilt wird (Phase 1).
4. **Ohne Randfüllung zeigt der 16:9-Rand die Clear-Farbe.** Wo das Spiel am Rand Kacheln malt (Dorf-Felswand, dunkelgrüne Randkacheln), kann der Übergang hart aussehen. Dafür sind Phase 4 und die Raumtabelle in Phase 3 da.
5. **Alte Save States** laden nach dem Kachelpuffer-Umbau schon nicht mehr (bekannt, `alundra-kachelpuffer-ueberlauf.md`).

## Bekannte Raumhashes (Startwerte für die Tabelle)

| Raum | Hash | Anmerkung |
|---|---|---|
| Dorf | `0x0B440C2D`, `0xB4655671` (anderer Spielstand), Rand-Hash `0x1D39BE10` | links Randverlauf 12 px, rechts 28 px |
| Mine-Problemraum | `0x877DDF27` | Außenfüllung (8,8,0) |
| Mine, anderer Raum | `0xD78EE04C` | passt schon, Default |
| Mine-Raum 3 | `0x56AA69AF` (Rand `0x52D040E7`) | Spalten 8..22 gefüllt, Füllung (8,8,0) |
| Skelett-Raum | `0x793D39CF` | Spiel-Clear (0,8,0) |
| Skelett-Raum 2 | `0x1B8E3013` | rechte Kante nie geprüft |
| Speicher-/Laderaum | (Hash fehlt) | Nebelstreifen-Szene, Kantenquad nicht nötig |

Hash-Berechnung: FNV-1a über 24960 B ab Pointer 0x800DD86C (`debug_client.py --port 4370 read`).

## Was bleibt unverändert

HUD-Mod (`alundra_hud.c`, Feature `hud_corners`) wird nicht angefasst. Er hängt an 16:9, aber nicht an Rand oder Farbe.
