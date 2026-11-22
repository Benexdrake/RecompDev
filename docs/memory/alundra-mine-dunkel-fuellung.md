---
name: alundra-mine-dunkel-fuellung
description: Alundra Mine/dunkle Räume: Dunkelschicht nur 4:3 breit, 90%-Schwarz-Füllquads links/rechts, bestätigt 2026-11-22
metadata:
  type: project
---

In der Mine (dunkle Räume) ist die Dunkelheit KEINE Ring-Maske (0x67), sondern die Wolken-/Schattenschicht (Routine 0x8005C294, 16x16-Sprites cmd 0x7F, OT-Slot 0, 20 Spalten x 16 Zeilen bei x=0..320, Randspalten voll hoch). Die Layer-Karte (40 Spalten, 2 Byte/Zelle, Byte0 = 0 → leer) hat außerhalb von 4:3 keine Zellen, daher blieben in 16:9 helle Streifen links/rechts (Bildschirm-x < 0 bzw. >= 320). Die Wolken-Widening-Hooks helfen hier nicht, weil die Zellen dort leer sind.

Fix in `mods/alundra_widescreen.c`: `alundra_cloud_loop` zählt pro Frame emittierte Zellen (Zähler s2 ändert sich): Spalte x=0, x<0, x=304, x>=320 (`g_cl_now`, Snapshot `g_cl_snap` in `alundra_after_tiles`). Wenn Randspalte >= 12 Zeilen emittiert und dahinter 0 → flaches subtraktives Quad (cmd 0x2A, E1 0xE1000040, Farbe `ALU_DARK_FILL_COLOR` 0xE6 = ~90 % Schwarz) für -m-8..0 bzw. 320..320+m+8, y 0..240, in OT-Slot 959 (unter HUD und Overlay-Liste, über Welt). Arena `g_alundra_fill` (64 B). Vom Nutzer im Debug-Build bestätigt ("Perfekt, so passt es gut"). Stretch wie bei der Ring-Maske wurde verworfen (würde den Ellipsenrand verzerren).

**Why:** Erkennung über Vorframe-Zählung (1 Frame Verzögerung beim Raumwechsel möglich). Schwellwert 12 und Spalten 0/304 sind aus der Mine abgeleitet.
**How to apply:** Falls die Füllung in normalen Räumen (Wolken) auftaucht oder in anderen dunklen Räumen fehlt, die Schwellen/Spaltenpositionen prüfen (`gpu_frame_dump`: 0x7F-Sprites in OT 0, x-Verteilung). Ähnlich: [[alundra-ring-maske-stretch]]. Debug-Hinweis: Das Debug-Exe hängt manchmal nach längerer Laufzeit/Zweitinstanz; nur eine Instanz starten, sonst blockiert der Port.
