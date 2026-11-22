# Offen (zurückgestellt)

Stand: 2026-11-22. Diese Punkte machen wir erst, **wenn der Widescreen wieder clean ist** (Ende Phase 2). Sie brauchen den Nutzer am Spiel (Spielstand pro Raum von Hand laden).

## Aus Phase 0

- Referenzscreenshots pro Raum aus dem heutigen Stand (`screenshot_wide_hires`, Ablage `ref/`, nicht einchecken, wenn groß).
- Hash und Kamera-X-Min/Max je Raum notieren.
- Clear-Schicht pro Raum messen: Debug-Build mit `PSX_DEBUG_FILL_ONLY=1`, Farbe des FillRects (Befehl 0x02, Wort `0xCCBBGGRR`) aus `gpu_frame_dump`. Tabelle `Raum | Hash | Spiel-Clear RGB`.
- Fehlende Hashes nachtragen: Speicherraum, Grabstätte, Schuppen, Haus, Gras-Außengebiet.
- Nutzer bestätigt die Raumliste.

Ablauf pro Raum und Testmatrix: [phase-0-ergebnis.md](phase-0-ergebnis.md).

## Auswirkung auf spätere Phasen

Die Clear-Farben-Tabelle ist Grundlage für Phase 3 (`background_color`). Bis sie vorliegt, gilt dort der Default Schwarz plus die bereits bekannten Räume aus dem Alt-Mod.
