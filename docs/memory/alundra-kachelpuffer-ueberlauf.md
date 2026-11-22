---
name: alundra-kachelpuffer-ueberlauf
description: Alundra 16:9: Kachelpuffer-Überlauf zerstörte VRAM (Rauschen) in Baumstadt-Szene; Fix = private Arena per Hook 0x8002CFD8; Randfix danach weg (offen)
metadata:
  type: project
---

Stand 2026-11-22, `mods/alundra_widescreen.c` (`alundra_tilebuf`), `game.toml` Site 0x8002CFD8 (Wort 0x00438821, `ADDU s1,v0,v1`).

**Symptom:** Nach einer Szene (Leiter hoch, Kamera schwenkt, Baumstadt mit zwei Kachelebenen) erst Flackern, dann komplett Pixelrauschen in allen Kachelseiten. Kachel-Tabelle (0x800DCF10) und VRAM-Hash waren zunächst unauffällig.

**Ursache:** Das Spiel gibt pro Parität 12000 B = 600 Kachelpakete (20 B) bei 0x800DD878 + 13600*Parität, danach 1600 B Pool aus 8-Byte-E1-Paketen (s1 = s0 + 12000), danach Spielvariablen (0x800E42BC.., Kamera 0x800E4328, Palettenzeiger 0x800E4320). Keine Grenzprüfung. 4:3 braucht ~550, 21 Spalten x 2 Ebenen bis ~714+ -> Überlauf in E1-Pool und Variablen; der GPU-DMA-Walker führte Variablenwerte als Befehle aus (0x80 VRAM-Kopie) -> VRAM zerstört. Beweis: Falle (`gpu_frame_dump` mit Ops 0x80..0xDF, src 0xE42BC/E4320/E4330).

**Fix:** Hook setzt s0 = Arena + Parität*STRIDE (1500 Kachel- + 800 E1-Pakete pro Parität), s1 = s0 + 30000. **Falle:** Das Spiel initialisiert die Kachelpakete nur einmal vorab (Kopf 0x04000000, 0x65808080, +16 = 0x00100018) und schreibt pro Frame nur x/y/u/v/clut + Link. Die Arena wird nach der Aktivierung gelöscht (`psx_mod_memory_reset_session`), die Vorlage muss im Hook nachgeschrieben werden (prüft Wort +4 == 0x65808080). Ohne Vorlage: Raum komplett leer.

**Nebenwirkungen:** Save States von vorher laden nicht mehr (Arena-Größe). Debug: `read` auf 0x8080xxxx liest nicht die Arena (spiegelt anderes), Zähler per Hook ausgeben. Testschalter `ALU_NO_TILEBUF=1` (Env) schaltet den Hook ab.

**Bestätigt (2026-11-22, Nutzer): Baumstadt-Szene läuft ohne Rauschen, "sehe keine Probleme mehr".** Der Rand fehlte nur im Memory-Card-Laderaum (kein Zusammenhang mit dem Fix bekannt), in der Baumstadt ist der Randverlauf da. Nur Debug-Build gebaut, Release nicht. Debug-Ausgaben entfernt; `ALU_NO_TILEBUF`-Schalter bleibt.

Siehe [[alundra-recomp-status]].
