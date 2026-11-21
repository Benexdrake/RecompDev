---
name: psx-force-60hz
description: "PAL->60Hz override is now DEFAULT ON in all 4 recomp projects (bof3, alundra, bof4, lod); PSX_FORCE_60HZ=0 disables"
metadata:
  node_type: memory
  type: project
  originSessionId: 5f797392-1190-497b-9168-320b0195d9f6
  modified: 2026-11-21T11:19:51.024Z
---

psx_video_timing.c in all four projects forces NTSC 60 Hz timing by default (since 2026-11-21). Set `PSX_FORCE_60HZ=0` to get 50 Hz back. User tested all four, no problems. Release builds rebuilt. Doc: C:\RecompDev\PAL_ZU_60HZ.md.

**Why:** 50 Hz PAL ran choppy on 60 Hz panels; game runs ~20% faster (NTSC speed), accepted by user.
**How to apply:** don't re-add the env var requirement; for new PAL projects copy the same patch. Debugtools builds not rebuilt.
