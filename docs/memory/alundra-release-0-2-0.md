---
name: alundra-release-0-2-0
description: Alundra Release 0.2.0 (USA, Windows-ZIP) - Packager-Befehl, Stolpersteine, Identitaetsdateien, GitHub-Draft
metadata:
  type: project
---

**Stand 2026-11-24:** Release `v0.2.0` ist gebaut, vom Nutzer getestet ("funktioniert") und als **Draft** auf GitHub (`Benexdrake/Alundra-Recomp`), Tag gepusht. Windows-ZIP (getestet) und Linux-AppImage (gebaut ueber WSL, nur Start bis Launcher getestet, ohne PGO), unsigniert. Das Release ist die **USA-Fassung (SLUS-00553)**, die DE-Version ist nicht enthalten (Kopien `*.de_main`).

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

**Linux-AppImage ueber WSL (`--platform linux`)** - Stolpersteine:
- WSL-Pakete noetig: `build-essential cmake ninja-build imagemagick curl file python3 pkg-config libsdl3-dev libgl-dev libegl-dev` (Installation als Root mit `wsl -u root`, kein sudo-Passwort noetig; ohne Nutzer-Freigabe blockiert die Auto-Mode-Pruefung das).
- libwebp-Entpacken scheitert auf `/mnt/c` (Umbenennen: Permission denied). Fix: Archiv in WSL nach `~/libwebp-src` entpacken (`tar --strip-components=1`) und `PSX_LIBWEBP_SOURCE_DIR=/home/<user>/libwebp-src` mit `WSLENV=PSX_LIBWEBP_SOURCE_DIR` und `MSYS2_ENV_CONV_EXCL=PSX_LIBWEBP_SOURCE_DIR` setzen (Git Bash wandelt sonst den Pfad um). `vendor_deps.sh` hilft nicht.
- PGO-Boot-Training in WSL scheitert (`no_disc`): die Projekt-`game.toml` hat den Windows-Disc-Pfad. Fuer den Linux-Build `selective_pgo = false` in `packaging/release.toml` setzen, committen, bauen, danach zurueck.
- `package_appimage.sh`/`AppRun`/`.desktop` muessen LF haben (`sed -i "s/$//"`, danach `git add -u`, sonst "set: pipefail: invalid option name"). `build-package/linux` vorher loeschen, wenn PGO-Reste drin sind.

**Disc-Korrektur (2026-11-24, nach Release):** Die "US-Disc" ist die Fan-Patch-ISO *Alundra - Definitive Edition v4 (USA)* (md5 5b14a3d8...) mit 2 geaenderten Sektoren (22, 48460; 54 Bytes: SYSTEM.CNF + Verzeichniseintrag EASY_005.53 -> SLUS_005.53). Das Release/README sagte zuerst faelschlich "unveraenderte SLUS-00553-Disc". Jetzt korrigiert; `alundra-recomp/tools/make_us_disc.py` erzeugt die Disc aus der DE-v4-bin (prueft beide MD5). Die ZIP/AppImage von 0.2.0 enthalten noch die alten README/DISC.md/RELEASE_NOTES -> bei 0.2.1 neu bauen. Retail-US-v1.1 ungetestet (Code ist anders: EASY_005.53 stammt aus dem Patch).
