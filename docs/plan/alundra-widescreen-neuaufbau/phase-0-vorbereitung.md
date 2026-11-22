# Phase 0: Vorbereitung

> **Hinweis:** Zurückgestellte Punkte (Messungen am Spiel, Referenzbilder, Clear-Farben) stehen in [offen.md](offen.md).

Ziel: Ausgangslage sichern und messbar machen, damit jede spätere Phase gegen Referenzen geprüft werden kann.

## Aufgaben

1. **Git-Stand sichern.** Aktuelle, nicht committete Änderungen in `alundra-recomp` (Submodul) committen, damit der Alt-Mod wiederherstellbar ist. Nur nach Freigabe des Nutzers.
2. **Backup-Kopien** (`.bak2`, `.pre_*`) bleiben liegen, werden nicht ins neue Gerüst übernommen und nicht in CMake eingetragen.
3. **Testmatrix festlegen** (Debug-Build, 16:9, Spielstand von Hand laden):

   | Raum | Prüft |
   |---|---|
   | Dorf (links/rechts Rand) | Rand, Verlauf, Felswand links |
   | Mine 1 (`0x877DDF27`), Mine 3 (`0x56AA69AF`), anderer Mine-Raum (`0xD78EE04C`) | Farbton, Dunkelheit |
   | Skelett-Raum 1/2 | Clear (0,8,0), kein Block |
   | Speicher-/Laderaum | Nebelstreifen |
   | Grabstätte, Schuppen, Haus | Randfarbe (laut Notizen alle gleich) |
   | Ein Außengebiet mit Gras | Rand mit einheitlichen Kacheln |
   | Ein Raum mit Ringmaske/Licht | Maske gestreckt |
   | Tor | kein schwarzer Schatten-Kreis |
   | Start (HUD ohne Start-Menü), Start-Menü | HUD-Mod unverändert |

4. **Referenzscreenshots** pro Raum aus dem heutigen Stand: `screenshot_wide_hires` (Ablage `docs/plan/alundra-widescreen-neuaufbau/ref/`, nicht einchecken, wenn groß). Zusätzlich Hash und Kamera-X-Min/Max je Raum notieren.
5. **Clear-Schicht pro Raum messen** (Grundlage für Phase 3): Debug-Build mit `PSX_DEBUG_FILL_ONLY=1` starten, pro Raum die Farbe des Clear-FillRects aus `gpu_frame_dump` (Befehl 0x02, Wort `0xCCBBGGRR`) notieren. Tabelle `Raum | Hash | Spiel-Clear RGB` anlegen.
6. **Fehlende Hashes nachtragen** (Speicherraum, Grabstätte, Schuppen, Haus, Gras-Außengebiet).

## Ergebnis

- Testmatrix mit Hashes und Referenzbildern.
- Tabelle der Spiel-Clear-Farben je Raum. Sie zeigt, ob "Default Schwarz" mit dem Spiel übereinstimmt oder ob das Spiel teils (0,8,0) nutzt.

## Abnahme

Nutzer bestätigt die Raumliste. Danach Phase 1.
