---
name: alundra-hud-menue-ausblenden
description: "Alundra HUD-Hook blendet das HUD aus, solange die HUD-Basis-Y nicht 0x10 ist (Start-Menü-Slide); bestätigt 2026-11-21"
metadata:
  node_type: memory
  type: project
  originSessionId: 2bd64dd2-b0f8-4dba-ae60-8d96358a4a87
  modified: 2026-11-21T15:20:24.606Z
---

Beim Öffnen/Schließen des Start-Menüs gleitet die HUD-Basis (0x800A825A) von y=16 nach y=-41. Der alte Hook verschob nur Pakete mit y>=0 in die Ecken, die mit y<0 rutschten original nach oben, sodass das HUD kurz doppelt erschien.

Fix in `mods/alundra_hud.c` (Post-Hook): `hidden = (s16)[0x800A825A] != 0x10`; dann werden alle HUD-Pakete mit y in [-64,0x40) um dy=-400 aus dem Bild geschoben (Undo läuft über die bestehende wertgenaue Record-Tabelle). Nutzer bestätigte "sieht gut aus". Release und Debug neu gebaut.

**Why:** Verhindert Doppel-HUD beim Menü-Slide.
**How to apply:** Falls das HUD beim Menü-Schließen stören sollte, Alternative wäre mitgleiten lassen statt ausblenden. Siehe [[recomp-docs-in-claude-md]] für HUD-Grundlagen.
