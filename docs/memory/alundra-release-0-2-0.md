---
name: alundra-release-0-2-0
description: Alundra Release 0.2.0 (USA, Windows-ZIP) - Packager-Befehl, Stolpersteine, Identitaetsdateien, GitHub-Draft
metadata:
  type: project
---

**Stand 2026-11-24:** Release `v0.2.0` ist gebaut, vom Nutzer getestet ("funktioniert") und als **Draft** auf GitHub (`Benexdrake/Alundra-Recomp`), Tag gepusht. Nur Windows-ZIP, unsigniert, kein Linux-AppImage. Das Release ist die **USA-Fassung (SLUS-00553)**, die DE-Version ist nicht enthalten (Kopien `*.de_main`).

**Befehl** (Git Bash, im Projektordner `alundra-recomp`, ca. 10 Min, baut in `build-package/`, Ergebnis `dist/`):
```
B="$HOME/.local/share/retcomm/toolchains/cmake-clang-v1/1.0.14/bin"
TC="C:\Users\BeneX Drake\.local\share\retcomm\toolchains\cmake-clang-v1\1.0.14\bin"
export PATH="$B:$PATH" PYTHONIOENCODING=utf-8 PYTHONUTF8=1
bash scripts/package_release.sh --channel public --platform windows --toolchain-bin "$TC"
```
Danach: `git push`, `git tag -a vX`, `gh release create vX dist/*.zip dist/*.sha256 --draft --notes-file ...`. Beim Veroeffentlichen im Draft den Tag auswaehlen, nicht "untagged".

**Stolpersteine:**
- Der Packager verlangt einen **sauberen Git-Baum** (vorher committen) und erwartet MSYS2 unter `C:\msys64`; deshalb `--toolchain-bin` setzen.
- In der retcomm-Toolchain fehlte `objdump.exe`; Kopie von `llvm-objdump.exe` dort abgelegt.
- Ohne UTF-8 (`PYTHONUTF8=1`) stuerzt er an einem Haekchen ab.
- Public-Gate lehnt `psx.enhancement.cd-speed` und `fast-loading` ab: in `CMakeLists.txt` per `EXCLUDE_BUILTIN_MODS` ausgeschlossen. Die Ladezeit-Aussagen (Memory-Card-Turbo) sind deshalb aus README/Notizen entfernt; in US ungetestet.
- Der Launcher prueft die Disc gegen `catalog_identity.json`/`disc_probe.json`. Beim US-Port waren die halb umgestellt (DE-MD5, disc_fp, entry_pc, text_size): neu erzeugen mit `python psxrecomp/tools/new_project_layout/probe_disc.py <cue> --json-out disc_probe.json --write-catalog catalog_identity.json --display-name Alundra --region USA --players 1` (nicht mit `--identity-only`). Bei jedem Disc-Wechsel pruefen.
- Das Paket darf keinen lokalen Disc-Pfad tragen: `packaging/release/game.toml` (= `game.toml` ohne `disc =`), eingetragen als `player_game_toml` in `packaging/release.toml`.
- `build-release/` ist noch der alte DE-Stand (22.11.), nicht fuers Release benutzen. Zum Testen das ZIP in frischen Ordner entpacken.

**Why:** Der Release-Weg ist vom Framework vorgegeben (wie MegaManX4Recomp); die Fehler lagen an der lokalen Toolchain und an halb umgestellten US-Daten.
**How to apply:** Fuer jedes weitere Release `VERSION` und `RELEASE_NOTES.md` anpassen, committen, obigen Befehl ausfuehren, ZIP frisch entpackt mit US-Disc testen, dann Draft.
