---
name: alundra-mine-dunkel-staerke-gemessen
description: Alundra Mine: gemessene Stärke/Farbe der Original-Dunkelschicht (0x7F-Sprites) für die Außenfüllung, 2026-11-24
metadata:
  type: project
---

Gemessen per `gpu_frame_dump` + `vram_peek` im Mine-Raum (Debug-Build, 2026-11-24):
- Dunkelschicht = 0x7F-Sprites (16x16, raw texture, OT 0), E1 0xE100005D → Texpage x=832 (Seite 13), y=0, **subtraktiv B-F**, 4-bit-Textur. CLUT 0x7C10 (VRAM x=256, y=496).
- CLUT ist **reines Grau** (r=g=b), Index 13 (Innenfläche) = 10/31 subtrahiert, Dithering 7..12. Mittel Innenfläche ≈ 9,7/31 ≈ **31 %** (≈ 78 in 8 Bit), Randkachel u=0 ≈ 26 %.
- Also: Farbe Schwarz (subtrahiert gleich viel von R/G/B), keine Tönung. Subtraktiv = absoluter Abzug, kein Prozent der Helligkeit.
- Die Füllquads (cmd 0x2A, E1 0xE1000040) subtrahieren die 5-Bit-Zahl `c>>3`: Match mit Grauwert **0x4E** (9,7 → 78). Alt-Wert 0x66 (=12/31, 39 %) war zu stark.

**Why:** Der Nutzer sah, dass die Prozente der Füllung nicht zur Vignette passten. **How to apply:** Neuaufbau Phase 5 (`mods/alundra_bgcolor.c`, Mine) nutzt Grauwert ~0x4E statt 0x66. Gilt für CLUT 0x7C10; in anderen dunklen Räumen CLUT/Index erneut messen. Siehe [[alundra-mine-dunkel-fuellung]], [[alundra-raumfarbe-switch]].
