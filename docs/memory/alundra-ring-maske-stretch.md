---
name: alundra-ring-maske-stretch
description: Alundra Ring-/Lichtmaske (Turmräume) auf 16:9 gestreckt, Hook 0x8005D5E0, bestätigt 2026-11-21
metadata:
  type: project
---

Der Ring-Effekt (halbtransparente Lichtmaske, 4:3-breit) besteht aus 120 Sprites (cmd 0x67, Höhe 4, Breite <=256, OT-Slot 0) aus einer 256x240-4-Bit-Maske (Texpage 0x3D, CLUT 0x7C10). Sie entstehen in der generischen Objektroutine 0x8005D3xx (aufgerufen aus der Schleife bei 0x8005C8D0, Objekte à 20 B).

Fix: Hook `alundra_mask_stretch` in `mods/alundra_widescreen.c` auf Site 0x8005D5E0 (JR ra, Wort 0x03E00008; a3 = Sprite, t6 = OT-Slot-Pointer, t3 = Layer). Ersetzt jeden Streifen durch ein Textur-Quad (cmd 0x2F, 9 Wörter) in einer GPU-DMA-Arena (480 x 48 B), um 4/3 um x=160 gestreckt. Texpage aus Tabelle 0x8018CF66 + 2*idx (idx = Byte 2 der Layer-Definition, Layer-Tabelle 0x8018CF98). Site steht in `mod_instruction_sites`. Vom Nutzer im Debug-Build bestätigt ("Sieht gut aus").

**Why:** Sprites lassen sich nicht skalieren, das Framework hat kein Tag für 0x67-Streifen.
**How to apply:** Gleiches Muster (Sprite -> gestrecktes Quad am Funktionsende) für weitere 4:3-breite Overlays. Adressrechnung bei `LUI/ADDIU` mit negativem Immediate prüfen (0x80190000-12392 = 0x8018CF98). Siehe [[alundra-recomp-status]].
