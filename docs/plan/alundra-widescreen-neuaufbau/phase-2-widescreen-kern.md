# Phase 2: Reiner Widescreen-Mod

> **Hinweis:** Zurückgestellte Punkte (Messungen am Spiel, Referenzbilder, Clear-Farben) stehen in [offen.md](offen.md).

Ziel: Alles, was **nur** der Breite dient, aus dem Alt-Mod in den neuen Widescreen-Mod übernehmen. Keine Randfüllung, keine Raumfarben.

## Übernehmen (Quelle: `alundra_widescreen_legacy.c.txt`)

| Baustein | Hooks/Sites | Anmerkung |
|---|---|---|
| Aspekt | `psx_mod_set_fixed_display_aspect(16, 9)` | Activation |
| Kachelschleife 21 Spalten | 0x8002CED0, 0x8002CF04, 0x8002CEF0, 0x8002D14C (`alundra_use_xtab`) | private X-Tabelle (`g_alundra_xtab`) |
| Spaltenlimit Kartenbreite | `alundra_clamped_cols`, `ALU_MAP_COLS` 52 | bleibt zunächst (jenseits der Karte schwarz, bestätigt). Prüfen, ob es mit dem Clear-Ansatz noch nötig ist |
| Kachelpuffer-Arena | 0x8002CFD8 (`alundra_tilebuf`) | Überlauf-Fix, zwingend |
| Wolken/Schatten-Overlay | 0x8005C538 / 0x8005C5F4 / 0x8005C4E8, 28-KB-Arena | `ALU_CLOUD_WIDEN` |
| Speicherraum-Nebel | 0x800262EC (`alundra_cloud_strip`) | |
| Ringmaske gestreckt | 0x8005D5E0 (`alundra_mask_stretch`) | |
| Tor-Schatten | 0x8002DDF4 (`alundra_shadow_part`) | Spiellogik-Fix; hier lassen oder später in ein eigenes Feature auslagern (Nutzerentscheid) |

## NICHT übernehmen

`alundra_after_tiles` (Kantenquad, Außenfüllung, Lückenfüllung, `room_fill`, Hook 0x8002D444), `alundra_tiles_overlap`, `alundra_edge_sample`, `alundra_zone_dark`, `alundra_blend`, `alundra_outside_build`, `alundra_fix_stale_col`, `alundra_room_clear`, `alundra_dark_fill`, `ALU_EDGE_TILE_SHADE` samt Hooks 0x8002D220/0x8002D390. Diese gehen in Phase 3 bis 5 an die neuen Besitzer oder entfallen.

## Offene Punkte

- **Dunkelraum-Erkennung** sitzt heute im Wolken-Hook (`alundra_cloud_loop` zählt Randspalten). Zählung vorerst stehen lassen, Quad-Bau weglassen; Phase 5 entscheidet.
- **`g_alu_map_cols` pro Raum** wurde in `alundra_after_tiles` gesetzt (Wert vom Vorframe). Ohne diesen Hook bleibt es fest 52. Sonderfall Skelett-Raum: Karte geht dort weiter, das Limit schnitt echte Karte ab. In Phase 3 prüfen, ob das Limit mit Clear-Farbe ganz fallen kann.
- `ws.active` im Debug-Befehl `gpu` zeigt 0 auch wenn es klappt; `present_native_43` prüfen (0 = 16:9).

## Test

Testmatrix aus Phase 0, ohne Rand-Behandlung. Erwartet: Kacheln, Wolken, Nebel, Maske, Tor stimmen; der Rand zeigt die Spiel-Clear-Farbe (Schwarz / (0,8,0)). Keine Quad-Streifen, kein Flackern. Vergleich mit den Referenzbildern nur für Kacheln, Wolken, Maske.

## Abnahme

Nutzer bestätigt: Widescreen stabil in den Testräumen. Kein `generate` nötig (unbenutzte Sites bleiben vorerst in `game.toml`).
