---
name: bof3-widescreen-status
description: "State of 16:9 widescreen work in bof3-recomp: what works, cull sites found in main EXE, how to run the debug build"
metadata:
  node_type: memory
  type: project
  originSessionId: c5193a29-0b6e-40f3-b6ee-8a0fb06c1e0c
  modified: 2026-11-20T18:04:47.149Z
---

BoF3 (SLES-01304) 16:9 runs (battle + field confirmed by user 2026-11-20). Edge pop-in (black wedges) was the defect; fixed 2026-11-20.

What made 16:9 work:
- Runtime clamps aspect from toml to 4:3; only mod plugin mods/bof3_widescreen.c (psx_mod_set_fixed_display_aspect(16,9)) enables it; manifest format_version 11; CMake target_sources. game.toml needs `[widescreen] gte_game_mode = true`.
- Build: retcomm toolchain dir (~/.local/share/retcomm/toolchains/cmake-clang-v1/1.0.14/bin) on PATH, `python psxrecomp/psxrecomp_cli.py rebuild --config game.toml --project-root . --build-dir build-debugtools --no-pgo --cmake-extra=-DPSX_DEBUG_TOOLS=ON`. The CLI forces PSX_DEBUG_TOOLS=OFF unless --cmake-extra overrides it (without it gpu_gp0_ring capacity is 0 and gpu_frame_dump is empty).
- Run debug build: `cd build-debugtools; PSX_DEBUG_SERVER=1 ./BreathOfFire3.exe --debug-port 4370`; client `python psxrecomp/tools/debug_client.py <cmd> k=v`. `ws_census` takes positional args (start end file). Use `gpu_ring_stats` newest_frame for gpu_frame_dump (alternate frames are empty), `disasm addr= count=` for main-EXE code, `screenshot_wide_hires path=` to see the real image (Read can view PNGs).

FIXED (user confirmed gaps gone in the cave battle, 2026-11-20). Cull finding (2026-11-20): the earlier "no cull exists" conclusion was wrong because scans only covered overlay captures. The MAIN EXE has object/tile SX culls `lhu SX; addiu +bias; andi 0xFFFF; sltiu W`, each paired with a Y test: 0x8014C73C, 0x80153668, 0x80156344, 0x8015656C, 0x80156810, 0x80157CC4 (windows ~[-50..370] etc, narrower than 16:9's ~-53..373). These were added to game.toml `[widescreen.cull] screen_x_sites`. Needs game-C regen (>10 min) + rebuild; regen + rebuild done. Untested: world map, towns, menus, FMVs.

**Why:** the analyzer's auto_screen_x needs a paired sltiu 0x140/0xE0 form that BoF3 doesn't use. **How to apply:** if gaps remain, scan main EXE (disc/SLES_013.04, text at 0x80096800, file offset 0x800) for further SX compares (slti/sltiu with other immediates, bltz chains) and RTP4/RTPT callers (0x80156xxx-0x801581xx tile renderer); also the Y-paired sltiu sites (0x8014C758, 0x80153688, 0x80156360, 0x80156588, 0x80157CE4) are NOT X. Backups: game.toml.bak, CMakeLists.txt.bak.
