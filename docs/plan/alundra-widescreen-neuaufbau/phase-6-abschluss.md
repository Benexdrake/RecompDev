# Phase 6: Gesamttest und Abschluss

> **Hinweis:** Zurückgestellte Punkte (Messungen am Spiel, Referenzbilder, Clear-Farben) stehen in [offen.md](offen.md).

## Aufgaben

1. **Gesamttest** der Testmatrix aus Phase 0 mit allen drei Features an. Dann jedes Feature einzeln aus (`build-debugtools/mods/state.toml`, mit `package_id`) und prüfen, dass das Spiel ohne es sauber läuft. Besonders `widescreen` aus (4:3): Rand und Farbe tun nichts Falsches.
2. **Ungetestetes aus CLAUDE.md** mitnehmen: Sprite-Pop-in, Menüs, Dialoge mit HUD, FMV, Audio, Save/Load, Innenräume mit anderer Kartenbreite als 52, Release-Exe-Hänger beim ersten Start.
3. **Alt-Code entfernen:** `mods/alundra_widescreen_legacy.c.txt` und die `.pre_*`/`.bak*`-Dateien löschen oder nach `mods/archive/` verschieben (Nutzer entscheidet).
4. **Unbenutzte Sites aus `game.toml` `mod_instruction_sites` streichen** (0x8002D150 / 0x8002D220 / 0x8002D390 und was Phase 3 nicht braucht), danach `generate` (einige Minuten) und Rebuild. Nur wenn gewünscht; die Sites sind harmlos.
5. **Doku:**
   - `docs/memory/`: neuer Eintrag zur Aufteilung (Features, Dateien, Hooks, Raumtabellen). Alt-Einträge zu Rand/Füllung als "ersetzt durch Clear-Layer" kennzeichnen. `MEMORY.md` aktualisieren.
   - `CLAUDE.md` (Abschnitt Alundra): Mods, Dateien, Schalter, Raumtabellen und Teststand neu schreiben; die Abschnitte zu Kartenrand, Mine, Skelett-Raum, Raumfarbe auf den neuen Stand bringen.
   - `docs/ALUNDRA_WIDESCREEN_HANDOFF.md` verlinken bzw. aktualisieren.
6. **Release-Build nur auf Nachfrage** (Nutzerwunsch).
7. **Commit** nur auf Wunsch: Submodul `alundra-recomp` und Hauptrepo getrennt, Nachrichten wie bisher.

## Abnahme

Nutzer bestätigt: drei Mods laufen einzeln und zusammen, Doku ist auf dem neuen Stand.
