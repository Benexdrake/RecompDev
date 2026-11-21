---
name: bof4-lod-recomp-status
description: "BoF4 (EU) and Legend of Dragoon (DE, 4 discs) recomp projects: locations, serials, CHD conversion, build state, LoD 16:9 partially working"
metadata:
  node_type: memory
  type: project
  originSessionId: 6cc89c9a-f55e-4eef-a2e2-cb8d96b61eaf
  modified: 2026-11-20T18:40:03.511Z
---

Set up 2026-11-20, both release-built (untested in-game, 16:9 not started):
- BoF4: C:\RecompDev\bof4-recomp, SLES-03552, boot SLES_035.52, entry 0x80136DA0, build-release\BreathOfFire4.exe, disc C:\Discs\BOF4\*.cue (2 tracks).
- Legend of Dragoon: C:\RecompDev\lod-recomp, SCES-03045 (discs 2-4: SCES-13045/23045/33045), boot SCES_030.45, load 0x80188888, entry 0x801C0620, only 73 seeds (overlay-heavy, likely needs seed work), build-release\LegendOfDragoon.exe. Discs in C:\Discs\LOD\D1..D4; game.toml has `discs` + `disc_serials` added by hand (use forward slashes, LF line endings).

CHD conversion: no chdman; build libchdr (`ninja chdr` in a project's psxrecomp/recompiler/build with toolchain on PATH), then `python tools/psx_chd.py <chd> --extract <dir> --no-hash`.
Setup gotchas: don't run two setup_project.ps1 in parallel or delete dirs while one runs; use `-ExecutionPolicy Bypass`; run via a .ps1 wrapper with `*>` log and `-NoBuild`, then rebuild with psxrecomp_cli.py. Recipe as [[bof3-widescreen-status]] and [[alundra-recomp-status]].

**Why:** avoids repeating setup mistakes. **How to apply:** next step is playtest, then 16:9 (both are 3D: try gte_game_mode + fixed aspect mod + screen_x cull sites as in BoF3).

**LoD 16:9 (2026-11-20, final state):** user confirmed: 16:9 works in battle, edge polygon pop-in fixed. Setup = mods/lod_widescreen.c (only sets 16:9) + manifest + game.toml `[widescreen] gte_game_mode` + `[widescreen.cull] slti_sites` (39x `slti x,193`) / `slti_lower_sites` (40x `slti x,-192`) in battle overlay 0x800CC..0x800DE (found via overlay_xref.py scan of captures; LoD draws centre-origin, 384 wide, so bounds are +-192). No game regen needed for overlay sites. Field scenes: pre-rendered scrolling backdrop strips (4-6 tiles of 128x256) stay 4:3-wide, so black side margins remain; user chose to leave it. Stretch attempt (tag tiles via gpu_ws_tag_background_prim in a list-kick hook; framework hook added in lod-recomp/psxrecomp gpu.c/dma.c) filled width but caused cyan CLUT artefacts on foreground pieces; reference copy in lod-recomp/analysis/lod_widescreen_backdrop_stretch.c.txt. Untested: world map, towns, menus, FMV. Debug build: build-debugtools (port 4370).
