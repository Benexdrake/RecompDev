---
name: alundra-usa-port
description: Alundra USA (Definitive Edition v4, SLUS-00553) Port auf Branch usa-slus-00553; Disc-Patch, Einrichtung, Stand
metadata:
  type: project
---

Stand 2026-11-24: Branch `usa-slus-00553` in `alundra-recomp`, USA-Disc bootet im Debug-Build (Intro-Szene läuft, 4:3). Mods/Widescreen noch NICHT portiert (`mod_instruction_sites = []`).

**Disc:** Original `Downloads\Alundra - Definitive Edition v4 (USA)` (Fan-Patch, 565580736 B). `SYSTEM.CNF` bootet dort `EPIX.EXE` (45-KB-Lader mit Menü: EASY/HARD/DEBUG MODE/INTRO/ENDING laut `PROGRAMS.TXT`). Das Spiel selbst ist `EASY_005.53` bzw. `HARD_005.53` (je 1,2 MB, Load 0x80020000, Entry 0x80036044, text 0x12E800; DE: Entry 0x800360F4, text 0x12B000).
**Kopie `C:\Discs\AlundraUS\` (game.bin + Alundra.cue) ist gepatcht** (Original unberührt): `SYSTEM.CNF` -> `BOOT=cdrom:\SLUS_005.53;1` (gleiche Länge 65 B, Leerzeichen entfernt), Verzeichniseintrag `EASY_005.53;1` -> `SLUS_005.53;1` (Sektor 22 / SYSTEM.CNF Sektor 48460). Ohne das findet der Runtime keine Serial, und das BIOS bootet den Lader. Der Spielstart ist damit immer EASY (kein Schwierigkeits-Menü, HARD nicht erreichbar).
MD5 `b1a1a01a890cc9f939dd7d14e833bd27`, SHA1 `e0172f00...`, CRC32 `c14e9fca`.

**Projekt-Umbau (nur auf dem Branch):** `game.toml` (id, exe `disc/SLUS_005.53`, Entry, text_size, Digests, Netplay-fp, Sites leer), `CMakeLists.txt` (GEN_MARKER/GEN_FULL_GLOB), `.recomp.json`, `catalog_identity.json`, `disc_probe.json`, Manifest `game_id`, `seeds/ghidra_funcs.txt` (nur JAL-Scan, 493 Seeds). `disc/SLUS_005.53` aus EASY extrahiert. DE-Stand gesichert als `generated.de_main/`, `build-debugtools.de_main/`, `*.de_main`-Dateien (gitignored bzw. unversioniert); `generated/` und `build-debugtools/` sind jetzt US.
Zurück auf DE: Branch `main`, `generated.de_main` -> `generated`, `build-debugtools.de_main` -> `build-debugtools` zurückbenennen.

**Fallen:** `rebuild` allein regeneriert nicht (immer erst `generate`). Debug-Client `screenshot_file` braucht gültigen Pfad; `screenshot_wide_hires path=<Windows-Pfad mit \>` ging.

**16:9-Kacheln fertig (2026-11-24, Debug-Build, Screenshot ok):** US-Kachelroutine ~0x8002D0C0..0x8002D7A4 (DE +~0x300..0x360, Code anders aufgebaut). Sites in `game.toml`: 0x8002D1CC/0x8002D204 (SW s3,32(sp): Spaltenzahl in **s3**, nicht t8), 0x8002D1EC (first_col, Wort 0xAFB60010), 0x8002D2F0 (Kachelpuffer-Arena, 0x00438821; US-Puffer 0x801D0FF8 + 13600*Parität), 0x8002D4B0 (t6 = X-Tabelle 0x800203F0 -> private Tabelle), 0x8002D778 (SLT t6,v0: Schleifenende vergleicht gegen Original-Tabelle+2*Spalten, Hook rechnet auf private Tabelle um; Wort 0x01C2102A). Hooks `alundra_us_*` in `mods/alundra_widescreen.c`. Methode: gpu_frame_dump (0x65-Pakete, src) -> wtrace_add auf Paketadresse -> Schreiber-PCs -> disasm; RAM-Dump per read_ram in 16-KB-Blöcken. Wortvergleich DE/US per difflib brachte wenig (Code zu verschieden).
Fallstück: Hook-Wort muss exakt dem RAM entsprechen (erst falsch kodiertes SLT -> Hook greift still nicht, nur 1 Spalte).

**Wolken/Schatten fertig (2026-11-24, Boot-Szene, Screenshots ok):** US-Routine ~0x8005E488..0x8005E804 (DE 0x8005C294), 21->30 Spalten in GPU-DMA-Arena. Sites: 0x8005E6B0 (ADDU s6,t1,zero; t0 = Arena, Layer-Index in **s2**), 0x8005E6F8 (SUBU t6,t5,t9; a3 -= 4 Spalten mit Wrap 40, t1 = -64), 0x8005E7B8 (BNE v0, Wort 0x1440FFD1; v0 = t1 < 416). Hooks `alundra_us_cloud_*`. Ohne Dunkelraum-Erkennung (`g_cl_hide`, Randzähler) - die kommt mit Mine/Raumfarben.

**Hintergrund (Spiel-Clear):** funktioniert in US ohne Mod-Code. Nutzer sieht die Farbe als etwa (8,0,0); DE ist laut Raum-Hintergrund-Notiz (0,8,0) - Abweichung nicht geprüft (nur Nutzer-Beobachtung, nicht per Pixelwert verifiziert).

**Pillarbox + Ringmaske (2026-11-24, Kars-/Melzas-Szene, Screenshots ok):** Raum-Hashes in US identisch zu DE (`0xB3BDE1C5`/`0xE93D8AA1`), nur Adressen anders: `alundra_common.h` jetzt US (Karten-Zeiger 0x801AC6C4, Kamera X/Y 0x801EF434/438). Pillarbox-Site 0x8002D7A4 (Wort 0x0000C021, OT-Basis in **fp**, nicht sp+0x58). Ringmaske (120 0x67-Streifen, wellige Nebel-Vignette): Hook `alundra_us_mask_stretch` auf 0x8005F784 (JR ra; a2 = Sprite, t4 = OT-Slot-Pointer, Texpage fest 0x3D, Streifen-Routine 0x8005F5C8, Aufrufer 0x8005ECB8). Nebel läuft jetzt über 16:9. Achtung: `alundra_common.h` ist damit nur noch US-tauglich (DE-Werte im Kommentar).

**Nächste Schritte:** Kantenquad/Kartenrand, Wolken, Speicher-Nebel, HUD, Maske, Schatten, Pillarbox per Befehlsmuster im US-Code neu finden; Spiel nach dem Intro testen (Titel, Neues Spiel, Menüs); Release-Build nicht gebaut.

**Update 2026-11-24 (abends):** Weitere Mods portiert (Tor-Schatten 0x8002E150, bgcolor 0x8008952C, edgefade 0x8002D7A4, HUD-Sites 0x8004D588/0x8004D6B4). Nutzer bestätigt: Farben stimmen immer (evtl. wegen der angepassten Fan-Patch-ISO). Branch in `main` gemergt. Test: Claude startet das Debug-Build nach jedem Rebuild selbst.
