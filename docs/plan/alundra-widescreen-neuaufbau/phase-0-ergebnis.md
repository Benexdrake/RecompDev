# Phase 0: Ergebnis

Stand: 2026-11-22. Branch `widescreen-neuaufbau` (Hauptrepo und Submodul `alundra-recomp`).

## Erledigt

1. **Git-Stand gesichert.** Submodul-Commit `998d104` ("Stand vor Widescreen-Neuaufbau") auf Branch `widescreen-neuaufbau`, gepusht. Alt-Mod ist damit wiederherstellbar.
2. **Backups** (`.bak2`, `.pre_*`) bleiben unangetastet liegen, werden später nicht in CMake eingetragen.
3. **Testmatrix** (unten) mit den bisher bekannten Hashes festgelegt.

## Testmatrix (Debug-Build, 16:9, Spielstand von Hand laden)

| Raum | Hash | Spiel-Clear RGB | Referenzbild | Kamera-X min/max | Prüft |
|---|---|---|---|---|---|
| Dorf (Rand links/rechts) | offen | offen | offen | 0 / 927 | Rand, Verlauf, Felswand links |
| Mine 1 | `0x877DDF27` | offen | offen | 0 / ? | Farbton, Dunkelheit (Kamera X=0, Außenbereich graugrün) |
| Mine 3 | `0x56AA69AF` (Rand-Hash `0x52D040E7`) | offen (Füllung heute 8,8,0) | offen | offen | Farbton, Dunkelheit |
| Anderer Mine-Raum | `0xD78EE04C` | offen (Farbe passt mit `default`) | offen | offen | Farbton |
| Skelett-Raum 1 | `0x793D39CF` | erwartet (0,8,0) | offen | offen | kein Block |
| Skelett-Raum 2 | `0x1B8E3013` | erwartet (0,8,0) | offen | offen | kein Block |
| Speicher-/Laderaum | offen | offen | offen | offen | Nebelstreifen |
| Grabstätte | offen | offen | offen | offen | Randfarbe |
| Schuppen | offen | offen | offen | offen | Randfarbe |
| Haus | offen | offen | offen | offen | Randfarbe |
| Außengebiet mit Gras | offen | offen | offen | offen | Rand, einheitliche Kacheln |
| Raum mit Ringmaske/Licht | offen | offen | offen | offen | Maske gestreckt |
| Tor | offen | offen | offen | offen | kein Schatten-Kreis |
| Start ohne Start-Menü / Start-Menü | – | – | offen | – | HUD unverändert |

## Offen (braucht den Nutzer am Spiel)

Die Punkte 4–6 der Phase (Referenzscreenshots, Clear-Farben per `PSX_DEBUG_FILL_ONLY=1`, fehlende Hashes) setzen voraus, dass der Spielstand pro Raum von Hand geladen wird. Ablauf pro Raum:

1. `cd build-debugtools; PSX_DEBUG_SERVER=1 PSX_DEBUG_FILL_ONLY=1 ./Alundra.exe --debug-port 4370`, Spielstand laden, Raum anlaufen.
2. Hash und Kamera lesen (`read 0x800E4328 8`, Hash aus dem Debug-Log des Mods).
3. `gpu_frame_dump frame=N`: Eintrag mit op 0x02, Farbwort `0xCCBBGGRR` notieren.
4. `screenshot_wide_hires path=docs/plan/alundra-widescreen-neuaufbau/ref/<raum>.png`.

Sag Bescheid, sobald du im Spiel bist; dann gehe ich die Räume mit dir durch und trage die Tabelle nach.

## Abnahme

Nutzer bestätigt die Raumliste, danach Phase 1.
