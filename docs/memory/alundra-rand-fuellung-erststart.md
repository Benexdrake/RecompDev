---
name: alundra-rand-fuellung-erststart
description: Alundra Dialog: schwarzer Balken links nur nach Exe-Neustart, weil Füllfarbe nie gesampelt wurde (Kartenrand außerhalb 4:3)
metadata:
  type: project
---

Symptom: Nach frischem Start der Alundra.exe schwarzer Balken (x -53..Rand) links im Dialog (Kamera X=20), nach Reden/Neuladen weg.

**Ursache:** `alundra_after_tiles` sampelte die Füllfarbe (`g_alu_rgb_l/r`) nur, wenn der Kartenrand im 4:3-Bild lag (`xl >= -1`, `xr <= 316`). Bei Kamera X>0 liegt der Rand außerhalb, `g_alu_rgb_*_ok` blieb 0, kein Fill -> Clear-Farbe (schwarz).

**Fix (2026-11-22, Release + Debug gebaut, Nutzertest offen):** Rand außerhalb des 4:3-Bilds, aber im 16:9-Bild: Sampling an der äußersten sichtbaren Spalte (links x=2, rechts x=316).
Ergänzt [[alundra-rand-fuellung-blinken]], [[alundra-randfarbe-fill-stale-spalte]].
